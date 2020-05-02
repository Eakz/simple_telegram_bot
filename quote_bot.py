# TODO add async database usage.
import telebot
from qod import read_json, write_json, quoting, dict_f, gquote
import time
from telebot import types
import requests
"""
This is a detailed example using almost every command of the API
"""

TOKEN = '1243531721:AAFczJI3DL04WaiGwwtxtlNAvRkxFU-45WQ'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'qod': 'A \'QUOTE\' of the day',
    'getImage': 'Get a random cat',
    'help': 'back to menu',
    'currency': 'Get Ukraine cur/exc rates'
}

imageSelect = types.ReplyKeyboardMarkup(
    one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Kitties')
menuSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
menuSelect.add('/start', '/getImage', '/currency', '/qod')

hideBoard = types.ReplyKeyboardRemove(
)  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(
                str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " +
                m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener
bot.set_chat_description = 'Welcome To FunTimes!'


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(
            cid
        )  # save user id, so you could brodcast messages to all users of this
        #  bot later
        userStep[
            cid] = 0  # save user id and his current "command level", so he
        #  can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(
            cid, "I already know you, no need for me to scan you again!")
    try:
        quote, author = gquote()
        data = read_json()
        write_json(dict_f(quote, author, data))
        bot.send_message(cid, 'Quotes database updated')
    except Exception as e:
        bot.send_message(cid, 'Can\'t connect to API!')
        print(e)
    finally:
        bot.send_message(cid, '/help')


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands
        # dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text,
                     reply_markup=menuSelect)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['qod'])
def command_qod(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(cid, quoting())
    bot.send_message(cid, '/help')


@bot.message_handler(commands=['currency'])
def currency_privat(m):
    cid = m.chat.id
    try:
        PRIVAT_BANK_URL =\
            'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        pj = requests.get(PRIVAT_BANK_URL).json()
        for i in pj:
            bot.send_message(
                cid, f"|{i['ccy']}\t|\t{i['base_ccy']}|\n\n"
                f"Buy\t|\t{i['buy']}\nSell\t|\t{i['sale']}")
    except Exception as e:
        bot.send_message(cid, 'Sorry bank has some problems!')
        print(e)
    finally:
        bot.send_message(cid, '/help')


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid,
                     "Please choose your image now",
                     reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step
    # (expecting a reply in the listener now)
    bot.send_message(cid, '/help')


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    try:
        # for some reason the 'upload_photo' status isn't quite working
        #  (doesn't show at all)
        bot.send_chat_action(cid, 'typing')
        img = requests.get('https://thecatapi.com/api/images/get'
                           '?format=src&type=gif&size=medium')
        if text == 'Kitties':  # send the appropriate image based on the reply
            #  to the "/getImage" command
            bot.send_video(
                cid, img.url, reply_markup=hideBoard
            )  # send file and hide keyboard, after image is sent
            userStep[cid] = 0  # reset the users step back to 0

        else:
            bot.send_message(cid, "Please, use the predefined keyboard!")
            bot.send_message(cid, "Please try again")
        data = read_json()
        data['img_url'] = img.url
        write_json(data)
    except Exception as e:
        print(e)
        try:
            img = read_json()['img_url']
            bot.send_video(cid, img, reply_markup=hideBoard)
        except Exception as e:
            print(e)
            bot.send_message(cid, "We dont have any kitties now")
    finally:
        bot.send_message(cid, '/help')


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")
    bot.send_message(m.chat.id, '/help')


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(
        m.chat.id, "I don't understand \"" + m.text +
        "\"\nMaybe try the help page at /help")


# quotes
bot.polling()
