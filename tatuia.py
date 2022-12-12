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

import src.database as database
import src.fretados.fretados_model as fretados_model
import src.catalogo.catalogo_model as catalogo_model
import src.restaurante.restaurante_model as restaurante_model
import src.usuario.usuario_model as usuario_model
import src.calendario.calendario_model as calendario_model
import src.turmas.turmas_model as turmas_model

from datetime import datetime


from unittest import result


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
        #self.__train()
        self.__load_model()
        self.PROB_SAFE_VALUE = 0.25

    def __load_model(self):
        current_filepath = os.getcwd()
        model_folder = "modelbot"
        complete_path = os.path.join(current_filepath, model_folder)
        if os.path.exists(complete_path):
            print(">>> Carregando o TatuBot do Disco")
            self.model = tf.keras.models.load_model(complete_path + "/model")
            print(">>> Fim do Carregando o TatuBot do Disco")
        else:
            print(">>> Build do TatuBot")
            if self.model:
                self.__train()
            else:
                self.model = self.__simple_ann()
                self.__train()
            os.mkdir(complete_path)
            self.model.save(complete_path + "/model")
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
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

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

        if most_prob_intent == 'myclasses':
            result = get_turmas(user_message)
        elif most_prob_intent == 'businfo':
            fretado = get_fretado(user_message)
            result = fretado if fretado else 'Não encontrei um fretado adequado'
        elif most_prob_intent == 'discinfo':
            disc = get_disciplina_selecionada(user_message)
            result = disc if disc else 'Não encontrei a disciplina selecionada'
        elif most_prob_intent == 'ru':
            result = get_ru(unidecode.unidecode(user_message).lower())
        elif most_prob_intent == 'contadorferias':
            result = calendario_model.contador_calendario()
        print('result: ',result)
        return result, most_prob_intent

    def get_predict(self, user_message):
        # a classe mais provável
        return self.__intent_prediction(user_message)[0]['intent']





#tatu_zap.print_model()

#tatu_zap.eval_model()



def get_turmas(mensagem):
    """
    Retorna as turmas (no formato de string a ser exibido) para determinado RA, caso o encontre
    """
    string = ""
    result = get_materias(mensagem)
    if not result : return 'RA não encontrado, por favor digite seu RA'
    lista_clean = result

    for disciplina in lista_clean:
        teoria = disciplina['horário_teoria']
        pratica = disciplina['horário_pratica']
        nome = disciplina['Disciplina']

        if teoria == ' ':
            string += '***{} ***\nHorário Prática: {}\n\n'.format(nome,pratica) #print('Disciplina: {}, Horário Prática: {}'.format(nome,pratica)) tempo
        elif pratica == ' ':
            string += '***{} ***\nHorário Teoria: {}\n\n'.format(nome,teoria) #print('Disciplina: {}, Horário Teoria: {}'.format(nome,teoria))
        else:
            string += '***{} ***\nHorário Teoria: {}\nHorário Prática: {}\n\n'.format(nome,teoria,pratica)

    return string

def getRA_byID(ID):
    ra = usuario_model.find_by_id(ID)
    return ra if ra else -1

def setRA_byID(message,ID):
    ra = extract_ra(message)
    if ra:
        if usuario_model.find_by_id(ID):
            usuario_model.find_and_update(ID,ra)
        else: usuario_model.insert_id_ra(ID,ra)
    return 'ra:{} id:{}'.format(ra,ID)

def get_materias(message):
    ra = extract_ra(message)
    dia_semana = extract_dia_semana(message)
    tempo = extract_tempo(message)
    if ra:
        # turmas_model.next_aula(horario,dia) #horario do dateTime
        # turmas_model.now_aula(horario,dia)
        if dia_semana:
            return turmas_model.find_turmas_by_ra(ra,dia_semana)
        # if tempo:
        #     if tempo == 'agora':
        #         return turmas_model.now_aula(ra,tempo)
        #     if tempo == 'proxima':
        #         return turmas_model.next_aula(ra,tempo)
        #     if tempo == 'hoje':
        #         hoje = datetime.now().weekday()
        #         return turmas_model.get_materias(ra,hoje)
        #     if tempo == 'amanha':
        #         amh = datetime.now().weekday()+1
        #         return turmas_model.get_materias(ra,amh)

        else:
            return turmas_model.find_turmas_by_ra(ra)
    else: return None

def extract_ra(message):
    """
    Retorna o RA extraido de uma string.
    """
    return message_utils.is_ra(message)

def extract_dia_semana(message):
    a = re.findall('segunda|terça|quarta|quinta|sexta|sabado', message)
    return convert_dia(a[0]) if a != [] else None

def extract_tempo(message):
    a = re.findall('agora|proxima|hoje|amanha', message)
    return a



def convert_dia(message):
    lista = list(enumerate(["segunda","terça","quarta","quinta","sexta","sabado"]))
    for i in lista:
        if i[1] == message:
            return i[0]
    return -1

def extract_origem_destino(message):
    """
    Retorna uma lista com origem, destino, horário atual, horário limite (+1h) e dia da semana
    """
    return message_utils.check_origin(unidecode.unidecode(message).lower())

def get_fretado(message):
    """
    Retorna o próximo fretado (formatado para uma String 'Linha e Horário de Partida') para origem, destino, horário atual,horário limite (+1h) e dia da semana.
    """
    user_localtime = extract_origem_destino(message)
    explicacao = 'Essa são as linhas de fretado disponíveis para o horário:\n\n'
    if not user_localtime :
        possibilides = ["DE SA PARA SBC:", "DE SBC PARA SA:", "DE SBC PARA SBC:", "DE TERMINAL SBC PARA SBC:","DE SBC PARA TERMINAL SBC:",'DE SA PRO TERMINAL']
        saida = explicacao

        for i in possibilides:
            user_localtime = extract_origem_destino(i)
            if user_localtime:
                response = list(fretados_model.next_bus(user_localtime[0], user_localtime[1], user_localtime[2],user_localtime[3],user_localtime[4]))
                aux = '***{}***'.format(i) + "\nLinha: {}, Horário_partida: {}\n\n".format(response[0]['linha'],response[0]['hora_partida']) if response else '***{}***'.format(i)+'\n'+"Não existem fretados dentro de uma hora para essa opção.\n\n"
                saida += aux
        return saida.replace('_',' ')
    response = list(fretados_model.next_bus(user_localtime[0], user_localtime[1], user_localtime[2],user_localtime[3],user_localtime[4]))

    return ("{}Linha: {}, Horario_partida: {}".format(explicacao,response[0]['linha'],response[0]['hora_partida'])).replace('_',' ') if response else None


def extract_nome_disciplina(message):
    """
    Retorna a extração do nome de disciplinas de uma string, necessario utilizar .group(5) para acessar o nome
    """
    msg = unidecode.unidecode(message).lower() #limpa caracteres especiais da mensagem e coloca em lower
    return re.search(r'(ementa|informacoes|requisitos|bibliografia|(plano de ensino)|(plano ensino)).?(sobre.|de.)?(.*)$',string=msg) # retorna None se não encontrou nada dentro do padrão

def get_disciplinas(message):
    """
    Retorna a lista de disciplinas similares ao nome encontrado na string
    """
    search_nome_disc = extract_nome_disciplina(message)
    print('nome: ',search_nome_disc)
    nome_disc = search_nome_disc.group(5) #separa a parte da mensagem qual o nome da disciplina
    #         mensagem.text.lower().split('ementa ')[1]
    if len (nome_disc) < 6:
        apelido_matéria = nome_disc
    else: apelido_matéria = ''.join([ w[0] for w in nome_disc.split() if w not in STOPWORDS]) #gera o apelido da matéria pedida
    print('apelido ', apelido_matéria)
    return list(catalogo_model.find_by_apelido(apelido_matéria)) #retorna a lista de disciplina com tal apelido


def get_disciplina_selecionada(message):
    """
    Retorna a string formatada para a disciplina mais próxima (similaridade de texto) ao nome extraido da string
    """
    tmp = extract_nome_disciplina(message)
    if tmp:
        nome_disc = tmp.group(5)
    else: return 'Não entendi sua solicitação'
    print('nome:', nome_disc)
    similar_discipline = None
    nome_disc = nome_disc.replace(' ','')
    if len(nome_disc) < 6 : #se menor que 6 testa para siglas
        lista_apelido = list(catalogo_model.find_by_apelido(nome_disc)) #retorna a lista de disciplina com tal apelido
        if lista_apelido:
            return 'Selecionar na lista'
    else:
        lista_disc = get_disciplinas(message)
        if nome_disc == '': return None
        for disc in lista_disc:
            sim_nome = SequenceMatcher(None, nome_disc, disc['disciplina']).ratio() #similaridade entre o nome da disciplina com o encontrado no banco
            #sim_apelido = similar(nome_disc, disc['apelido'])
            print('similarity ', sim_nome)
            if sim_nome > 0.6:
                similar_discipline = disc
            #if sim_apelido > 0.8:
            #    similar_discipline = disc
            print(disc['disciplina'] + ' ' + disc['sigla'] )

    texto_disciplina = "***{}***\n\nTPI: {}    Sigla: {}\n\nRecomendacoes: {}\n\nEmenta: {}".format(similar_discipline['disciplina'],similar_discipline['TPI'],similar_discipline['sigla'],similar_discipline['recomendacoes'],similar_discipline['ementa']) if similar_discipline else None
    print('texto_saida:',texto_disciplina)
    texto_saida = texto_disciplina if similar_discipline else 'Selecionar na lista'
    return texto_saida

def get_disciplina_codigo(message):
    similar_discipline = list(catalogo_model.find_by_sigla(message))[0]
    texto_disciplina = "***{}***\n\nTPI: {}    Sigla: {}\n\nRecomendacoes: {}\n\nEmenta: {}".format(similar_discipline['disciplina'],similar_discipline['TPI'],similar_discipline['sigla'],similar_discipline['recomendacoes'],similar_discipline['ementa']) if similar_discipline else None
    print(texto_disciplina)
    texto_saida = texto_disciplina if similar_discipline else 'Selecionar na lista'
    return texto_saida

def get_ru(message):
    """
    Retorna as informações para o cardápio do RU para o dia de hoje
    """
    tipo = 0
    dia = extract_dia_semana(message)
    cardapio = list(restaurante_model.find_by_weekday_num(datetime.now().weekday(),tipo)) if not dia        else list(restaurante_model.find_by_weekday_num(dia,tipo))
    print('cardapio:',cardapio)
    if len(cardapio) == 0 : return 'O Restaurante Universitário não funciona nesse dia.'
    saida = cardapio[0] if cardapio != [] else None
    print('saida jantar:',saida['jantar'])
    if saida:
        if saida['almoço'] == saida['saladas']:
            print('vazio')
            return saida['sobremesas'].split('ru são bernardo fechado.')[0]+'\nru são bernardo fechado.'+saida['sobremesas'].split('ru são bernardo fechado.')[1]
        jantar = re.findall(r"jantar|janta|noite", message)
        almoço = re.findall(r"almoco|manha", message)
        if jantar:
            resposta = "***Jantar*** {}\n\n***Salada***\n{}\n\n***Sobremesa***\n{}".format(split_pratoprincipal_opcao(saida['jantar']),saida['saladas'][1:],saida['sobremesas'][1:])
        elif almoço:
            resposta = "***Almoço*** {}\n\n***Salada***\n{}\n\n***Sobremesa***\n{}".format(split_pratoprincipal_opcao(saida['almoço']),saida['saladas'][1:],saida['sobremesas'][1:])
        else:
            resposta = "***Almoço***{}\n\n***Jantar***{}\n\n***Salada***\n{}\n\n***Sobremesa***\n{}".format(split_pratoprincipal_opcao(saida['almoço']),split_pratoprincipal_opcao(saida['jantar']),remove_spaces(saida['saladas']),remove_spaces(saida['sobremesas']))
    else: resposta = 'Falha na recuperação do cardápio'
    return resposta

def split_pratoprincipal_opcao(message):
    print(len(message))
    if len(message)<10 : return '\nNão possui essa refeição.'
    else:
        return '\nPrato Principal'+message.split('opção sem carne')[0].split(' prato principal')[1]+'\nOpção sem CARNE'+(message.split('opção sem carne')[1]).split('guarnição')[0] + '\nGuarnição'+(message.split('opção sem carne')[1]).split('guarnição')[1]

def remove_spaces(message):
    if len(message)<5 : return '\nNão possui essa opção.'
    return message[2:]

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
            "responses": ['disciplinas'],
            "context": [""]
        },
        {
            "tag": "businfo",
            "patterns": [],
            "responses": ['fretado'],
            "context": [""]
        },
        {
            "tag": "discinfo",
            "patterns": [],
            "responses": ['ementa'],
            "context": [""]
        },
        {
            "tag": "ru",
            "patterns": [],
            "responses": ['ru'],
            "context": [""]
        },
        {
            "tag": "contadorferias",
            "patterns": [],
            "responses": ['final'],
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



print("filling database")
database = gerador.fill_database(database,100)
fretados_model.populate_database()
catalogo_model.populate_database()
restaurante_model.populate_database()
# demo da funcionalide da classe utils para mensagem
message_utils = MessageUtils()
print("processing database data")
message_utils.process_training_data(database,None)

tatu_zap = TatuIA("", message_utils=message_utils,lstm=False)
