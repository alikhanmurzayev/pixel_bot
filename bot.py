import telebot

import config
import messages
import database

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message)
    database.set_status(message, 'name')
    bot.send_message(message.chat.id, messages.start_message)
    current_status = database.get_status(message)
    bot.send_message(message.chat.id, current_status)


bot.polling(none_stop=True)