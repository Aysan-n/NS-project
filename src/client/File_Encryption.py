from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import re
from key_managemnt_table import create,insert
def generate_key_iv():
    key=get_random_bytes(16)
    iv=get_random_bytes(16)
    return key,iv
def file_Encryption(file_address:str):
    file_name=re.findall(r'\w+\.\w+',file_address)
    with open(file_address,mode='rb') as file:
        orginal_file=file.read()
    key,iv=generate_key_iv()
    cipher=AES.new(key, AES.MODE_CBC, iv)
    enc=cipher.encrypt(pad(orginal_file,16,style='pkcs7'))
    create()
    insert(file_name[0],key,iv)
    return enc


