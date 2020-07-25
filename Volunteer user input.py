import telebot
from telebot import types

API_TOKEN = '1076450876:AAHNcfXOVfnhH1UP5auDb-ypDk3hrFFCd9k'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

# Creates a list to store data in
info = []

# Beings bot after command /help or /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hello, I am the Sigmahacks Testbot
Please enter your name
""")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    # Gets chat id from the most recent reply from user.
    chat_id = message.chat.id
    # The most recent message from user would be their name.
    name = message.text
    # Name value is added to list.
    info.append(name)
    # Asks user to reply to message with their age.
    msg = bot.reply_to(message, 'How old are you?')
    #Program will procede to the next step called process_name_phone.
    bot.register_next_step_handler(msg, process_name_phone)


# Process is similar to above.
def process_name_phone(message):
    chat_id = message.chat.id
    age = message.text
    info.append(age)
    msg = bot.reply_to(message, 'What is your mobile number? ')
    bot.register_next_step_handler(msg, process_name_email)


def process_name_email(message):

    chat_id = message.chat.id
    number = message.text
    info.append(number)
    msg = bot.reply_to(message, 'What is your email?')
    bot.register_next_step_handler(msg, process_age_step)


def process_age_step(message):

    chat_id = message.chat.id
    email = message.text
    info.append(email)

    # Code to create male / female gender.
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Male', 'Female')
    msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
    bot.register_next_step_handler(msg, process_sex_step)


# The button is like a keyboard to send a message, same input as if normally
# typing male / female
def process_sex_step(message):

    sex = message.text
    info.append(sex)
    #Info is the list containing all of the data collected.
    print(info)


# Must be kept to run program
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()
