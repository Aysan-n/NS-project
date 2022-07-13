import rsa

from server.Client_table import add_client


def receive_registration(message, private_key):
    if message['message_type'] != 'registration':
        print("Error in registration")
        return
    else:
        message = message['cipher']

        message = bytes.fromhex(message)
        message = rsa.decrypt(message, private_key).decode()
        messages = str.split(message)
        print(messages[0], messages[1], messages[2], messages[3])
        add_client(messages[0], messages[1], messages[2], messages[3])
