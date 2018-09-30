import sqlite3
import glob

import config

# start database's tables names
db_name = 'pixel.db'
users_t = 'users'
status_t = 'status'
tests_t = 'tests'
files_t = 'files'

# end tables names

def open_db(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return conn, cursor
def close_db(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def create_users_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {users_t} (id varchar, name varchar, age varchar, gender varchar, interest varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)
def create_status_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {status_t} (id varchar, status varchar, test_id varchar, question_number varchar, " \
            f"score varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)
# User's main info
def add_user(message):
    conn, cursor = open_db(db_name)
    check = f"SELECT * FROM {users_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(check).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {users_t} (id) VALUES ('{message.chat.id}')"
        cursor.execute(query)
    close_db(conn, cursor)




def set_name(message):
    conn, cursor = open_db(db_name)
    query = f"UPDATE {users_t} SET name='{message.text}' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    close_db(conn, cursor)
def set_age(message):
    conn, cursor = open_db(db_name)
    query = f"UPDATE {users_t} SET age='{message.text}' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    close_db(conn, cursor)
def set_gender(message):
    conn, cursor = open_db(db_name)
    query = f"UPDATE {users_t} SET gender='{message.text}' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    close_db(conn, cursor)
def set_interest(message):
    conn, cursor = open_db(db_name)
    query = f"UPDATE {users_t} SET interest='{message.text}' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    close_db(conn, cursor)


def set_status(message, status):
    conn, cursor = open_db(db_name)
    check = f"SELECT * FROM {status_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(check).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {status_t} (id, status) VALUES ('{message.chat.id}', '{status}')"
    else:
        query = f"UPDATE {status_t} SET status='{status}' WHERE id='{message.chat.id}'"
    cursor.execute(query)
    close_db(conn, cursor)
def get_status(message):
    conn, cursor = open_db(db_name)
    try:
        query = f"SELECT status FROM {status_t} WHERE id='{message.chat.id}'"
        result = cursor.execute(query).fetchall()[0][0]
        close_db(conn, cursor)
        return result
    except:
        pass
    return config.wait

def create_tests_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {tests_t} (id varchar, number varchar, question varchar, " \
            f"ans_1 varchar, ans_2 varchar, ans_3 varchar, ans_4 varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)
def create_files_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {files_t} (file_name varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)
def update_tests_table():
    conn, cursor = open_db(db_name)
    query = f"SELECT * from {files_t}"
    result = [elem[0] for elem in cursor.execute(query).fetchall()]
    files = glob.glob('tests/*.txt')
    for file in files:
        if file not in result:
            query = f"INSERT INTO {files_t} (file_name) VALUES ('{file}')"
            cursor.execute(query)
            f = open(file, 'r')
            content = f.read()
            lines = content.split('\n')
            id = int(lines[0])
            n = int(lines[1])
            for i in range(n):
                q = lines[2 + 5*i]
                num = i + 1
                ans_1 = lines[3 + 5*i]
                ans_2 = lines[4 + 5*i]
                ans_3 = lines[5 + 5*i]
                ans_4 = lines[6 + 5*i]
                query = f"INSERT INTO {tests_t} (id, number, question, ans_1, ans_2, ans_3, ans_4) " \
                        f"VALUES ('{id}', '{num}', '{q}', '{ans_1}', '{ans_2}', '{ans_3}', '{ans_4}')"
                cursor.execute(query)
    close_db(conn, cursor)



create_users_table()
create_status_table()
create_tests_table()
create_files_table()
