import telebot
import time
from telebot import types

# Telegram token - Android, PC
TOKEN_BOT = '462144950:AAFBwrFtFR1tx70E5hzIVkjOxucuLNX3mug'

commands = {
              'start': 'Provjeri status operatera',
              'operater': 'Daje informaciju o glavnim naredbama linije pogona',
              'kamera': 'Naredbe za upravljanje kamere',
              'linija': 'Naredbe za upravljanje linije',
}

knownUsers = ['linijapogona']
userStep = {}

bot = telebot.TeleBot(TOKEN_BOT)

# prva naredba /start
@bot.message_handler(commands=['start'])
def command_start(m):
    tip = m.chat.id
    if tip not in knownUsers:
        knownUsers.append(tip)
        userStep[tip] = 0
        bot.send_message(tip, "Dobrodosao u pogon, pricekaj zbog skeniranja...")
        msg = "Zavrseno skeniranje, sada smo upareni. RazgovorID: " + str(tip)
        bot.send_message(tip, msg)
        command_help(m)
    else:
        bot.send_message(tip, "Upareni smo od prije, nastavi.")


# ispisi glavne naredbe
@bot.message_handler(commands=['operater'])
def command_help(m):
    tip = m.chat.id
    help_text = "Glavne naredbe linije pogona: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(tip, help_text)

# kamera naredba video
@bot.message_handler(commands=['video'])
def command_video(m):
    tip = m.chat.id
    bot.send_message(tip, "Kamera pokreni video")

# kamera naredba stop
@bot.message_handler(commands=['stopvid'])
def command_stop_video(m):
    tip = m.chat.id
    bot.send_message(tip, "Kamera zaustavi video")

# kamera naredba fotografija
@bot.message_handler(commands=['fotografija'])
def command_fotografija(m):
    tip = m.chat.id
    bot.send_message(tip, "Pohrani fotografiju")

# linija naredba brze
@bot.message_handler(commands=['brze'])
def command_brze(m):
    tip = m.chat.id
    bot.send_message(tip, "Linija brzina BRZE")

# linija naredba sporije
@bot.message_handler(commands=['sporije'])
def command_sporije(m):
    tip = m.chat.id
    bot.send_message(tip, "Linija brzina SPORIJE")

# linija naredba lijevo
@bot.message_handler(commands=['lijevo'])
def command_lijevo(m):
    tip = m.chat.id
    bot.send_message(tip, "Lija smjer LIJEVO")

# linija naredba desno
@bot.message_handler(commands=['desno'])
def command_desno(m):
    tip = m.chat.id
    bot.send_message(tip, "Linija smjer DESNO")

# linija naredba pauziraj
@bot.message_handler(commands=['pauziraj'])
def command_pauziraj(m):
    tip = m.chat.id
    bot.send_message(tip, "Linija status pauziraj")

# kamera tipkovnica
@bot.message_handler(commands=['kamera'])
def command_kamera(m):
    tip = m.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('/video')
    itembtn2 = types.KeyboardButton('/stopvid')
    itembtn3 = types.KeyboardButton('/fotografija')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(tip, "Kamera:", reply_markup=markup)

# linija tipkovnica
@bot.message_handler(commands=['linija'])
def command_linija(m):
    tip = m.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton(' ')
    itembtn2 = types.KeyboardButton('/brze')
    itembtn3 = types.KeyboardButton(' ')
    itembtn4 = types.KeyboardButton('/lijevo')
    itembtn5 = types.KeyboardButton('/pauziraj')
    itembtn6 = types.KeyboardButton('/desno')
    itembtn7 = types.KeyboardButton(' ')
    itembtn8 = types.KeyboardButton('/sporije')
    itembtn9 = types.KeyboardButton(' ')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
    bot.send_message(tip, "Upravljanje linijom:", reply_markup=markup)

bot.polling(none_stop=True)
