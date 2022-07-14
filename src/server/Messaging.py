import socket
import threading
import time

from client.Messaging import serialize, deserialize
from server.Authentication import authentication
from server.Registration import receive_registration


class Messaging:

    def __init__(self, private_key):
        self.socket = None
        self.reqs = []
        self.connections = []
        self.private_key = private_key

    def create_socket(self, port):
        self.socket = socket.socket()
        print("Server socket created")
        self.socket.bind(('', port))

    def start_receiving(self):
        self.socket.listen()
        print("Server is listening")

        while True:
            c, addr = self.socket.accept()
            message = c.recv(2048)
            message = deserialize(message)
            print(message)
            self.reqs.append(message)
            self.connections.append(c)
            #print("appended")

    def send_message(self, message, c):
        print("***")
        c.send(serialize(message))

    def handle_registration(self, request):
        receive_registration(request, self.private_key)

    def handle(self, request, connection):
        if request['message_type'] == 'registration':
            self.handle_registration(request)

        elif request['message_type'] == 'authentication':
            authentication(self, connection)
        else:
            print("ERROR")
        connection.close()

    def handle_tasks(self):
        while True:
            if len(self.reqs) != 0:
                request = self.reqs.pop()
                connection = self.connections.pop()
                self.handle(request, connection)
            else:
                #print(len(self.reqs))
                time.sleep(2)

    def start(self):
        thread = threading.Thread(target=self.start_receiving, args=())
        thread.start()
        self.handle_tasks()
