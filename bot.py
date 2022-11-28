import telebot
from telebot import types
import emoji
import random

calс = False

gameIsStart = False

item = {}

gameGround = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " ", ]


CrossesOrToe = ["0", "X"]


playerSymbol = "X"


botSymbol = "0"


print("Bot is start")


winbool = False

losebool = False

call = False

def clear():
    global gameGround
    gameGround = [" ", " ", " ",
                  " ", " ", " ",
                  " ", " ", " ", ]


def win(cell_1, cell_2, cell_3):
    if cell_1 == playerSymbol and cell_2 == playerSymbol and cell_3 == playerSymbol:
        print("win")
        global winbool
        winbool = True


def lose(cell_1, cell_2, cell_3):
    if cell_1 == botSymbol and cell_2 == botSymbol and cell_3 == botSymbol:
        print("lose")
        global losebool
        losebool = True


def defend(cell_1, cell_2, posDef):
    if cell_1 == playerSymbol and cell_2 == playerSymbol:
        posDef = botSymbol


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
       
@bot.message_handler(commands=['game'])
def game_message(message):
    global gameIsStart
    gameIsStart = True
    bot.send_message(message.chat.id, "Крестики-нолики")

       
@bot.message_handler(content_types='text')
def message_reply(message):
    global calc
    global gameIsStart
    if calc == True :
        bot.send_message(message.chat.id,eval(message.text))
        calc = False 
    elif gameIsStart == True :
        bot.send_message(message.chat.id, "Игра началась")
        global markup
        markup = types.InlineKeyboardMarkup(row_width=3)

        global i 
        i = 0
        for i in range(9):
            item[i] = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))

        markup.row(item[0], item[1], item[2])
        markup.row(item[3], item[4], item[5])
        markup.row(item[6], item[7], item[8])
        bot.send_message(message.chat.id, "Выбери клетку", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbackInline(call):
    global gameIsStart
    if (call.message):
        global item
        randomCell = random.randint(0, 8)
        if gameGround[randomCell] == playerSymbol:
            randomCell = random.randint(0, 8)
        if gameGround[randomCell] == botSymbol:
            randomCell = random.randint(0, 8)
        if gameGround[randomCell] == " ":
            gameGround[randomCell] = botSymbol
       
        for i in range(9):
            if call.data == str(i):
                if (gameGround[i] == " "):
                    gameGround[i] = playerSymbol

            # lose or win
            win(gameGround[0], gameGround[1], gameGround[2])
            win(gameGround[0], gameGround[4], gameGround[8])
            win(gameGround[6], gameGround[4], gameGround[2])
            win(gameGround[6], gameGround[7], gameGround[8])
            win(gameGround[0], gameGround[3], gameGround[6])
            lose(gameGround[0], gameGround[1], gameGround[2])
            lose(gameGround[0], gameGround[4], gameGround[8])
            lose(gameGround[6], gameGround[4], gameGround[2])
            lose(gameGround[6], gameGround[7], gameGround[8])
            lose(gameGround[0], gameGround[3], gameGround[6])

            item[i] = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))

        global  markup
        markup.row(item[0], item[1], item[2])
        markup.row(item[3], item[4], item[5])
        markup.row(item[6], item[7], item[8])

        bot.send_message(call.message.chat.id, "Выбери клетку", reply_markup=markup)
        global winbool
        if winbool:
            clear()
            bot.send_message(call.message.chat.id, "Я проиграл :(")

            winbool = False
            gameIsStart = False
        global losebool
        if losebool:
            clear()
            bot.send_message(call.message.chat.id, "Я выиграл!!")


            losebool = False
            gameIsStart = False
                  
bot.polling()