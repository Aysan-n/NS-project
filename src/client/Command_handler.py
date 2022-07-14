import re
from File_Encryption import Encryption
from key_managemnt_table import find_file
def command_handler(client_command:str,seq_num:int,session_key:bytes):
    command_string=client_command
    support_command=['mkdir','touch','cd','ls','rm','mv']
    client_command=re.findall(r'^\w+',command_string)
    if client_command not in support_command:
        return False
    if client_command in ['mkdir','touch','cd','ls']:
        path=re.findall(r'\s(.+$)',command_string)
        directory_name=path[0].split('/')
        enc_dir_name=[]
        for dir_name in directory_name:
            if dir_name=='..' or dir_name=='.':
                enc_dir_name+=[dir_name]
            else:
                record=find_file(dir_name)
                if len(record)==0 and (client_command=='cd' or client_command=='ls'):
                    return False
                elif len(record)==0:
                    enc_dir_name+=[Encryption(dir_name)]
                else:
                    enc_dir_name+=[record[1]]
        enc_path='/'.join(enc_dir_name)
        client_message={'message_type':'client_command','command':client_command+enc_path}
        ######################### فرستادن پیام ++++ می توان بر روی نتیجه حاصل عملیات انجام داد
    if client_command=='rm':
        path=re.findall(r'\s-{0,1}\w{0,1}\s{0,1}(.+$)',command_string)
        directory_name=path[0].split('/')
        enc_dir_name=[]
        for dir_name in directory_name:
            if dir_name=='..' or dir_name=='.':
                enc_dir_name+=[dir_name]
            else:
                record=find_file(dir_name)
                if len(record)==0:
                    return False
                else:
                    enc_dir_name+=[record[1]]
        enc_path='/'.join(enc_dir_name)
        command_flag=re.findall(r'\s(-{0,1}\w{0,1})\s{0,1}.+$',command_string)
        client_message={'message_type':'client_command','command':client_command+command_flag[0]+enc_path}
            #####################
    if client_command=='mv':
        access_path=re.findall(r'\s-{0,1}\w{0,1}\s{0,1}(.+)\s',command_string)
        dest_path=re.findall(r'\s-{0,1}\w{0,1}\s{0,1}.+\s(.+)',command_string)
        access_directory_name=access_path[0].split('/')
        dest_directory_name=dest_path[0].split('/')
        enc_access_dir_name=[]
        enc_des_dir_name=[]
        for dir_name in access_directory_name:
            if dir_name=='..' or dir_name=='.':
                enc_access_dir_name+=[dir_name]
            else:
                record=find_file(dir_name)
                if len(record)==0:
                    return False
                else:
                    enc_access_dir_name+=[record[1]]
        for dir_name in dest_directory_name:
            if dir_name=='..' or dir_name=='.':
                enc_des_dir_name+=[dir_name]
            else:
                record=find_file(dir_name)
                if len(record)==0:
                    enc_dir_name+=[Encryption(dir_name)]
                else:
                    enc_access_dir_name+=[record[1]]  
        enc_access_path='/'.join(enc_access_dir_name)
        enc_dest_path='/'.join(enc_des_dir_name)
        command_flag=re.findall(r'\s(-{0,1}\w{0,1})\s{0,1}.+$',command_string)
        client_message={'message_type':'client_command','command':client_command+command_flag[0]+enc_access_path+enc_dest_path}
        ################################
        
