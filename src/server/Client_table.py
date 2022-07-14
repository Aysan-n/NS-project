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
            cwd text
            );""")

    client_directory.commit()
    client_directory.close()


def delete_auth_user(client_user_name):
    connection = sqlite3.connect('clients.db')
    cursor = connection.cursor()
    sql_select_query = """DELETE from session_keys where user_name=?"""
    cursor.execute(sql_select_query, (client_user_name,))
    connection.commit()
    cursor.close()
    connection.close()


def find_auth_user(client_user_name):
    connection = sqlite3.connect('clients.db')
    cursor = connection.cursor()
    sql_select_query = '''SELECT * FROM session_keys WHERE user_name=?'''
    cursor.execute(sql_select_query, (client_user_name,))
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


def add_session_key(user_name, session_key, seq_num, joiningDate):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    sqlite_insert_with_param = """INSERT INTO session_keys
                          (user_name,session_key,seq_num, joiningDate) 
                          VALUES (?, ?, ?, ?);"""
    data_tuple = (user_name, session_key, seq_num, joiningDate)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    client_directory.commit()
    client_directory.close()


def add_client(first_name, last_name, username, password):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("INSERT INTO clients VALUES ('" + first_name + "', '" + last_name + "', '" +
                   username + "' , '" + password + "');")
    client_directory.commit()
    client_directory.close()


def find_client(username):
    try:
        client_directory = sqlite3.connect('clients.db')
        cursor = client_directory.cursor()
        cursor.execute("SELECT * FROM clients WHERE username = '" + username + "' ")
        return cursor.fetchone()
        client_directory.close()
    except:
        error = 'Failed to find user'
        return error
