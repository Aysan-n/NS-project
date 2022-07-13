import rsa


def initiate_registration(messaging, pub_key, first_name, last_name, username, password):
    cipher = rsa.encrypt(build_message(first_name, last_name, username, password).encode(), pub_key).hex()
    messaging.send_message({'message_type': 'registration', 'cipher': cipher})


def build_message(first_name, last_name, username, password):
    return first_name + " " + last_name + " " + username + " " + password
