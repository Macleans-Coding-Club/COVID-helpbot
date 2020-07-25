import telebot
from telebot import types
import pandas as pd
from csv import writer

bot = telebot.TeleBot("1317717235:AAGo2iVPuabY6FpayigYouJuA5ydgg_ypr4", parse_mode=None)
knownUsers = []
Data_sheet = "D://information_table.csv"


#-------------------------------------------------------------------------------
def AddToCsvFile(FileName, ListRowContent):
    with open(FileName, 'a+', newline='') as i:
        csv_writer = writer(i)
        csv_writer.writerow(ListRowContent)
        #This function is used to add to a csv file
#---------------------------------------------------------------------------------
    
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup.add('Male', 'Female')
userLocation_markup = types.ReplyKeyboardMarkup()
yesBt = types.KeyboardButton(text = 'Yes', request_location = True)
noBt = types.KeyboardButton(text = 'No')
userLocation_markup.row(yesBt,noBt)
force = types.ForceReply(selective=False)
#--------------------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
def command_start(m):
    df = pd.read_csv(Data_sheet)
    cid = m.chat.id
    if cid not in df.values:  # if user hasn't used the "/start" command yet:
        knownUsers.append(str(cid))  # save user id, so you could brodcast messages to all users of this bot later
        print(cid)
        start_msg = bot.send_message(cid , "Hello, Seem like this is the first time we meet. I will have to ask for your information. First, may i ask for your name?", reply_markup = force)
        bot.register_next_step_handler(start_msg, ask_for_age)
    else:
        bot.send_message(cid, "I already know you")

def ask_for_age(message):
    cid = message.chat.id
    global userName
    userName = message.text
    print(userName)
    age_msg = bot.send_message(cid , "Your age?", reply_markup = force)
    bot.register_next_step_handler(age_msg, ask_for_gender)

def ask_for_gender(message):
    cid = message.chat.id
    global userAge
    userAge = message.text
    print(userAge)
    sex_msg = bot.send_message(cid , "May i ask for your gender as well?", reply_markup = markup)
    bot.register_next_step_handler(sex_msg, ask_for_phone)

def ask_for_phone(message):
    cid = message.chat.id
    global userGender
    userGender = message.text
    print(userGender)
    phone_msg = bot.send_message(cid , "What is your phone number?", reply_markup = force)
    bot.register_next_step_handler(phone_msg, ask_for_mail)

def ask_for_mail(message):
    cid = message.chat.id
    global userPhone
    userPhone = message.text
    print(userPhone)
    mail_msg = bot.send_message(cid , "what is your gmail?", reply_markup = force)
    bot.register_next_step_handler(mail_msg, ask_for_location)

def ask_for_location(message):
    cid = message.chat.id
    global userMail
    userMail = message.text
    print(userMail)
    bot.send_message(cid, "Will you allow us to know your location?", reply_markup = userLocation_markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    global location_latitude
    location_latitude = message.location.latitude
    global location_longitude
    location_longitude = message.location.longitude
    print(location_latitude, location_longitude)
    
    RowContent = [knownUsers[0], userName, userAge, userGender, userPhone, userMail, location_latitude, location_longitude]
    AddToCsvFile(Data_sheet ,RowContent)

bot.polling()
