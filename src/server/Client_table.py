import sqlite3


def create():
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("""CREATE TABLE clients(
            firstname text,
            lastname text,
            username text,
            encrypted_username tex
            password text
            )""")

    client_directory.commit()
    client_directory.close()


def add_client(first_name, last_name, username, password):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("INSERT INTO clients VALUES ('" + first_name + "', '" + last_name + "', '" +
                   username + "' , '"+password+"')")
    client_directory.commit()
    client_directory.close()


def find_client(username):
    client_directory = sqlite3.connect('clients.db')
    cursor = client_directory.cursor()
    cursor.execute("SELECT * FROM clients WHERE username = '"+username+"' ")
    return cursor.fetchone()
    client_directory.commit()
    client_directory.close()



