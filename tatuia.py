from email import message
from tensorflow.keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.optimizers import SGD
from keras.layers import Dense, Activation, Dropout, SpatialDropout1D, LSTM, Embedding
from keras.models import Sequential
from keras import metrics
import tensorflow as tf
from messageutils import MessageUtils  # nossa classe de pré-processamento
import geradorfrases as gerador
import warnings
import numpy as np
import pandas as pd
import random
import pickle
import json
import os
from unittest import result

from src.load.DB import get_db,DBCollections

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# tensorflow tags
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed


# from keras.preprocessing.sequence import pad_sequences


class TatuIA:
    def __init__(self, dfa_file_path, message_utils: MessageUtils, lstm = True):
        self.dfa_file = dfa_file_path
        self.message_utils = message_utils  # classe de pré-processamento de textos
        self.model = self.__simple_ann() if not lstm else self.__simple_lstm() # neuranet do bot
        self.__train()
        self.PROB_SAFE_VALUE = 0.25

    def __load_model(self):
        # current_filepath = os.getcwd()
        # model_folder = "modelbot"
        # complete_path = os.path.join(current_filepath, model_folder)
        # if os.path.exists(complete_path):
        #     print(">>> Carregando o TatuBot do Disco")
        #     self.model = tf.keras.models.load_model(complete_path + "/model")
        #     print(">>> Fim do Carregando o TatuBot do Disco")
        # else:
        print(">>> Build do TatuBot")
        if self.model:
            self.__train()
        self.model = self.__simple_ann()
        self.__train()
        #os.mkdir(complete_path)
        #self.model.save(complete_path + "/model")
        print(">>> Fim do Build, TatuBot dumped")

    def __simple_ann(self):
        self.X = self.message_utils.X
        self.Y = self.message_utils.Y

        input_shape = (self.message_utils.X.shape[1],)
        output_shape = self.message_utils.Y.shape[1]
        # the deep learning model
        model = Sequential()
        model.add(Dense(128, input_shape=input_shape, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(output_shape, activation="softmax"))
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)

        #model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=[tf.keras.metrics.AUC()])
        model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['acc'])
        return model

    def __simple_lstm(self):
        """
            pré-processamento especial para a LSTM FIXME: realocar esse código.
        """
        df = pd.DataFrame(self.message_utils.documents,columns = ["token-frase","classe"])
        df["texto-lstm"] = df["token-frase"].apply( lambda message : " ".join(message))
        df = df.drop("token-frase",axis="columns")
        MAX_LEN   = len(self.message_utils.vocabulary)
        tokenizer = Tokenizer(MAX_LEN,lower=True)
        tokenizer.fit_on_texts(df['texto-lstm'].values)
        X = tokenizer.texts_to_sequences(df['texto-lstm'].values)
        self.X = pad_sequences(X, maxlen=MAX_LEN)
        self.Y = pd.get_dummies(df['classe']).values
        

        model = Sequential()
        model.add(Embedding(MAX_LEN, 32, input_length=self.X.shape[1]))
        model.add(LSTM(16))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.Y.shape[1], activation='softmax'))
        #model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[tf.metrics.Recall()])
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

        return model

    def __train(self):
        self.model.fit(self.X,
                       self.Y, epochs=13, batch_size=1,verbose=1)
    def get_model(self):
        return self.model

    def print_model(self):
        print(self.get_model().summary())

    def eval_model(self):
        print("Evaluate on train data")
        results = self.model.evaluate(
            self.X, self.Y, batch_size=1)
        print("test loss, test acc:", results)

    def __intent_prediction(self, user_message):
        #print(">>> Normalized and Clean user_message: {}.".format(self.message_utils.full_clean_text(user_message)))
        user_message_bag = self.message_utils.bag_for_message(user_message)

        response_prediction = self.model.predict(
            np.array([user_message_bag]), verbose=0)[0]

        # print(response_prediction)

        results = [[index, response] for index, response in enumerate(
            response_prediction) if response > self.PROB_SAFE_VALUE]
        # print(results)
        # verifica nas previsões se não há 1 na lista, se não há envia a resposta padrão (anything_else)
        # ou se não corresponde a margem de erro

        if "1" not in str(user_message_bag) or len(results) == 0:
            results = [[0, response_prediction[0]]]

        results.sort(key=lambda x: x[1], reverse=True)
        #print([{"intent": self.message_utils.classes[r[0]], "probability": str(r[1])} for r in results])
        return [{"intent": self.message_utils.classes[r[0]], "probability": str(r[1])} for r in results]

    def get_reply(self, user_message):
        most_prob_intent = self.__intent_prediction(
            user_message)[0]['intent']  # a classe mais provável
        # lista de intenções
        list_of_intents = self.message_utils.corpus['intents']

        for idx in list_of_intents:
            if idx['tag'] == most_prob_intent:
                result = random.choice(idx['responses'])
                break

        return result, most_prob_intent

    def get_predict(self, user_message):
        # a classe mais provável
        return self.__intent_prediction(user_message)[0]['intent']



def main():
    database = {
        "intents": [
            {
                "tag": "welcome",
                "patterns": [],
                "responses": ["Olá, serei seu assistente virtual, em que posso te ajudar?","Salve, qual foi ?", "Manda pro pai, Lança a braba", "No que posso te ajudar ?"],
                "context": [""]
            },
            {
                "tag": "myclasses",
                "patterns": [],
                "responses": ["Entendi, você deseja saber suas salas","Você deseja saber suas salas ?", "Ah, você quer saber qual sala ? ", "Suas Aulas ?"],
                "context": [""]
            },
            {
                "tag": "businfo",
                "patterns": [],
                "responses": ["Esses são os horários dos fretados","Horarios dos fretados: ", "Ah, você quer saber o horário dos fretados"],
                "context": [""]
            },
            {
                "tag": "discinfo",
                "patterns": [],
                "responses": ['Informações da disciplina X','Para a disciplina Y, as informações são as seguintes: '],
                "context": [""]
            },
            {
                "tag": "ru",
                "patterns": [],
                "responses": ['O cárdapio de hoje é esse:','Para o almoço temos:', 'Para o jantar teremos:'], # provisório
                "context": [""]
            },
            {
                "tag": "anything_else",
                "patterns": [],
                "responses": ["Desculpa, não entendi o que você falou, tente novamente!","Não compreendi a sua solicitação, talvez eu possa te ajudar", "Por favor, digite novamente"],
                "context": [""]
            }
        ]
        }


    database = gerador.fill_database(database,50)
    # demo da funcionalide da classe utils para mensagem
    message_utils = MessageUtils()
    message_utils.process_training_data(database,None)

    tatu_zap = TatuIA("", message_utils=message_utils,lstm=False)
  
    #tatu_zap.print_model()

    #tatu_zap.eval_model()
    
    turmas_por_ra_collection = get_db[DBCollections.TURMAS_POR_RA]

    def turmas(RA):
        QUERY = {"RA": str(RA)}
        result = list(turmas_por_ra_collection.find(QUERY))
        lista = result[0]["TURMAS"]
        for res in lista:del res['_id']
        lista_clean = [dict(item) for item in {tuple(dict.items()) for dict in lista}]
        for disciplina in lista_clean:
            teoria = disciplina['HORÁRIO TEORIA']
            pratica = disciplina['HORÁRIO PRÁTICA']
            nome = disciplina['DISCIPLINA - TURMA']

            if teoria == 0:
                print('Disciplina: {}, Horário Prática: {}'.format(nome,pratica)) 
            if pratica == 0:
                print('Disciplina: {}, Horário Teoria: {}'.format(nome,teoria)) 
        return lista_clean



    print(">>> Demo da funcionalidade de reconhecimento de intenção do TatuBot.")
    print(">>> Inicialmente a I.A foi treinada com cinco intenções (welcome,myclasses,businfo,discinfo,ru).")
    print(">>> Envie uma mensagem para o TatuBot!")
    while True:
        try:
            user_message = input("user: ")
            response, intent = tatu_zap.get_reply(user_message)
            if intent == "myclasses":
                user_ra = tatu_zap.message_utils.is_ra(user_message)
                if user_ra:
                    turmas(user_ra)
                else:
                    while True:
                        print("Tatu: Você solicitou informações sobre suas turmas, agora insira seu ra!")
                        expected_ra = input('user: ')
                        user_ra = tatu_zap.message_utils.is_ra(expected_ra)
                        if user_ra:
                            #print("Tatu: Já estou processando as turmas para o ra {}.".format(user_ra))
                            turmas(user_ra)
                            break
            elif intent == "businfo":
                user_localtime =  tatu_zap.message_utils.check_origin(user_message)
                while True:
                    if user_localtime:
                        print("Tatu: Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
                        break
                    else :
                        print("Tatu: Por favor, para conseguirmos identificar qual fretado você quer, diga de onde você quer ir (de SA / de SBC) para onde (para SA/ para SBC)")
                        expected_local = input('user: ')
                        user_localtime =  tatu_zap.message_utils.check_origin(expected_local)
                        
            elif intent == "discinfo": #TODO
                print("Tatu: Digite apenas o nome da matéria (ou sigla) que você deseja! ")
                expected_disc = input()
                print("Tatu: Estou buscando a ementa da disciplina {}.".format(expected_disc))

            else:
                print("Tatu: {}.".format(response)) 

        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()

