import telebot                  #import telebot libary
from telebot import types

bot = telebot.TeleBot("992300889:AAEuMc0EdcBm7enrID7FDUjVuEzo9WqHbzM")

helpers = {}  # save these in a file
need_help = {}
other = []

commands = {  # command description for new users 
    'start'       : 'Get used to the bot',
    'help'        : 'show available commands',
    'needhelp'    : 'register as vulnerable',
    'helper'      : 'register as volunteer helper'
}

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('/help')
itembtn2 = types.KeyboardButton('/needhelp')
itembtn3 = types.KeyboardButton('/helper')
markup.add(itembtn1, itembtn2, itembtn3)


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in other and cid not in need_help and cid not in helpers:  # if user hasn't used the "/start" command yet:
        bot.send_message(cid, "Hello, stranger, ")
        bot.send_message(cid, "Scanning complete, I know you now")
        other.append(cid)
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")
        bot.send_message(cid, "Choose a command:", reply_markup=markup)


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page
    bot.send_message(cid, "Choose a command:", reply_markup=markup)

#register as helper
@bot.message_handler(commands=['helper'])
def helping(m):
    cid = m.chat.id
    if cid in other:
        other.remove(cid)
        #take user contact details
        
    elif cid in need_help:
        need_help.pop(cid)
        #take user contact details
    
    elif cid in helpers:
        bot.send_message(cid, "You are already a helper")
    bot.send_message(cid, "Choose a command:", reply_markup=markup)

#register as vulnerable
@bot.message_handler(commands=['needhelp'])
def helping(m):
    cid = m.chat.id
    if cid in other:
        other.remove(cid)
        #take user contact details
        
    elif cid in helpers:
        need_help.pop(cid)
        #take user contact details
    
    elif cid in need_help:
        bot.send_message(cid, "You are already registered")
    bot.send_message(cid, "Choose a command:", reply_markup=markup)

bot.polling()
