#myapp/telegrambot.py
# Example code for telegrambot.py module
from .models import Upravljanje
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

import logging
logger = logging.getLogger(__name__)

commands = {
              'start': 'Provjeri status operatera',
              'operater': 'Daje informaciju o glavnim naredbama linije pogona',
              'kamera': 'Naredbe za upravljanje kamere',
              'linija': 'Naredbe za upravljanje linije',
              'zaustavi': 'Zaustavi aktivni model',
              'model': 'Modeli kojima je moguce upravljati',
}

kamera_ctrl = {
              'video': 'Pokreni video - pregled pomocu VLC app',
              'stop': 'Zaustavi video buffer - stop stream',
              'fotka': 'Snimanje fotografije',
}


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def operater(bot, update):
    text = "Glavne naredbe linije pogona: \n"
    for key in commands:
        text += "/" + key + ": "
        text += commands[key] + "\n"
    bot.sendMessage(update.message.chat_id, text=text)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def kamera(bot, update):
    video = KeyboardButton(text="video")
    stop = KeyboardButton(text="stop")
    fotka = KeyboardButton(text="fotka")
    custom_keyboard = [[ video, stop, kamera]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    bot.sendMessage(update.message.chat_id,
              text="Upravljanje modulom za kameru",
              reply_markup=reply_markup)

def linija(bot, update):
    nul = KeyboardButton(text=" ")
    brze = KeyboardButton(text="brze")
    sporije = KeyboardButton(text="sporije")
    lijevo = KeyboardButton(text="fotka")
    desno = KeyboardButton(text="desno")
    pauziraj = KeyboardButton(text="pauziraj")
    custom_keyboard = [[ nul, brze, nul],
                       [ lijevo, pauziraj, desno],
                       [ nul, sporije, nul]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    bot.sendMessage(update.message.chat_id,
              text="Upravljanje modulom linije pogona",
              reply_markup=reply_markup)

def zaustavi(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def kamera(bot, update):
    video = KeyboardButton(text="video")
    stop = KeyboardButton(text="stop")
    fotka = KeyboardButton(text="fotka")
    custom_keyboard = [[ video, stop, kamera]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    bot.sendMessage(update.message.chat_id,
              text="Upravljanje modulom za kameru",
              reply_markup=reply_markup)

def model(bot, update):
    queryset = Upravljanje.objects.filter(korisnik=request.user)
    title = queryset.title
    for key in title:
        #text += "/" + model.title + "\n"
        #text += commands[key] + "\n"
        text += "/" + title[key] + "\n"
    bot.sendMessage(update.message.chat_id, text=key)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("operater", operater))
    dp.add_handler(CommandHandler("kamera", kamera))
    dp.add_handler(CommandHandler("linija", linija))
    dp.add_handler(CommandHandler("zaustavi", zaustavi))
    dp.add_handler(CommandHandler("model", model))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)
