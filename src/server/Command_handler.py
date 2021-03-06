import json
from tkinter.tix import TEXT
from Client_table import find_auth_user, delete_auth_user, update_cwd, find_client
from seq_number_enc_dec import seq_Decryption
import datetime
import os
import subprocess
import re
def server_command_handler(client_message):
    client_user_name=client_message['client_user_name']
    record=find_auth_user(client_user_name)
    client_record=find_client(client_user_name)
    critical_path=os.getcwd()+'/src/server/Repository/'+client_record[3]
    
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
    if client_message['command_type']!='mv':
        path=client_message['path']
        path_list=path.split('/')
        cwd_list=record[5].split('/')[1:]   ##################### جدول باید درست شود
        if path_list.count('..')>(len(cwd_list))-1:
            return False     #دسترسی غیر مجازی
        elif len(lcs(critical_path,path)>0 and critical_path.find(path)==0):
            return False   ######دسترسی غیر مجاز
    else:
        access_path=client_message['access_path']
        dest_path=client_message['dest_path']
        access_path_list=access_path.split('/')
        dest_path_list=dest_path.split('/')
        cwd_list=record[5].split('/')[1:]   ##################### جدول باید درست شود
        if access_path_list.count('..')>(len(cwd_list))-1 or dest_path_list.count('..')>(len(cwd_list))-1:
            return False     #دسترسی غیر مجازی
        elif (len(lcs(critical_path,access_path)>0 and critical_path.find(access_path)==0)) or (len(lcs(critical_path,dest_path)>0 and critical_path.find(dest_path)==0)):
            return False    ###دسترسی غیر مجاز
    cwd_total=os.getcwd()+'/src/server/Repository/'+client_record[3]+record[5]    
 


def server_command_handler(connection, client_message):

    client_user_name = client_message['client_user_name']
    record = find_auth_user(client_user_name)
    client_record = find_client(client_user_name)
    critical_path = os.getcwd() + '/src/server/Repository/' + client_record[3]

    if len(record) == 0:  ###عدم احراز اصالت کاربر
        return False

    current_time = datetime.datetime.now()

    time_stamp = record[3]
    print(time_stamp)

    time_stamp = datetime.datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S.%f")

    delta_time = current_time - time_stamp

    max_delta_time = datetime.timedelta(seconds=7200)
    if delta_time > max_delta_time:
        delete_auth_user(client_user_name)
        return False  ## منقضی شدن احراز اصالت
    session_key = record[1]
    seq_number = record[2]
    enc_seq_number = bytes.fromhex(client_message['enc_seq_num'])
    dec_seq_num = seq_Decryption(enc_seq_number, session_key)

    if dec_seq_num != seq_number + 1:
        return False  ##کاریر نامعتبر
    if client_message['command_type'] != 'mv':
        path = client_message['path']
        path_list = path.split('/')
        cwd_list = record[5].split('/')[1:]  ##################### جدول باید درست شود
        if path_list.count('..') > (len(cwd_list)) - 1:
            return False  # دسترسی غیر مجازی
        elif len(lcs(critical_path, path) > 0 and critical_path.find(path) == 0):
            return False  ######دسترسی غیر مجاز
    else:
        access_path = client_message['access_path']
        dest_path = client_message['dest_path']
        access_path_list = access_path.split('/')
        dest_path_list = dest_path.split('/')
        cwd_list = record[5].split('/')[1:]  ##################### جدول باید درست شود
        if access_path_list.count('..') > (len(cwd_list)) - 1 or dest_path_list.count('..') > (len(cwd_list)) - 1:
            return False  # دسترسی غیر مجازی
        elif (len(lcs(critical_path, access_path) > 0 and critical_path.find(access_path) == 0)) or (
        len(lcs(critical_path, dest_path) > 0 and critical_path.find(dest_path) == 0)):
            return False  ###دسترسی غیر مجاز
    cwd_total = os.getcwd() + '/src/server/Repository/' + client_record[3] + record[5]


def ls_handler(cwd_total, client_message):
    path = client_message['path']
    if len(path) == 0:
        pass
    elif path[0] == '/':
        path = path[1:]
    cwd_total = cwd_total.replace('/', '\\')
    path = path.replace('/', '\\')
    with cd(cwd_total):
        process = subprocess.Popen(["dir", "%s" % path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    output, error = process.communicate()
    if len(error) != 0:
        return False  # دستور دچار خطا شد
    else:
         result=re.sub(r'.*\r\n\r\n','',output.decode())
         result=re.sub(r'^\s{0,1}.*?\.\r\n','',result)  ########## خروجی رو درست کن سپس بفرست
         print(result)


def cd_handler(cwd_total, critical_path, client_message):
    savedPath = os.getcwd()
    os.chdir(cwd_total)
    path = client_message['path']
    if path[0] == '/':
        path = path[1:]
    path = path.replace('/', '\\')
    os.chdir(path)
    new_cwd = os.getcwd()
    os.chdir(savedPath)
    critical_path = critical_path.replace('/', '\\')
    critical_path = critical_path.split('\\')
    new_cwd = new_cwd.split('\\')
    new_cwd = new_cwd[len(critical_path):]
    new_cwd = '/' + '/'.join(new_cwd)
    client_user_name = client_message['client_user_name']
    update_cwd(client_user_name, new_cwd)
    return True


def touch_handler(cwd_total, client_message):
    path = client_message['path']
    if path[0] == '/':
        path = path[1:]
    path = path.replace('/', '\\')
    path = path.split('\\')
    file_name = path.pop()
    if len(path) == 0:
        savedPath = os.getcwd()
        os.chdir(cwd_total)
        new_path = os.getcwd()
    else:
        savedPath = os.getcwd()
        os.chdir(cwd_total)
        path = '\\'.join(path)
        os.chdir(path)
        new_path = os.getcwd()
    os.chdir(savedPath)
    with cd(new_path):
        process = subprocess.Popen('type nul >> "%s.txt"' % file_name, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.wait()
    output, error = process.communicate()
    if len(error) > 0:
        return False  ########### خطای اجرا کد
    return True


#fixed
def mkdir_handler(cwd_total, client_message):
    path = client_message['path']
    if path[0] == '/':
        path = path[1:]
    with cd(cwd_total):
        return os.makedirs(path)
def rm_handler(cwd_total,client_message):
    path=client_message['path']
    if path[0]=='/':
        path=path[1:]
    path=os.path.join(cwd_total,path)
    path=path.replace('/','\\')
    if client_message['command_flag']=='-r':
        process=subprocess.Popen(['rmdir','/s','/q','%s' %path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        output,error=process.communicate()
        if len(error)==0:
            return False
        else:
            return True
    try:
        os.remove(path+'.txt')
        return True
    except:
        return False

def mv_handler(cwd_total,client_message):
    access_path=client_message['access_path']
    dest_path=client_message['dest_path']
    if access_path[0]=='/':
        access_path=access_path[1:]
    if dest_path[0]=='/':
        dest_path=dest_path[1:]    
    access_path=os.path.join(cwd_total,access_path)
    access_path=access_path.replace('/','\\')
    dest_path_from_access_path=re.findall(r'(.*)\\\w+$',access_path)[0]
    dest_path=os.path.join(dest_path_from_access_path,dest_path)
    dest_path=dest_path.replace('/','\\')
    if client_message['command_flag']=='-r':
        try:
            process=subprocess.Popen(['move','%s' %access_path,'%s' %dest_path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
               return False
            else:
               return True
        except:
            return False
    else:
        try:
            access_path+='.txt'
            process=subprocess.Popen(['move','%s' %access_path,'%s' %dest_path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
                return False
            else:
                return True
        except:
            return False

        
        
        
 def ls_handler_linux(cwd_total, client_message):
    path = client_message['path']
    if len(path) == 0:
        pass
    elif path[0] == '/':
        path = path[1:]
    with cd(cwd_total):
        process = subprocess.Popen(["ls","-l", "%s" % path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    output, error = process.communicate()
    if len(error) != 0:
        return False  # دستور دچار خطا شد
    else:
         result=re.sub(r'.*\r\n\r\n','',output.decode())
         result=re.sub(r'^\s{0,1}.*?\.\r\n','',result)  ########## خروجی رو درست کن سپس بفرست
         print(result)

def rm_handler_linux(cwd_total,client_message):
    path=client_message['path']
    if path[0]=='/':
        path=path[1:]
    path=os.path.join(cwd_total,path)
    if client_message['command_flag'] == '-r':
        process=subprocess.Popen(['rm','-rf','%s' %path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        output,error=process.communicate()
        print(error.decode())
        if len(error)==0:

            return False
        else:
            return True
    try:
        print("***")
        os.remove(path+'.txt')
        return True
    except:
        print("**")
        return False
        

def mv_handler_linux(cwd_total,client_message):
    access_path=client_message['access_path']
    dest_path=client_message['dest_path']
    if access_path[0]=='/':
        access_path=access_path[1:]
    if dest_path[0]=='/':
        dest_path=dest_path[1:]
    access_path=os.path.join(cwd_total,access_path)

    print(re.findall(r'(.*)//\w+$',access_path))

    dest_path_from_access_path=re.findall(r'(.*)/\w+$',access_path)[0]
    dest_path=os.path.join(dest_path_from_access_path,dest_path)
    if client_message['command_flag']=='-r':
        try:
            process=subprocess.Popen(['mv','%s' %access_path,'%s' %dest_path], shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
                print(error.decode())
                return False
            else:
               return True
        except:
            return False
    else:
        try:
            access_path+='.txt'
            process=subprocess.Popen(['mv','%s' %access_path,'%s' %dest_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
                print(error.decode())
                return False
            else:
                return True
        except:
            print(error.decode())
            return False



class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


import subprocess

command = ['dir']


# print(subprocess.call("der C:\\",shell=True))
# from subprocess import check_output
# a=check_output("dir C:\\", shell=True).decode()
# print(type(a))
# process=subprocess.Popen("der C:\\",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# process.wait()
# output, error = process.communicate()
# print(error,   type(output))

def lcs(S, T):
    m = len(S)
    n = len(T)
    counter = [[0] * (n + 1) for x in range(m + 1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i - c + 1:i + 1])
                elif c == longest:
                    lcs_set.add(S[i - c + 1:i + 1])

    return lcs_set

print(os.getcwd())



#######################################################
def mv_handler(cwd_total,client_message):
    access_path=client_message['access_path']
    dest_path=client_message['dest_path']
    if access_path[0]=='/':
        access_path=access_path[1:]
    if dest_path[0]=='/':
        dest_path=dest_path[1:]    
    access_path=os.path.join(cwd_total,access_path)
    access_path=access_path.replace('/','\\')
    dest_path=os.path.join(cwd_total,dest_path)
    dest_path=dest_path.replace('/','\\')
    if client_message['command_flag']=='-r':
        try:
            process=subprocess.Popen(['move','%s' %access_path,'%s' %dest_path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
               return False
            else:
               return True
        except:
            return False
    else:
        try:
            access_path+='.txt'
            process=subprocess.Popen(['move','%s' %access_path,'%s' %dest_path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            output,error=process.communicate()
            if len(error)!=0:
                return False
            else:
                return True
        except:
            return False
    


