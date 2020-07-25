from telebot import types
import telebot

API_TOKEN = '1076450876:AAHNcfXOVfnhH1UP5auDb-ypDk3hrFFCd9k'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup()
    location_button = types.KeyboardButton(text="Send Location", request_location=True)
    keyboard.add(location_button)
    bot.send_message(message.chat.id, "Please let us know your location", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))
    
print()
bot.polling()
  

