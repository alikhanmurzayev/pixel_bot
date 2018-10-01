import telebot
import random

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

def take_test(message):
    print('hello')

def send_question(message):
    conn, cursor = database.open_db(database.db_name)
    query = f"SELECT test_id, question_number, score FROM {database.status_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(query).fetchall()[0]
    test_id = int(result[0])
    question_number = int(result[1])
    score = int(result[2])
    # get number of questions in test
    query = f"SELECT * FROM {database.tests_t} WHERE id='{test_id}'"
    result = cursor.execute(query).fetchall()
    test_len = len(result)
    if question_number == 0:
        question_number += 1
    elif 0 < question_number <= test_len:
        user_answer = message.text
        query = f"SELECT ans_1 FROM {database.tests_t} WHERE id='{test_id}' AND number='{question_number}'"
        correct_answer = cursor.execute(query).fetchall()[0][0]
        if user_answer == correct_answer:
            score += 1
            bot.send_message(message.chat.id, messages.correct_answer_message)
        else:
            bot.send_message(message.chat.id, messages.incorrect_answer_message)
        question_number += 1
    if question_number > test_len:
        bot.send_message(message.chat.id, 'Тест окончен\nВерных ответов: ' + str(score) + ' из ' + str(test_len))
        database.set_status(message, config.wait)
        send_help(message)
    else:
        query = f"UPDATE {database.status_t} SET question_number='{question_number}', score='{score}'"
        cursor.execute(query)
        # send question
        query = f"SELECT question, ans_1, ans_2, ans_3, ans_4 FROM {database.tests_t} " \
                f"WHERE id='{test_id}' AND number='{question_number}'"
        result = list(cursor.execute(query).fetchall()[0])
        question = result[0]
        answers = result[1:]
        random.shuffle(answers)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(answers[0], answers[1])
        user_markup.row(answers[2], answers[3])
        bot.send_message(message.chat.id, question, reply_markup=user_markup)

    database.close_db(conn, cursor)



def select_test(message):
    conn, cursor = database.open_db(database.db_name)
    query = f"SELECT id from {database.tests_t}"
    result = [elem[0] for elem in cursor.execute(query).fetchall()]
    result = list(set(result))
    test_id = random.choice(result)
    query = f"UPDATE {database.status_t} SET test_id='{test_id}', question_number='0', score='0' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    query = f"SELECT interest FROM {database.users_t} WHERE id='{message.chat.id}'"
    interest = cursor.execute(query).fetchall()[0][0]
    bot.send_message(message.chat.id, interest)
    bot.send_message(message.chat.id, messages.test_info_message + test_id)
    database.close_db(conn, cursor)
    send_question(message)




@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message)
    database.set_status(message, config.name)
    bot.send_message(message.chat.id, messages.start_message)
    bot.send_message(message.chat.id, messages.name_message)

@bot.message_handler(commands=['help'])
def help(message):
    send_help(message)


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
        bot.send_message(message.chat.id, messages.finish_reg_message)
        send_help(message)
    elif status == config.wait:
        if message.text == messages.take_test:
            database.update_tests_table()
            database.set_status(message, config.take_test)
            select_test(message)
        elif message.text == messages.find_friends:
            database.set_status(message, config.find_friends)
            bot.send_message(message.chat.id, 'поиск друзей...')
    elif status == config.take_test:
        send_question(message)





bot.polling(none_stop=True)