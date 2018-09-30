import telebot

import config
import messages
import database

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message)
    bot.send_message(message.chat.id, messages.start_message)

bot.polling(none_stop=True)