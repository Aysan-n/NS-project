from Server import Server


class Client:

    def __init__(self, id, server):
        self.id = id
        self.server = server


    def send(self, message):
        self.server.respond(message)

    def register(self):

    def dh_key_exchange(self):




