
req=[]

from Client_message_receiver import Client_buffer
while True:
    a=Client_buffer
    if len(a):
       req+=a
       print(req)
