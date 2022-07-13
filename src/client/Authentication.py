
from Client_message_sender import Client_message_sender
from Client_message_receiver import Client_message_receiver  ############
import hashlib
import os
from Crypto.Random import get_random_bytes
def client_auth(client_user_name:str,client_pwd:bytes):
    client_address= os.getcwd()+'src/client'
    client_message={'message_type':'authentication','client_address':client_address}
    ###############################    بر اساس پیام دریافتی
    Client_message_sender(client_message)
    server_message=Client_message_receiver()
    hash_string=(hashlib.sha1(server_message['server_nance']+client_pwd)).hexdigest()     #string
    session_key=get_random_bytes(16)
    ################### عملیات دریافت کلید عمومی، و رمز کردن کلید جلسه
    ########################
    client_message={'message_type':'authentication','client_user_name':client_user_name,'client_address':client_address,'hash_string':hash_string,'enc_str':enc_string}###### نیاز به کامل شدن
    Client_message_sender(client_message)
    server_message=Client_message_receiver()
    if server_message['status']!='error':
        enc_string=server_message['enc_str']
        ############# عملیات رمز گشایی و بدست آوردن seq num
        hash_string=(hashlib.sha1(seq_number.encode()+client_pwd)).hexdigest()
        if hash_string==server_message['hash_string']:
            return seq_number,session_key
        else:
            return False
    else:
        return False






