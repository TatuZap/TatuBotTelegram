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

from dotenv import load_dotenv
from nltk.corpus import stopwords


# from telebot import custom_filters
# from telebot.handler_backends import State, StatesGroup #States

# # States storage
# from telebot.storage import StateMemoryStorage


from telebot import types

sys.stdout.flush()

# # States group.
# class MyStates(StatesGroup):
#     # Just name variables differently
#     inicial = State()
#     ra = State() 
#     disc = State()
#     fret = State()


# # Now, you can pass storage to bot.
# state_storage = StateMemoryStorage() # you can init here another storage

load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local 
CHAVE_API = os.getenv("BOT_API")

print("TatuZap is working!")
bot = telebot.TeleBot(CHAVE_API) #carrega o bot com a key

#msginicial = 'Bem-Vindo ao TatuBot.\n Nosso bot possui como funcionalidades informar quais as salas e horários das disciplinas em que você está matriculado, informações sobre ementa de disciplinas (nome), qual o próximo horário e número do fretado, qual o cardápio do RU'

msginicial = 'Olá, esse é o TatuZap. Aqui você pode ficar sabendo sobre a sua grade (turmas, salas e horários), cardápio do RU, fretados (horários de partida), disciplinas da UFABC, etc. Basta digitar o que deseja.\n Alguns exemplos de uso:\n- Grade: quero saber as minhas turmas, ra 1234567891011\n- Cardápio RU: O que tem para o almoço/jantar?\n- Fretados: Qual o próximo fretado de SA para SBC?\n'



def verificar(mensagem):
    return True


'''
Função quando o usuário da um /start
'''
@bot.message_handler(commands=["start"])
def msg_inicial(mensagem):
    bot.reply_to(mensagem, msginicial)

@bot.message_handler(commands=["help"])
def msg_inicial(mensagem):
    bot.reply_to(mensagem, msginicial)

@bot.message_handler(content_types=['text'])
def padrao(mensagem):
    try:
        print('step padrao')
        print('Aqui está a mensagem: {} '.format(mensagem))

        response, intent = tatuia.tatu_zap.get_reply(mensagem.text) #recebe intent prevista com mensagem de resposta padrão para a intent
        print('response {},intent {}'.format(response,intent))
        if intent == "myclasses": #intent myclasses, para conseguir as salas/professores/horarios por RA
            msg = bot.reply_to(mensagem,response)
            if response == 'RA não encontrado, por favor digite seu RA' :
                print('set state ra')
                bot.register_next_step_handler(msg, ra)
            else : bot.register_next_step_handler(msg,padrao)
        elif intent == 'discinfo':
            if response == 'Selecionar na lista':
                search_nome_disc = tatuia.extract_nome_disciplina(mensagem.text)
                if search_nome_disc:
                    response = tatuia.get_disciplinas(mensagem.text)
                    print('response: ', response)
                    keyboard = telebot.types.InlineKeyboardMarkup() #utilizado para gerar o menu em mensagens do telegram
                    for disc in response:
                        keyboard.row(telebot.types.InlineKeyboardButton(disc['disciplina'], callback_data=disc['sigla']))#insere no menu cada disciplina presenta na lista, gerando um callback com a sigla da disciplina (para diferenciar)

                    msg = bot.reply_to(mensagem, 'Selecione qual o nome da disciplina desejada', reply_markup=keyboard)
            else: msg = bot.reply_to(mensagem,response)

            bot.register_next_step_handler(msg,padrao)
        else:
            msg = bot.reply_to(mensagem,response,parse_mode= 'Markdown')
            bot.register_next_step_handler(msg,padrao)
    except Exception as e:
        bot.reply_to(mensagem, e)


def ra(mensagem):
    try:
        print("step ra")
        response, intent = tatuia.tatu_zap.get_reply('matérias do ' + mensagem.text) #recebe intent prevista com mensagem de resposta padrão para a intent
        msg = bot.reply_to(mensagem,response)

        if intent == "myclasses": #intent myclasses, para conseguir as salas/professores/horarios por RA
            if response == 'RA não encontrado, por favor digite seu RA' :
                bot.register_next_step_handler(msg, ra)
            else : bot.register_next_step_handler(msg,padrao)
        else:
            bot.register_next_step_handler(msg,padrao)

        #bot.delete_state(mensagem.from_user.id, mensagem.chat.id)

    except Exception as e:
        bot.reply_to(mensagem, e)




#lida com callback (como o utilizado no menu no discinfo)
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
        userMessage = call.data
        texto = tatuia.get_disciplina_codigo(userMessage)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


#bot.polling()

#bot.add_custom_filter(custom_filters.StateFilter(bot))
#bot.enable_save_next_step_handlers(delay=2)


#bot.infinity_polling(skip_pending=True)


bot.infinity_polling()