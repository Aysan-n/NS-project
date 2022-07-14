import rsa
import random

from server.Client_table import add_client, table_contains


def receive_registration(messaging, connection, message, private_key):
    if message['message_type'] != 'registration':
        print("Error in registration")
        server_message = {'message_type': 'registration', 'status': 'failed'}
        messaging.send_message(server_message, connection)
        return
    else:
        message = message['cipher']
        message = bytes.fromhex(message)
        message = rsa.decrypt(message, private_key).decode()
        messages = str.split(message)
        if table_contains(messages[2]):
            server_message = {'message_type': 'registration', 'status': 'failed'}
            messaging.send_message(server_message, connection)
        else:
            enc_username = 'u' + str(random.randint(1, 1000))
            print(messages[0], messages[1], messages[2], messages[3])
            add_client(messages[0], messages[1], messages[2], messages[3], enc_username)
            server_message = {'message_type': 'registration', 'status': 'ok'}
            messaging.send_message(server_message, connection)
