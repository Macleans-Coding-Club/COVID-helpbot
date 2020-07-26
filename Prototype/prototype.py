import telebot                  #import telebot libary
from telebot import types
import pandas as pd

bot = telebot.TeleBot("992300889:AAEuMc0EdcBm7enrID7FDUjVuEzo9WqHbzM")

hp = pd.read_csv('helpers.csv', index_col=0)
nh = pd.read_csv('need_help.csv', index_col=0)
oth = pd.read_csv('other.csv', index_col=0)

helpers = hp.to_dict()   # save these in a csv file
need_help = nh.to_dict() 
other = oth.to_dict() 

commands = {  # command description for new users 
    'start'       : 'Get used to the bot',
    'help'        : 'show available commands',
    'elderly'    : 'register as vunerable',
    'helper'      : 'register as volunteer helper',
    'needhelp'    :  'ask a volunteer for help'
}

details = {
     'NAME':'',
     'AGE':'',
     'GENDER':'',
     'PHONE':'',
     'EMAIL':'',
     'LONGITUDE':'',
     'LATITUDE':''
}

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('/help')
itembtn2 = types.KeyboardButton('/elderly')
itembtn3 = types.KeyboardButton('/helper')
itembyn4 = types.KeyboardButton('/needhelp')
markup.add(itembtn1, itembtn2, itembtn3)

force = types.ForceReply(selective=False)

yesno = types.ReplyKeyboardMarkup(row_width=2)
yes = types.KeyboardButton('yes')
no = types.KeyboardButton('no')
yesno.add(yes,no)

gender = types.ReplyKeyboardMarkup(row_width=2)
male = types.KeyboardButton('male')
female = types.KeyboardButton('female')
others = types.KeyboardButton('other')
gender.add(male,female,others)

send_loc = types.ReplyKeyboardMarkup()
location_button = types.KeyboardButton(text="Send Location", request_location=True)
send_loc.row(location_button)

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if str(cid) not in other and str(cid) not in need_help and str(cid) not in helpers:  # if user hasn't used the "/start" command yet:
          bot.send_message(cid, "Hello, stranger, ")
          bot.send_message(cid, "Scanning complete, I know you now")
          other[cid] = ''
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
    global register
    cid = m.chat.id
    register = "helper"
    if str(cid) in other:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
        #take user contact details
        
    elif str(cid) in need_help:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
        #take user contact details
    
    elif str(cid) in helpers:
        bot.send_message(cid, "You are already a helper, changing details")
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)

#register as vulnerable
@bot.message_handler(commands=['elderly'])
def needinghelp(m):
     global register
     cid = m.chat.id
     register = "vunerable"
     if str(cid) in other:
          name = bot.send_message(cid, 'What is your name?',reply_markup = force)
          bot.register_next_step_handler(name, get_name)
          #take user contact details  
     elif str(cid) in helpers:
          name = bot.send_message(cid, 'What is your name?',reply_markup = force)
          bot.register_next_step_handler(name, get_name)
          #take user contact details
    
     elif str(cid) in need_help:
          bot.send_message(cid, "You are already registered, changing details")
          name = bot.send_message(cid, 'What is your name?',reply_markup = force)
          bot.register_next_step_handler(name, get_name)
     

def get_name(m):
     cid = m.chat.id
     info = m.text
     details['NAME'] = info
     age = bot.send_message(cid, 'What is your age?',reply_markup = force)
     bot.register_next_step_handler(age, get_age)

def get_age(m):
     cid = m.chat.id
     info = m.text
     details['AGE'] = info
     gen = bot.send_message(cid, 'What is your gender?',reply_markup = gender)
     bot.register_next_step_handler(gen, get_gender)

def get_gender(m):
     cid = m.chat.id
     info = m.text
     details['GENDER'] = info
     phone = bot.send_message(cid, 'What is your phone number?',reply_markup = force)
     bot.register_next_step_handler(phone, get_phone)

def get_phone(m):
     cid = m.chat.id
     info = m.text
     details['PHONE'] = info
     email = bot.send_message(cid, 'What is your email address?',reply_markup = force)
     bot.register_next_step_handler(email, get_email)

def get_email(m):
     cid = m.chat.id
     info = m.text
     details['EMAIL'] = info
     location = bot.send_message(cid, 'Send current location as home address?',reply_markup = yesno)
     bot.register_next_step_handler(location, get_location)

def get_location(m):
     cid = m.chat.id
     info = m.text
     if info == 'yes':
          try:
               locate = bot.send_message(cid,"Please let us know your location", reply_markup=send_loc)
               bot.register_next_step_handler(locate, handle_location)
          except:
               details['LONGITUDE'] = ''
               details['LATITUDE'] = ''
               end = bot.send_message(cid, 'Save information?',reply_markup = yesno)
               bot.register_next_step_handler(end, save_info)
               
     elif info == 'no':
          details['LONGITUDE'] = ''
          details['LATITUDE'] = ''
          end = bot.send_message(cid, 'Save information?',reply_markup = yesno)
          bot.register_next_step_handler(end, save_info)

def handle_location(m):
     cid = m.chat.id
     details['LONGITUDE'] = m.location.latitude
     details['LATITUDE'] = m.location.longitude
     end = bot.send_message(cid, 'Save information?',reply_markup = yesno)
     bot.register_next_step_handler(end, save_info)

def save_info(m):
     cid = m.chat.id
     info = m.text
     if info == 'yes':
          if register == "vunerable":
               print(details)  #save info
               if cid in other:
                    other.pop(cid)
               elif cid in helpers:
                    helpers.pop(cid)
               need_help[cid] = details.copy()
               save_to_csv()
          elif register == "helper":
               print(details)  #save info
               if cid in other:
                    other.pop(cid)
               elif cid in need_help:
                    need_help.pop(cid)
               helpers[cid] = details.copy()
               save_to_csv()
     elif info == 'no':
          for key in details:
               details[key] = ''
     bot.send_message(cid, "Choose a command:", reply_markup=markup)

def save_to_csv():
     hp = pd.DataFrame(data=helpers, index=[0])
     hp.to_csv('helpers.csv')
     nh = pd.DataFrame(data=need_help, index=[0])
     nh.to_csv('need_help.csv')
     oth = pd.DataFrame(data=other, index=[0])
     oth.to_csv('other.csv')

bot.polling()
