import rsa

from src.server.Client_table import add_client


def receive_registration(message, private_key):
    message = rsa.decrypt(message, private_key)
    messages = str.split(message)
    if messages[0] != "REGISTER":
        print("Error in registration")
    else:
        add_client(messages[1], messages[2], messages[3], messages[4])
