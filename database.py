import sqlite3

# start database's tables names
db_name = 'pixel_db.db'
users_t = 'users'

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
def add_user(message):
    conn, cursor = open_db(db_name)
    check = f"SELECT * FROM {users_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(check).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {users_t} (id) VALUES ('{message.chat.id}')"
        cursor.execute(query)
    close_db(conn, cursor)



create_users_table()