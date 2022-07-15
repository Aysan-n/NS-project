import time

from rsa import PublicKey

from Command_handler import command_handler
from Authentication import client_auth
from Messaging import Messaging
from Registration import initiate_registration
import os
import rsa



# public_key = PublicKey(
#     94057119611095946281523367855001930801008421995257743937642282436572904657606798603159545412659607974565461332313984750403479192213716994833909001676613969160857359369527054950459340417810569591327134941274724766743027563401125940872842341580457651667285658979777888792614809061606256624792008312706379659423,
#     65537)


with open(os.getcwd()+'/src/client/public_key.pem') as file:
    data = file.read()
public_key = rsa.PublicKey.load_pkcs1_openssl_pem(data)

messaging = Messaging()
messaging.create_socket(2548)

initiate_registration(messaging, public_key, "Aysan", "Nishai", "Ays", "ays123")

#
password = "ays123"

seq_number, session_key = client_auth(messaging, public_key, "Ays", password)

command_handler(messaging, 'mkdir /very6', seq_number, session_key, "Ays")





