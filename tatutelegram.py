import telebot
import os
import json
import tatuia
import sys 
import src.load.fretados_model as fretado_model
import src.load.catalogo_model as catalogo_model
# from bson.json_util import dumps, loads
from dotenv import load_dotenv
sys.stdout.flush()
load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local 
CHAVE_API = os.getenv("BOT_API")

print("TatuZap is working!")
bot = telebot.TeleBot(CHAVE_API)

@bot.message_handler(commands=["start"])
def pizza(mensagem):
    bot.send_message(mensagem.chat.id, "Bem-Vindo ao TatuZapper")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    print("Aqui está a mensagem",mensagem)
    texto = ""
    response, intent = tatuia.tatu_zap.get_reply(mensagem.text)

    if intent == "myclasses":
            user_ra = tatuia.tatu_zap.message_utils.is_ra(mensagem.text)
            if user_ra:
                texto += tatuia.turmas(user_ra)
                bot.send_message(mensagem.chat.id, texto)
            else:
                bot.send_message(mensagem.chat.id, "Você solicitou informações sobre suas turmas, agora insira seu ra!")
                #expected_ra = input('user: ')
                # user_ra = tatuia.tatu_zap.message_utils.is_ra(expected_ra)
                # if user_ra:
                #     #print("Tatu: Já estou processando as turmas para o ra {}.".format(user_ra))
                #     tatuia.turmas(user_ra)
                #     break
    elif intent == "businfo":
        user_localtime =  tatuia.tatu_zap.message_utils.check_origin(mensagem.text)
        if user_localtime:
            response = list(fretado_model.next_bus(user_localtime[0], user_localtime[1], user_localtime[2]))
            print('response: ', response)
            #response = dumps(response)
            #bot.send_message(mensagem.chat.id, "Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
            saida = response[1]
            resposta = "Linha: {}, Horario_partida: {}".format(saida['linha'],saida['hora_partida'])
            bot.send_message(mensagem.chat.id, resposta)
            
            # else :
            #     print("Tatu: Por favor, para conseguirmos identificar qual fretado você quer, diga de onde você quer ir (de SA / de SBC) para onde (para SA/ para SBC)")
            #     expected_local = input('user: ')
            #     user_localtime =  tatuia.tatu_zap.message_utils.check_origin(expected_local)
                    
    elif intent == "discinfo": #TODO
        apelido_matéria =  'MCZA031-13'
        response = list(catalogo_model.find_by_sigla(apelido_matéria))
        #response = list(catalogo_model.list_all())
        print('response: ', response)
        saida = response[0]
        resposta = "Disciplina: {}, TPI: {}, sigla: {}, recomendacoes: {}".format(saida['disciplina'],saida['TPI'],saida['sigla'],saida['recomendacoes'])
        #response = dumps(response)
        #bot.send_message(mensagem.chat.id, "Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
        bot.send_message(mensagem.chat.id, resposta)


    else:
        bot.reply_to(mensagem, response)

    
    
    #bot.reply_to(mensagem, texto)

bot.polling()