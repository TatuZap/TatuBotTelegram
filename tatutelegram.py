import telebot
import os
import re
import json
import unidecode
import tatuia
import sys 
import src.connection.database as database
import src.connection.fretados_model as fretado_model
import src.connection.catalogo_model as catalogo_model
import src.connection.restaurante_model as restaurante_model
import src.connection.usuario_model as usuario_model

from datetime import datetime #FIXME

# from bson.json_util import dumps, loads
from dotenv import load_dotenv
from nltk.corpus import stopwords
#from difflib import SequenceMatcher

STOPWORDS = stopwords.words('portuguese')
sys.stdout.flush()

#(forma provisória) variaveis para controle de fluxo
loopRA = False
loopDISC = False
loopFRET = False

load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local 
CHAVE_API = os.getenv("BOT_API")

print("TatuZap is working!")
bot = telebot.TeleBot(CHAVE_API) #carrega o bot com a key

msginicial = 'Bem-Vindo ao TatuBot.\n Nosso bot possui como funcionalidades informar quais as salas e horários das disciplinas em que você está matriculado, informações sobre ementa de disciplinas (nome), qual o próximo horário e número do fretado, qual o cardápio do RU'

#msginicial = 'Olá, esse é o TatuZap. Aqui você pode ficar sabendo sobre a sua grade (turmas, salas e horários), cardápio do RU, fretados (horários de partida), disciplinas da UFABC, etc. Basta que você digite o que deseja.\n Alguns exemplos de uso:\n- Grade: quero saber as minhas turmas, ra 1234567891011\n- Cardápio RU: O que tem para o almoço/jantar?\n- Fretados: Qual o próximo fretado de SA para SBC?\n'



'''
    Função quando o usuário da um /start
'''
@bot.message_handler(commands=["start"])
def pizza(mensagem):
    bot.send_message(mensagem.chat.id, msginicial)

def verificar(mensagem):
    return True

'''
   Handler para todas as mensagens de usuários
'''
@bot.message_handler(func=verificar)
def responder(mensagem):
    print("Aqui está a mensagem",mensagem)
    texto = ""
    global loopRA
    global loopDISC
    global loopFRET

    #testa os casos em que a mensagem estaria dentro de um loop (uma requisição do bot)
    if (loopRA):
        response, intent = tatuia.tatu_zap.get_reply('materias ' + mensagem.text)
    elif (loopDISC):
        apelido_matéria = ''.join([ w[0] for w in mensagem.text.lower().split() if w not in STOPWORDS])
        response, intent = tatuia.tatu_zap.get_reply('ementa ' + apelido_matéria)
        mensagem.text = apelido_matéria
    elif (loopFRET):
        response, intent = tatuia.tatu_zap.get_reply('fretados ' + mensagem.text)
    else:
        response, intent = tatuia.tatu_zap.get_reply(mensagem.text) #recebe intent prevista com mensagem de resposta padrão para a intent

    #após classificar as mensagens em response (respota padrão do bot) e intent (intenção desejada da mensagem), adota comportamento diferente para cada intent
    
    if intent == "myclasses": #intent myclasses, para conseguir as salas/professores/horarios por RA
            user_ra = tatuia.extract_ra(mensagem.text) 
            if user_ra:
                bot.send_message(mensagem.chat.id, tatuia.turmas(user_ra))
                loopRA = False
            else: #se não extraiu um ra, pede para o usuario enviar um ra válido
                bot.send_message(mensagem.chat.id, "Você solicitou informações sobre suas turmas, agora insira seu ra!")
                loopRA = True

    elif intent == "businfo": #intent businfo, para conseguir informações sobre fretado
        user_localtime = tatuia.extract_origem_destino(mensagem.text) #captura origem/destino na mensagem
        if user_localtime:
            loopFRET = False
            response = tatuia.get_fretado(mensagem.text)
            print('response: ', response)            
            if response:
                bot.send_message(mensagem.chat.id, response)
            else: #response é None quando não há linhas de fretado disponível para a requisição
                bot.send_message(mensagem.chat.id, 'Não existem linhas de fretado disponíveis na próxima hora.')
            
        else : #se a mensagem não possui a origem nem o destino, pede para o usuário enviar essa informação
            resposta ="Por favor, para conseguirmos identificar qual fretado você quer, diga de onde você quer ir (de SA / de SBC) para onde (para SA/ para SBC)"
            bot.send_message(mensagem.chat.id, resposta)
            loopFRET = True
                    
    elif intent == "discinfo": #intent discinfo, para informações (plano de ensino) das disciplinas
        search_nome_disc = tatuia.extract_nome_disciplina(mensagem.text)
        if search_nome_disc:       
            response = tatuia.get_disciplinas(mensagem.text)
            print('response: ', response)
            keyboard = telebot.types.InlineKeyboardMarkup() #utilizado para gerar o menu em mensagens do telegram
            for disc in response: 
                keyboard.row(telebot.types.InlineKeyboardButton(disc['disciplina'], callback_data=disc['sigla']))#insere no menu cada disciplina presenta na lista, gerando um callback com a sigla da disciplina (para diferenciar)

            similar_discipline = tatuia.get_disciplina_selecionada(mensagem.text)
            if similar_discipline:
                bot.send_message(mensagem.chat.id,similar_discipline)
            else :
                bot.send_message(mensagem.chat.id, 'Selecione qual o nome da disciplina desejada', reply_markup=keyboard)

        else : 
            resposta ="Por favor, para conseguirmos identificar de qual disciplina você quer o plano de ensino, diga o nome dela."
            loopDISC = True
            bot.send_message(mensagem.chat.id, resposta)

    elif intent == 'ru':
        # #response = list(restaurante_model.list_all())
        bot.send_message(mensagem.chat.id,tatuia.get_ru_hoje(mensagem.text,0))


    else:
        bot.reply_to(mensagem, response)

    
    
    #bot.reply_to(mensagem, texto)

#lida com callback (como o utilizado no menu no discinfo)
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
        userMessage = call.data
        saida = list(catalogo_model.find_by_sigla(userMessage))[0]
        print('saida: ',saida)
        texto = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(saida['disciplina'],saida['TPI'],saida['sigla'],saida['recomendacoes'],saida['ementa'])
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto)

bot.polling()
