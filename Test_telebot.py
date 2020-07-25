import telebot                  #import telebot libary
from telebot import types

bot = telebot.TeleBot("TOKEN", parse_mode=None) 

markup = types.ReplyKeyboardMarkup()    #setting up new keyboard
itembtna = types.KeyboardButton('a')    
itembtnv = types.KeyboardButton('v')
itembtnc = types.KeyboardButton('c')
itembtnd = types.KeyboardButton('d')
itembtne = types.KeyboardButton('e')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd, itembtne)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "I'm called TeleBot beep boop",  reply_markup=markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])   
@bot.message_handler(func=lambda message: True)     #reply back with the same message
def send_any(message):
    bot.send_message(message.chat.id, message.text)         

bot.polling()
