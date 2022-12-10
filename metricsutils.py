from tatuia import TatuIA
from messageutils import MessageUtils # nossa classe de pré-processamento
from sklearn.metrics import classification_report

#import seaborn as sn
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import geradorfrases as gerador


def main():
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
            "responses": [],
            "context": [""]
        },
        {
            "tag": "businfo",
            "patterns": [],
            "responses": [],
            "context": [""]
        },
        {
            "tag": "discinfo",
            "patterns": [],
            "responses": [],
            "context": [""]
        },
        {
            "tag": "ru",
            "patterns": [],
            "responses": [],
            "context": [""]
        },
        {
            "tag": "contadorferias",
            "patterns": [],
            "responses": ['final quadri'],
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
    n = 100
    database = gerador.fill_database(database,3*n)
    #print(database)
    message_utils = MessageUtils()
    message_utils.process_training_data(database,None)


    tatu_zap = TatuIA("", message_utils=message_utils,lstm = False)
    tatu_zap.print_model()
    #tatu_zap.eval_model()

    db_test = gerador.fill_treino(database,n)
    X = []
    for a in db_test['intents']:
        if a['tag'] != 'anything_else': X += a['patterns'][0:n]
    X = X + gerador.gerar_anything(n)

    Y = ['welcome']*n+['myclasses']*n+['businfo']*n+['discinfo']*n+['ru']*n+['contadorferias']*n+['anything_else']*n


    list_predict = [(tatu_zap.get_predict(i)) for i in X]


    y_true = pd.Series(Y, name='Row_True')
    y_pred = pd.Series(list_predict, name='Col_Pred')
    df_confusion = pd.crosstab(y_true, y_pred)
    #df_confusion = pd.crosstab(y_pred, y_true,margins = 'True')
    print('matriz confusao::')
    print(df_confusion)
    print(classification_report(Y, list_predict))

if __name__ == "__main__":
    main()
