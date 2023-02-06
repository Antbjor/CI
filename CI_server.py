import socket
import yaml


class CIServer:
    def __init__(self, port):
        self.port = port
        self.s = socket.socket()
        self.s.bind(('', self.port))

    def connection(self):
        self.s.listen()
        while True:
            self.client, self.client_addr = self.s.accept()
            print("Client: ", self.client_addr, " connected")
            self.parse_inc_data(self.client.recv(1024))

    def parse_inc_data(self, raw_data):
        data = raw_data.decode()
        print(data) 


with open('config.yml') as fin:
    data = yaml.load(fin, Loader=yaml.FullLoader)
PORT = data["PORT"]
server = CIServer(PORT)
server.connection()
