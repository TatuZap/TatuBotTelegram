import telebot
import os
import json
import tatuia
import sys 
import src.load.fretados_model as fretado_model
import src.load.catalogo_model as catalogo_model

# from bson.json_util import dumps, loads
from dotenv import load_dotenv
from nltk.corpus import stopwords
from difflib import SequenceMatcher

def similar(a, b): return SequenceMatcher(None, a, b).ratio()

STOPWORDS = stopwords.words('portuguese')
sys.stdout.flush()

loopRA = False
loopDISC = False

load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local 
CHAVE_API = os.getenv("BOT_API")

print("TatuZap is working!")
bot = telebot.TeleBot(CHAVE_API)

msginicial = 'Bem-Vindo ao TatuBot.\n Nosso bot possui como funcionalidades informar quais as salas e horários das disciplinas em que você está matriculado, informações sobre ementa de disciplinas, qual o próximo horário e número do fretado, qual o cardápio do RU'



@bot.message_handler(commands=["start"])
def pizza(mensagem):
    bot.send_message(mensagem.chat.id, msginicial)

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    print("Aqui está a mensagem",mensagem)
    texto = ""
    global loopRA
    global loopDISC
    if (loopRA):
        response, intent = tatuia.tatu_zap.get_reply('materias ' + mensagem.text)
    elif (loopDISC):
        convert = [ w[0] for w in mensagem.text.lower().split() if w not in STOPWORDS]
        apelido_matéria = ''.join(convert)
        response, intent = tatuia.tatu_zap.get_reply('ementa ' + apelido_matéria)
        mensagem.text = apelido_matéria
    else:
        response, intent = tatuia.tatu_zap.get_reply(mensagem.text)
    if intent == "myclasses":
            user_ra = tatuia.tatu_zap.message_utils.is_ra(mensagem.text)
            if user_ra:
                texto += tatuia.turmas(user_ra)
                bot.send_message(mensagem.chat.id, texto)
                loopRA = False
            else:
                bot.send_message(mensagem.chat.id, "Você solicitou informações sobre suas turmas, agora insira seu ra!")
                loopRA = True
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
        #(lambda x: "".join()
        nova_mensagem = mensagem.text.lower().split('ementa ')[1]
        convert = [ w[0] for w in nova_mensagem.split() if w not in STOPWORDS]
        apelido_matéria = ''.join(convert) 
        print('apelido ', apelido_matéria)
        response = list(catalogo_model.find_by_apelido(apelido_matéria))
        #response = list(catalogo_model.list_all())        
        print('response: ', response)
        keyboard = telebot.types.InlineKeyboardMarkup()
        similar_discipline = ''
        for disc in response:
            sim = similar(nova_mensagem, disc['disciplina'])
            print('similarity ', sim)
            if sim > 0.6:
                similar_discipline = disc
            keyboard.row(telebot.types.InlineKeyboardButton(disc['disciplina'], callback_data=disc['sigla']))
            print(disc['disciplina'] + ' ' + disc['sigla'] )
        
        #saida = response[0]
        #resposta = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(saida['disciplina'],saida['TPI'],saida['sigla'],saida['recomendacoes'],saida['ementa'])
        #response = dumps(response)
        #bot.send_message(mensagem.chat.id, "Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
        resposta = 'Selecione qual o nome da disciplina desejada'
        if similar_discipline == '':
            bot.send_message(mensagem.chat.id, resposta, reply_markup=keyboard)
        else:
            resposta = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(similar_discipline['disciplina'],similar_discipline['TPI'],similar_discipline['sigla'],similar_discipline['recomendacoes'],similar_discipline['ementa'])
            bot.send_message(mensagem.chat.id, resposta)
    # elif intent == 'ru':
    #     keyboard = telebot.types.InlineKeyboardMarkup()
    #     keyboard.row(
    #         telebot.types.InlineKeyboardButton('vitor', callback_data='11201721679')
    #     )
    #     keyboard.row(
    #         telebot.types.InlineKeyboardButton('fabio', callback_data='11201722790'),
    #         telebot.types.InlineKeyboardButton('higor', callback_data='11201810691')
    #     )
    #     bot.send_message(mensagem.chat.id, 'Click on the currency of choice:', reply_markup=keyboard)
        


    else:
        bot.reply_to(mensagem, response)

    
    
    #bot.reply_to(mensagem, texto)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
        userMessage = call.data
        saida = list(catalogo_model.find_by_sigla(userMessage))[0]
        print('saida: ',saida)
        texto = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(saida['disciplina'],saida['TPI'],saida['sigla'],saida['recomendacoes'],saida['ementa'])
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto)

bot.polling()