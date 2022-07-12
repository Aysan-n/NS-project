import rsa


def initiate_registration(pub_key, first_name, last_name, username, password):
    send_to_server(rsa.encrypt(build_message(first_name, last_name
                                             , username, password), pub_key))


def build_message(first_name, last_name, username, password):
    return "REGISTER " + first_name + " " + last_name + " " + username + " " + password
