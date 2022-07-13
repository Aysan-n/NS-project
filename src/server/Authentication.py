
from Client_table import find_client,create_session_key_table,add_session_key
from Crypto.Random import get_random_bytes
from Server_message_sender import Server_message_sender
from Server_message_receiver import Server_message_receiver
import hashlib
import datetime
import random
def authentication(client_message): ########################
    server_nance=get_random_bytes(10)
    ################    درصورت نیازف تبدیلی بر روی پیام دریافت شده
    server_message={'message_type':'authentication','server_nance':server_nance}
    #############    در صورت نیاز، تبدیل بر روی پیام سرور
    client_address=client_message['client_address']
    Server_message_sender(client_address,server_message)
    client_message=Server_message_receiver()
    ##########  در صورت لزوم، انجام عملیات بر روی پیام کلاینت
    client_info=find_client(client_message['client_user_name'])
    if client_info!='Failed to find user':
        hash_string=(hashlib.sha1(server_nance+client_info[4].encode())).hexdigest()
        if hash_string==client_message['hash_string']:
            ################    عملیات رمز گشایی کلید جلسه
            create_session_key_table()
            time_stamp=datetime.datetime.now()
            seq_number=random.randint(0,100000)
            add_session_key(client_info[2],session_key,seq_number,time_stamp)
            ################### عملیات رمز بر روی seq numb
            hash_string=(hashlib.sha1(client_info[4].encode()+seq_number.encode())).hexdigest()
            server_message={'message_type':'authentication','status':'ok','hash_string':hash_string,'enc_str':enc_string}
            Server_message_sender(client_address,server_message)
        else:
            server_message={'message_type':'authentication','status':'error'}
            Server_message_sender(client_address,server_message)
    else:
        server_message={'message_type':'authentication','status':'error'}
        Server_message_sender(client_address,server_message)        









