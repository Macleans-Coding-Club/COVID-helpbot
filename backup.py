import telebot                  #import telebot libary
from telebot import types
import pandas as pd
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

bot = telebot.TeleBot("992300889:AAEuMc0EdcBm7enrID7FDUjVuEzo9WqHbzM")
geolocator = Nominatim(user_agent="COVID-helpbot")

commands = {  # command description for new users 
    'start'       : 'Get used to the bot',
    'help'        : 'show available commands',
    'elderly'    : 'register as vunerable',
    'helper'      : 'register as volunteer helper',
    'needhelp'    :  'ask a volunteer for help'
}

details = pd.DataFrame({
     'ID'  :'',
     'NAME':'',
     'AGE':'',
     'GENDER':'',
     'PHONE':'',
     'EMAIL':'',
     'LONGITUDE':'',
     'LATITUDE':''
},columns = ['ID','NAME','AGE','GENDER','PHONE','EMAIL','LONGITUDE','LATITUDE'],index = ['1'])

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('/help')
itembtn2 = types.KeyboardButton('/elderly')
itembtn3 = types.KeyboardButton('/helper')
itembtn4 = types.KeyboardButton('/needhelp')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

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
    update()
    if cid not in need_help['ID'].values and cid not in helpers['ID'].values :  # if user hasn't used the "/start" command yet:
          bot.send_message(cid, "Hello, stranger")
          bot.send_message(cid, "You are not register in the system, please register as a helper or an elder")
          command_help(m)  # show the new user the help page
    else:
          bot.send_message(cid, "Hello, welcome back")
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
    if cid in need_help:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
        #take user contact details
    elif cid in helpers:
        bot.send_message(cid, "You are already a helper, changing details")
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
    else:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
        #take user contact details

#register as vulnerable
@bot.message_handler(commands=['elderly'])
def needinghelp(m):
    global register
    cid = m.chat.id
    register = "vulnerable" 
    if cid in helpers:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
        #take user contact details
    elif cid in need_help:
        bot.send_message(cid, "You are already registered, changing details")
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)
    else:
        name = bot.send_message(cid, 'What is your name?',reply_markup = force)
        bot.register_next_step_handler(name, get_name)

#ask for help
@bot.message_handler(commands=['needhelp'])
def helpme(m):
    update()
    cid = m.chat.id
    if cid not in need_help['ID'].values:
        bot.send_message(cid, "You are not registered as an elder, please register first")
    else:
        bot.send_message(cid, "Here is a list of volunteers and their info")
        vol = []
        longitude = need_help.loc[need_help.index[need_help['ID'] == cid], 'LONGITUDE'][0]
        latitude = need_help.loc[need_help.index[need_help['ID'] == cid], 'LATITUDE'][0]
        if pd.isnull(longitude) or pd.isnull(latitude):  #if location is recorded
            for index in range(5):
                row = helpers.loc[index]
                message = "Name: "+str(row['NAME'])+"\n Age: "+str(row['AGE'])+"\n Gender: "+str(row['GENDER'])+"\n Phone: "+str(row['PHONE'])+"\n Email: "+str(row['EMAIL'])
                bot.send_message(cid, message)
        else:
            for index,row in helpers.iterrows():    #find nearest volunteer
                if pd.isnull(row['LONGITUDE']) or pd.isnull(row['LATITUDE']):
                    vol.append((index, 9999))
                else:
                    distance = geodesic((latitude,longitude), (row['LATITUDE'],row['LONGITUDE'])).miles
                    vol.append((index, distance))
            vol.sort(key = lambda person: person[1])
            for index in range(5):
                row = helpers.loc[vol[index][0]]
                location = geolocator.reverse(str(row['LATITUDE'])+','+str(row['LONGITUDE']))
                message = " Name: "+str(row['NAME'])+"\n Age: "+str(row['AGE'])+"\n Gender: "+str(row['GENDER'])+"\n Phone: "+str(row['PHONE'])+"\n Email: "+str(row['EMAIL'])+"\n Address: "+str(location.address)
                bot.send_message(cid, message)
                
    bot.send_message(cid, "Choose a command:", reply_markup=markup)

def get_name(m):
     cid = m.chat.id
     info = m.text
     details['ID'] = cid
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
     details['LATITUDE'] = str(m.location.latitude)
     details['LONGITUDE'] = str(m.location.longitude)
     end = bot.send_message(cid, 'Save information?',reply_markup = yesno)
     bot.register_next_step_handler(end, save_info)

def save_info(m):
     cid = m.chat.id
     info = m.text
     global helpers
     global need_help
     if info == 'yes':
          if register == "vulnerable":
               print(details)  #save info
               if cid in helpers['ID'].values:
                    helpers = helpers[helpers['ID'] != cid]
               elif cid in need_help['ID'].values:
                    need_help = need_help[need_help['ID'] != cid]
               update()
               need_help = need_help.append(details)
               save_to_csv()
          elif register == "helper":
               print(details)  #save info
               if cid in need_help['ID'].values:
                    need_help = need_help[need_help['ID'] != cid]
               elif cid in helpers['ID'].values:
                    helpers = helpers[helpers['ID'] != cid]
               update()
               helpers = helpers.append(details)
               save_to_csv()
     elif info == 'no':
          details.loc['1'] = ''
     bot.send_message(cid, "Choose a command:", reply_markup=markup)

def save_to_csv():
    helpers.to_csv('Volunteer.csv',index=False)
    need_help.to_csv('Elderly.csv',index=False)

def update():
    global helpers
    global need_help
    helpers = pd.read_csv('Volunteer.csv', index_col = False)
    need_help = pd.read_csv('Elderly.csv', index_col = False)



bot.polling()
