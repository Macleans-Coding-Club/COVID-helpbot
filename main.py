import telebot
from telebot import types
import pandas as pd
from csv import writer

bot = telebot.TeleBot("1317717235:AAGo2iVPuabY6FpayigYouJuA5ydgg_ypr4", parse_mode=None)
knownUsers = []

#-------------------------------------------------------------------------------
def AddToCsvFile(FileName, ListRowContent):
    with open(FileName, 'a+', newline='') as i:
        csv_writer = writer(i)
        csv_writer.writerow(ListRowContent)
        #This function is used to add to a csv file
#---------------------------------------------------------------------------------


Gender_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
Gender_markup.add('Male', 'Female')
userLocation_markup = types.ReplyKeyboardMarkup()
yesBt = types.KeyboardButton(text = 'Share location', request_location = True)
userLocation_markup.row(yesBt)
force = types.ForceReply(selective=False)
Group_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
Group_markup.add('I need help!', 'I want to help!')
#--------------------------------------------------------------------------------------


@bot.message_handler(commands=['start']) #start
def ChooseGroup(message):
    cid = message.chat.id
    bot.send_message(message.chat.id, "Are you looking to help or do you need help?", reply_markup = Group_markup)


@bot.message_handler(func=lambda message: message.text == "I want to help!")
def helping(message):
    cid = message.chat.id
    global Data_sheet
    Data_sheet = "Volunteer.csv"
    print(Data_sheet)
    volunteer_msg = bot.send_message(cid, "Thank you for volunteering")
    command_start(message)

@bot.message_handler(func=lambda message: message.text == "I need help!")
def needinghelp(message):
    cid = message.chat.id
    global Data_sheet
    Data_sheet = "Elderly.csv"
    print(Data_sheet)
    elderly_msg = bot.send_message(cid, "Thank you for using our service!", )
    command_start(message)
    
    
def command_start(message):
    cid = message.chat.id
    global df
    df = pd.read_csv(Data_sheet)
    
    if cid not in df.values:        
        knownUsers.append(str(cid))  
        print(cid)
        start_msg = bot.send_message(cid , "Hello, it seems like this is the first time you are using our service. I will need your information. Firstly, what is your name?", reply_markup = force)
        bot.register_next_step_handler(start_msg, ask_for_age)
    else:
        bot.send_message(cid, "Hmm, it seems like we already know eachother!")
        

    
def ask_for_age(message):       
    cid = message.chat.id
    global userName
    userName = message.text
    print(userName)
    age_msg = bot.send_message(cid , "What is your age?", reply_markup = force)
    bot.register_next_step_handler(age_msg, ask_for_gender)

def ask_for_gender(message):    #ask_for gender
    cid = message.chat.id
    global userAge
    userAge = message.text
    print(userAge)
    sex_msg = bot.send_message(cid , "What gender do you indentify as?", reply_markup = Gender_markup)
    bot.register_next_step_handler(sex_msg, ask_for_phone)

def ask_for_phone(message):     #ask_for_phone
    cid = message.chat.id
    global userGender
    userGender = message.text
    print(userGender)
    phone_msg = bot.send_message(cid , "What is your phone number?", reply_markup = force)
    bot.register_next_step_handler(phone_msg, ask_for_mail)

def ask_for_mail(message):      #ask_ for_mail
    cid = message.chat.id
    global userPhone
    userPhone = message.text
    print(userPhone)
    mail_msg = bot.send_message(cid , "What is your email address?", reply_markup = force)
    bot.register_next_step_handler(mail_msg, ask_for_location)

def ask_for_location(message):  #ask_for_location
    cid = message.chat.id
    global userMail
    userMail = message.text
    print(userMail)
    bot.send_message(cid, "Can you share your location with us?", reply_markup = userLocation_markup)

@bot.message_handler(content_types=['location'])    #collect user location 
def handle_location(message):
    global location_latitude
    location_latitude = message.location.latitude
    global location_longitude
    location_longitude = message.location.longitude
    print(location_latitude, location_longitude)
    
    
    RowContent = [knownUsers[0], userName, userAge, userGender, userPhone, userMail, location_latitude, location_longitude]
    AddToCsvFile(Data_sheet , RowContent)

bot.polling()
