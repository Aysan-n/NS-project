from tkinter.tix import TEXT
from Client_table import find_auth_user,delete_auth_user
from seq_number_enc_dec import seq_Decryption
import datetime
import os
def server_command_handler(client_message):
    client_user_name=client_message['client_user_name']
    record=find_auth_user(client_user_name)
    if len(record)==0:       ###عدم احراز اصالت کاربر
        return False
    current_time=datetime.datetime.now()
    time_stamp=record[3]
    delta_time=current_time-time_stamp
    max_delta_time=datetime.timedelta(seconds=7200)
    if delta_time>max_delta_time:
        delete_auth_user(client_user_name)
        return False      ## منقضی شدن احراز اصالت
    session_key=record[1]
    seq_number=record[2]
    enc_seq_number=client_message['enc_seq_num']
    dec_seq_num=seq_Decryption(enc_seq_number,session_key)
    if dec_seq_num!=seq_number+1:
        return False     ##کاریر نامعتبر
    cwd_total=os.getcwd()+'src/sever/Repository/'+record[4]+record[5]
    if client_message['command_type']!='mv':
        path=client_message['path']
        path_list=path.split('/')
        cwd_list=record[5].split('/')[1:]   ##################### جدول باید درست شود
        if path_list.count('..')>(len(cwd_list))-1:
            return False     #دسترسی غیر مجازی
    else:
        access_path=client_message['access_path']
        dest_path=client_message['dest_path']
        access_path_list=access_path.split('/')
        dest_path_list=dest_path.split('/')
        cwd_list=record[5].split('/')[1:]   ##################### جدول باید درست شود
        if access_path_list.count('..')>(len(cwd_list))-1 or dest_path_list.count('..')>(len(cwd_list))-1:
            return False     #دسترسی غیر مجازی
    critical_path=os.getcwd()+'src/sever/Repository/'+record[4]
import subprocess
command=['dir']
#print(subprocess.call("der C:\\",shell=True))
#from subprocess import check_output
#a=check_output("dir C:\\", shell=True).decode()
#print(type(a))
#process=subprocess.Popen("der C:\\",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#process.wait()
#output, error = process.communicate()
#print(error,   type(output))
print(os.getcwd()+'src/sever/Repository/'+'u2546')


    


