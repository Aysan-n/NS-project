Client_buffer=[]
def Client_message_receiver(message:str):
    Client_buffer.append(message)
def receive_from(): 
    while True:
        if len(Client_buffer):
            break
    return Client_buffer.pop()

    
    

    
       

      


    




 
