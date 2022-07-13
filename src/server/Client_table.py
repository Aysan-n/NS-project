import sqlite3


def create():
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("""CREATE TABLE clients(
            firstname text,
            lastname text,
            username text,
            encrypted_username text,
            password text
            );""")

    client_directory.commit()
    client_directory.close()
def create_session_key_table():
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("""CREATE TABLE session_keys(
            user_name text,
            session_key text,
            seq_num  INTEGER,
            joiningDate timestamp
            );""")

    client_directory.commit()
    client_directory.close()
def add_session_key(user_name, session_key, joiningDate):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    sqlite_insert_with_param = """INSERT INTO session_key
                          (user_name,session_key, joiningDate) 
                          VALUES (?, ?, ?);"""
    data_tuple = (user_name, session_key, joiningDate)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    client_directory.commit()
    client_directory.close()

def add_client(first_name, last_name, username, password):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("INSERT INTO clients VALUES ('" + first_name + "', '" + last_name + "', '" +
                   username + "' , '"+password+"');")
    client_directory.commit()
    client_directory.close()


def find_client(username):
    try:
        client_directory = sqlite3.connect('clients.db')
        cursor = client_directory.cursor()
        cursor.execute("SELECT * FROM clients WHERE username = '"+username+"' ")
        return cursor.fetchone()
        client_directory.close()
    except:
        error='Failed to find user'
        return error



