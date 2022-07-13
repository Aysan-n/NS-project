import sys
def Server_message_sender(client_address,message):
    sys.path.append(client_address)
    from Client_message_receiver import Client_message_receiver
    Client_message_receiver(message)



Server_message_sender('C:/Users/Ali/NDS_project/NS-project/src/client','ali akbar')