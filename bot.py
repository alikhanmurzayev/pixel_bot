import telebot

import config
import messages
import database

bot = telebot.TeleBot(config.token)


def send_help(message):
    # Sending buttons
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row(messages.take_test)
    user_markup.row(messages.find_friends)
    bot.send_message(message.chat.id, messages.help_message, reply_markup=user_markup)

@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message)
    database.set_status(message, config.name)
    bot.send_message(message.chat.id, messages.start_message)
    bot.send_message(message.chat.id, messages.name_message)

@bot.message_handler(content_types=['text'])
def text_messages(message):
    status = database.get_status(message)
    if status == config.name:
        database.set_name(message)
        database.set_status(message, config.age)
        bot.send_message(message.chat.id, messages.age_message)
    elif status == config.age:
        database.set_age(message)
        database.set_status(message, config.gender)
        # Sending buttons
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(messages.gender_male, messages.gender_female)
        bot.send_message(message.chat.id, messages.gender_message, reply_markup=user_markup)
    elif status == config.gender:
        database.set_gender(message)
        database.set_status(message, config.interest)
        # Sending buttons
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(messages.interest_count, messages.interest_languages)
        user_markup.row(messages.interest_paint, messages.interest_read)
        bot.send_message(message.chat.id, messages.interest_message, reply_markup=user_markup)
    elif status == config.interest:
        database.set_interest(message)
        database.set_status(message, config.wait)
        send_help(message)
    elif status == config.wait:
        if message.text == messages.take_test:
            bot.send_message(message.chat.id, 'прохождение теста...')
        elif message.text == messages.find_friends:
            bot.send_message(message.chat.id, 'поиск друзей...')


bot.polling(none_stop=True)