import telebot
from telebot import types

bot = telebot.TeleBot("TOKEN", parse_mode=None)

markup = types.ReplyKeyboardMarkup()
ElderlyBT = types.KeyboardButton('/Elderly')
markup.row(ElderlyBT)
force = types.ForceReply(selective=False)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid , "Hello, how may i help you?", reply_markup = markup)

@bot.message_handler(commands=['Elderly'])
def Aks_name(message):
    cid = message.chat.id
    name = bot.send_message(cid , "what is your name?", reply_markup = force)
    bot.register_next_step_handler(name, Set_name)
    
def Set_name(message):
    cid = message.chat.id
    userName = message.text
    print(userName)    

bot.polling()
