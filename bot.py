import telebot
from telebot import types
import emoji
from calc import *

calс = False

API_TOKEN='5980890864:AAEvYO5STRtviJKf1IJyCRHZA2fKvG3IlzY'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start']) 
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("/calc")
    item2 = types.KeyboardButton("/game")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id,emoji.emojize(":vulcan_salute: Привеееет, {0.first_name}!\n Выбери нужную функцию в меню. :backhand_index_pointing_down:\n Подсказка:\n /calc - калькулятор \n /game - игра в крестики-нолики ").format(message.from_user), reply_markup = markup)

@bot.message_handler(commands=['calc'])
def calc_message(message):
    global calc
    calc=True
    bot.send_message(message.chat.id, "А теперь введите выражение" )
       
       
@bot.message_handler(content_types='text')
def message_reply(message):
    global calc
    if calc :
        bot.send_message(message.chat.id,eval(message.text))
        calc=False    
        
                  
bot.polling()