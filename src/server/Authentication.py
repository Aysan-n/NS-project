import rsa

from Client_table import find_client, create_session_key_table, add_session_key
# from Crypto.Random import get_random_bytes
from Server_message_sender import Server_message_sender
from Server_message_receiver import Server_message_receiver
import hashlib
import datetime
import random
import os

from client.Messaging import deserialize


def authentication(messaging, connection):  ########################

    # server_nance=get_random_bytes(10)
    server_nance = os.urandom(10)

    ################    درصورت نیازف تبدیلی بر روی پیام دریافت شده
    server_message = {'message_type': 'authentication', 'server_nance': server_nance.hex()}

    #############    در صورت نیاز، تبدیل بر روی پیام سرور
    # client_address=client_message['client_address']

    messaging.send_message(server_message, connection)
    print(server_message)
    # Server_message_sender(client_address,server_message)
    # client_message=Server_message_receiver()
    client_message = deserialize(connection.recv(2048))
    ##########  در صورت لزوم، انجام عملیات بر روی پیام کلاینت

    print(client_message)
    client_info = find_client(client_message['client_user_name'])

    if client_info != 'Failed to find user':
        hash_string = (hashlib.sha1(server_nance + client_info[4].encode())).hexdigest()
        if hash_string == client_message['hash_string']:
            ################    عملیات رمز گشایی کلید جلسه
            try:
                create_session_key_table()
            except:
                print("Tabl")

            time_stamp = datetime.datetime.now()
            seq_number = random.randint(0, 2047)
            encrypted_session_key = bytes.fromhex(client_message['enc_str'])
            session_key = rsa.decrypt(encrypted_session_key, messaging.private_key)

            # UNCOMMENT!!!!!!
            add_session_key(client_info[2], session_key, seq_number, time_stamp)
            # UNCOMMENT!!!!!!

            ################### عملیات رمز بر روی seq numb

            print(client_info[4])

            hash_string = (hashlib.sha1(client_info[4].encode() + seq_number.to_bytes(2, 'big'))).hexdigest()

            enc_string = 

            server_message = {'message_type': 'authentication', 'status': 'ok', 'hash_string': hash_string,
                              'enc_str': enc_string}

            messaging.send_message(server_message)
            # Server_message_sender(client_address,server_message)

        else:
            server_message = {'message_type': 'authentication', 'status': 'error'}
            messaging.send_message(server_message)
            # Server_message_sender(client_address,server_message)

    else:
        server_message = {'message_type': 'authentication', 'status': 'error'}
        messaging.send_message(server_message)
        # Server_message_sender(client_address,server_message)
