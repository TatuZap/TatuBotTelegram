import telebot
import os
import re
import json
import unidecode
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
        convert = [ w[0] for w in mensagem.text.lower().split() if w not in STOPWORDS]
        apelido_matéria = ''.join(convert)
        response, intent = tatuia.tatu_zap.get_reply('ementa ' + apelido_matéria)
        mensagem.text = apelido_matéria
    elif (loopFRET):
        response, intent = tatuia.tatu_zap.get_reply('fretados ' + mensagem.text)
    else:
        response, intent = tatuia.tatu_zap.get_reply(mensagem.text)

    #após classificar as mensagens em response (respota padrão do bot) e intent (intenção desejada da mensagem), adota comportamento diferente para cada intent
    
    if intent == "myclasses": #intent myclasses, para conseguir as salas/professores/horarios por RA
            user_ra = tatuia.tatu_zap.message_utils.is_ra(mensagem.text)
            if user_ra:
                texto += tatuia.turmas(user_ra)
                bot.send_message(mensagem.chat.id, texto)
                loopRA = False
            else:
                bot.send_message(mensagem.chat.id, "Você solicitou informações sobre suas turmas, agora insira seu ra!")
                loopRA = True

    elif intent == "businfo": #intent businfo, para conseguir informações sobre fretado
        user_localtime =  tatuia.tatu_zap.message_utils.check_origin(mensagem.text) #captura origem/destino dentro da mensagem
        if user_localtime:
            loopFRET = False
            response = list(fretado_model.next_bus(user_localtime[0], user_localtime[1], user_localtime[2]))
            print('response: ', response)
            #response = dumps(response)
            #bot.send_message(mensagem.chat.id, "Já estou buscando o horário de partida do próximo fretado que sai de {} para {} as {}".format(user_localtime[0], user_localtime[1], user_localtime[2]))
            saida = response[1]
            resposta = "Linha: {}, Horario_partida: {}".format(saida['linha'],saida['hora_partida'])
            bot.send_message(mensagem.chat.id, resposta)
            
        else :
            resposta ="Por favor, para conseguirmos identificar qual fretado você quer, diga de onde você quer ir (de SA / de SBC) para onde (para SA/ para SBC)"
            bot.send_message(mensagem.chat.id, resposta)
            loopFRET = True
            #     expected_local = input('user: ')
            #     user_localtime =  tatuia.tatu_zap.message_utils.check_origin(expected_local)
                    
    elif intent == "discinfo": #intent discinfo, para informações (plano de ensino) das disciplinas
        #(lambda x: "".join()
        msg = unidecode.unidecode(mensagem.text).lower() #limpa caracteres especiais da mensagem e coloca em lower
        search_nome_disc = re.search(r'(ementa|informacoes|requisitos|bibliografia|(plano de ensino)|(plano ensino)).?(sobre|de)?(.*?)$',string=msg) # retorna None se não encontrou nada dentro do padrão
        if search_nome_disc:
            nova_mensagem = search_nome_disc.group(5) #separa a parte da mensagem qual o nome da disciplina 
    #         mensagem.text.lower().split('ementa ')[1]
            convert = [ w[0] for w in nova_mensagem.split() if w not in STOPWORDS] 
            apelido_matéria = ''.join(convert) #gera o apelido da matéria pedida
            print('apelido ', apelido_matéria)
            response = list(catalogo_model.find_by_apelido(apelido_matéria)) #retorna a lista de disciplina com tal apelido
            #response = list(catalogo_model.list_all())        
            print('response: ', response)
            keyboard = telebot.types.InlineKeyboardMarkup() #utilizado para gerar o menu em mensagens do telegram
            similar_discipline = ''
            for disc in response: 
                sim_nome = similar(nova_mensagem, disc['disciplina']) #similaridade entre o nome da disciplina com o encontrado no banco 
                #sim_apelido = similar(nova_mensagem, disc['apelido'])
                print('similarity ', sim_nome)
                if sim_nome > 0.6:
                    similar_discipline = disc
                #if sim_apelido > 0.8:
                #    similar_discipline = disc
                keyboard.row(telebot.types.InlineKeyboardButton(disc['disciplina'], callback_data=disc['sigla']))
                print(disc['disciplina'] + ' ' + disc['sigla'] ) #insere no menu cada disciplina presenta na lista, gerando um callback com a sigla da disciplina (para diferenciar)


            resposta = 'Selecione qual o nome da disciplina desejada'
            if similar_discipline == '':
                bot.send_message(mensagem.chat.id, resposta, reply_markup=keyboard)
            else:
                resposta = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(similar_discipline['disciplina'],similar_discipline['TPI'],similar_discipline['sigla'],similar_discipline['recomendacoes'],similar_discipline['ementa'])
                bot.send_message(mensagem.chat.id, resposta)
        else : 
            resposta ="Por favor, para conseguirmos identificar de qual disciplina você quer o plano de ensino, diga o nome dela."
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

#lida com callback (como o utilizado no menu no discinfo)
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
        userMessage = call.data
        saida = list(catalogo_model.find_by_sigla(userMessage))[0]
        print('saida: ',saida)
        texto = "Disciplina: {}, TPI: {}, Sigla: {},\nRecomendacoes: {},\nEmenta: {}".format(saida['disciplina'],saida['TPI'],saida['sigla'],saida['recomendacoes'],saida['ementa'])
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto)

bot.polling()
