import sys,os
def Client_message_sender(message):
    server_path= os.getcwd()+'/src/server'
    sys.path.append(server_path)
    from Server_message_receiver import Server_message_receiver
    Server_message_receiver(message)
