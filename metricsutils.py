from src.tatuia import TatuIA 
from messageutils import MessageUtils # nossa classe de pré-processamento
from sklearn.metrics import classification_report

#import seaborn as sn
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import geradorfrases as gerador


def main():
    # database = {
    #     "intents": [
    #             {
    #                 "tag": "welcome",
    #                 "patterns": ['oi','ola','boa tarde','bom dia','boa noite','saudações','fala','eae','salve'],
    #                 "responses": ["Olá, serei seu assistente virtual, em que posso te ajudar?","Salve, qual foi ?", "Manda pro pai, Lança a braba", "No que posso te ajudar ?"],
    #                 "context": [""]
    #             },
    #             {
    #                 "tag": "my_classes",
    #                 "patterns": ['materias', 'materia', 'sala', 'disciplina','professor','local','turma','turmas','professores','disciplinas','salas','aula','aulas','grade','horario','classe','classes','cadeira','cadeiras','sala de aula','local de estudo','disciplinas matriculadas'],
    #                 "responses": ["Entendi, você deseja saber suas salas","Você deseja saber suas salas ?", "Ah, você quer saber qual sala ? ", "Suas Aulas ?"],
    #                 "context": [""]
    #             },
    #             {
    #                 "tag": "bus_info",
    #                 "patterns": ['fretado','fretados','onibus','busao','lotação','coletivo','circular','transporte','carro','veículo'],
    #                 "responses": ["Fretados","Horarios Fretado"], #provisório
    #                 "context": [""]
    #             },
    #             {
    #                 "tag": "anything_else",
    #                 "patterns": [],
    #                 "responses": ["Desculpa, não entendi o que você falou, tente novamente!","Não compreendi a sua solicitação, talvez eu possa te ajudar"],
    #                 "context": [""]
    #             }
    #         ]
    #     }

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
    
    Y = ['welcome']*n+['myclasses']*n+['businfo']*n+['discinfo']*n+['ru']*n+['anything_else']*n

    
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
