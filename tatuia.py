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
import unidecode
import re

import src.connection.database as database
import src.connection.fretados_model as fretado_model
import src.connection.catalogo_model as catalogo_model
import src.connection.restaurante_model as restaurante_model
import src.connection.usuario_model as usuario_model

from datetime import datetime 


from unittest import result

from src.load.DB import get_db,DBCollections

from difflib import SequenceMatcher

from nltk.corpus import stopwords

STOPWORDS = stopwords.words('portuguese')

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




database = {
    "intents": [
        {
            "tag": "welcome",
            "patterns": [],
            "responses": ["Olá, serei seu assistente virtual, em que posso te ajudar?","Olá, o que você gostaria de saber?","Olá, sobre o que você gostaria de saber?","Oi, diga para mim o que você quer saber", "Oi, diga no que posso te ajudar",
           "Olá, diz pra mim, o que você gostaria de saber?", "Sou seu assistente virtual, o que você gostaria de saber?", "Serei seu assistente virtual, diga pra mim o que deseja",
           "O que você gostaria de saber?","No que posso te ajudar?"],
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
            "responses": ["Desculpe, não entendi o que você falou, tente novamente!","Me desculpe, digite novamente o que deseja","Desculpe! Não entendi o que você quis dizer","Sinto muito, não entendi a sua solicitação, tente novamente",
                "Não compreendi a sua solicitação, talvez eu possa te ajudar","Não entendi a sua solicitação, digite novamente","Não consegui entender o que você digitou, tente novamente",
                "Por favor, digite novamente o que deseja","Por favor, digite novamente!","Peço, por gentileza, que digite novamente"],
            "context": [""]
        }
    ]
    }


database = gerador.fill_database(database,500)
# demo da funcionalide da classe utils para mensagem
message_utils = MessageUtils()
message_utils.process_training_data(database,None)

tatu_zap = TatuIA("", message_utils=message_utils,lstm=False)

#tatu_zap.print_model()

#tatu_zap.eval_model()

turmas_por_ra_collection = get_db[DBCollections.TURMAS_POR_RA]

def turmas(RA):
    """
    Retorna as turmas (no formato de string a ser exibido) para determinado RA, caso o encontre
    """
    QUERY = {"RA": str(RA)}
    string = ""
    result = list(turmas_por_ra_collection.find(QUERY))
    if result == []: return 'RA não encontrado, tente novamente'
    lista = result[0]["TURMAS"]
    for res in lista:del res['_id']
    lista_clean = [dict(item) for item in {tuple(dict.items()) for dict in lista}]
    for disciplina in lista_clean:
        teoria = disciplina['HORÁRIO TEORIA']
        pratica = disciplina['HORÁRIO PRÁTICA']
        nome = disciplina['DISCIPLINA - TURMA']

        if teoria == 0:
            string += 'Disciplina: {}, Horário Prática: {}\n'.format(nome,pratica) #print('Disciplina: {}, Horário Prática: {}'.format(nome,pratica)) 
        if pratica == 0:
            string += 'Disciplina: {}, Horário Teoria: {}\n'.format(nome,teoria) #print('Disciplina: {}, Horário Teoria: {}'.format(nome,teoria)) 
    return string

def extract_ra(message):
    """
    Retorna o RA extraido de uma string.
    """
    return message_utils.is_ra(message)

def extract_origem_destino(message):
    """
    Retorna uma lista com origem, destino, horário atual, horário limite (+1h) e dia da semana
    """
    return message_utils.check_origin(message)

def get_fretado(message):
    """
    Retorna o próximo fretado (formatado para uma String 'Linha e Horário de Partida') para origem, destino, horário atual,horário limite (+1h) e dia da semana. 
    """
    user_localtime = extract_origem_destino(message)
    response = list(fretado_model.next_bus(user_localtime[0], user_localtime[1], user_localtime[2],user_localtime[3],user_localtime[4]))
    return "Linha: {}, Horario_partida: {}".format(response[0]['linha'],response[0]['hora_partida']) if response else None

def extract_nome_disciplina(message):
    """
    Retorna a extração do nome de disciplinas de uma string, necessario utilizar .group(5) para acessar o nome 
    """
    msg = unidecode.unidecode(message).lower() #limpa caracteres especiais da mensagem e coloca em lower
    return re.search(r'(ementa|informacoes|requisitos|bibliografia|(plano de ensino)|(plano ensino)).?(sobre|de)?(.*?)$',string=msg) # retorna None se não encontrou nada dentro do padrão

def get_disciplinas(message):
    """
    Retorna a lista de disciplinas similares ao nome encontrado na string 
    """
    search_nome_disc = extract_nome_disciplina(message)
    nova_mensagem = search_nome_disc.group(5) #separa a parte da mensagem qual o nome da disciplina 
    #         mensagem.text.lower().split('ementa ')[1]
    apelido_matéria = ''.join([ w[0] for w in nova_mensagem.split() if w not in STOPWORDS]) #gera o apelido da matéria pedida
    print('apelido ', apelido_matéria)
    return list(catalogo_model.find_by_apelido(apelido_matéria)) #retorna a lista de disciplina com tal apelido

def get_disciplina_selecionada(message):
    """
    Retorna a string formatada para a disciplina mais próxima (similaridade de texto) ao nome extraido da string 
    """
    lista_disc = get_disciplinas(message)
    nova_mensagem = extract_nome_disciplina(message).group(5)
    print('nome ', nova_mensagem)
    similar_discipline = None
    for disc in lista_disc:
        sim_nome = SequenceMatcher(None, nova_mensagem, disc['disciplina']).ratio() #similaridade entre o nome da disciplina com o encontrado no banco 
        #sim_apelido = similar(nova_mensagem, disc['apelido'])
        print('similarity ', sim_nome)
        if sim_nome > 0.6:
            similar_discipline = disc
        #if sim_apelido > 0.8:
        #    similar_discipline = disc
        print(disc['disciplina'] + ' ' + disc['sigla'] )
    texto_saida = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(similar_discipline['disciplina'],similar_discipline['TPI'],similar_discipline['sigla'],similar_discipline['recomendacoes'],similar_discipline['ementa']) if similar_discipline else None
    print(texto_saida)
    return texto_saida

def get_ru_hoje(message):
    """
    Retorna as informações para o cardápio do RU para o dia de hoje
    """
    tipo = 0
    saida = list(restaurante_model.find_by_weekday_num(datetime.now().weekday(),tipo))[0]
    if saida:
        jantar = re.findall(r"jantar|noite", message)
        almoço = re.findall(r"almoço|manha", message)
        if jantar:
            resposta = "Jantar:{}\nSalada: {}\nSobremesa: {}".format(saida['jantar'],saida['saladas'],saida['sobremesas'])
        elif almoço:
            resposta = "Almoço:{}\nSalada: {}\nSobremesa: {}".format(saida['almoço'],saida['saladas'],saida['sobremesas'])
        else:
            resposta = "Almoço:{}\nJanta:{}\nSalada: {}\nSobremesa: {}".format(saida['almoço'],saida['jantar'],saida['saladas'],saida['sobremesas'])
    else: resposta = 'Falha na recuperação do cardápio'
    return resposta

# print(">>> Demo da funcionalidade de reconhecimento de intenção do TatuBot.")
# print(">>> Inicialmente a I.A foi treinada com cinco intenções (welcome,myclasses,businfo,discinfo,ru).")
# print(">>> Envie uma mensagem para o TatuBot!")
# while True:
#     try:
#         user_message = input("user: ")
#         response, intent = tatu_zap.get_reply(user_message)
#         if intent == "myclasses":
#             user_ra = tatu_zap.message_utils.is_ra(user_message)
#             if user_ra:
#                 turmas(user_ra)
#             else:
#                 while True:
#                     print("Tatu: Você solicitou informações sobre suas turmas, agora insira seu ra!")
#                     expected_ra = input('user: ')
#                     user_ra = tatu_zap.message_utils.is_ra(expected_ra)
#                     if user_ra:
#                         #print("Tatu: Já estou processando as turmas para o ra {}.".format(user_ra))
#                         turmas(user_ra)
#                         break
#         elif intent == "businfo":
#             user_localtime =  tatu_zap.message_utils.check_origin(user_message)
#             while True:
#                 if user_localtime:
#                     print("Tatu: Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
#                     break
#                 else :
#                     print("Tatu: Por favor, para conseguirmos identificar qual fretado você quer, diga de onde você quer ir (de SA / de SBC) para onde (para SA/ para SBC)")
#                     expected_local = input('user: ')
#                     user_localtime =  tatu_zap.message_utils.check_origin(expected_local)
                    
#         elif intent == "discinfo": #TODO
#             print("Tatu: Digite apenas o nome da matéria (ou sigla) que você deseja! ")
#             expected_disc = input()
#             print("Tatu: Estou buscando a ementa da disciplina {}.".format(expected_disc))

#         else:
#             print("Tatu: {}.".format(response)) 

#     except KeyboardInterrupt:
#         break



# if __name__ == "__main__":
#     main()

