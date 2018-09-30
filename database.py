import sqlite3

# start database's tables names
db_name = 'pixel.db'
users_t = 'users'
status_t = 'status'

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
    query = f"CREATE TABLE {users_t} (id varchar, name varchar, age varchar, sex varchar)"
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

def add_user(message):
    conn, cursor = open_db(db_name)
    check = f"SELECT * FROM {users_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(check).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {users_t} (id) VALUES ('{message.chat.id}')"
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
    return '0'



create_users_table()
create_status_table()
