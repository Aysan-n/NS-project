import sqlite3
def create():
    try:
        connection=sqlite3.connect('key_management.db')
        cursor=connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS key_management_table
                      (file_name TEXT, key TEXT, iv TEXT);''')
        connection.commit()
        connection.close()
    except sqlite3.Error as error:
        print("Failed to connect sqliteDB", error)

    
def insert(file_name,key,iv):
    try:
        connection=sqlite3.connect('key_management.db')
        cursor=connection.cursor()
        sqlite_insert_with_param='''INSERT TABLE key_management_table(file_name,key,iv)
                      VALUES (?, ?, ?);'''
        data_tuple = (file_name,key,iv)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
        connection.close()
    except sqlite3.Error as error:
        print("Failed to insert data into key_management_table", error)

def find_key(file_name):
    try:
        connection=sqlite3.connect('key_management.db')
        cursor=connection.cursor()
        sql_select_query ='''SELECT key,iv FROM key_management_table WHERE file_name=?'''
        cursor.execute(sql_select_query, (file_name,))
        records=cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    except sqlite3.Error as error:
         print("Failed to read data from key_management_table)", error)
    



