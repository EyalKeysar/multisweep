import socket

from shared.NetConstants import *
from Server.Client import Client

class ServerNetHandler:
    def __init__(self, port=SERVER_PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.in_AcceptClient = False

        self.clients = []

    def AcceptClient(self):
        print("listening for clients")
        self.in_AcceptClient = True
        try:
            client_socket, address = self.server_socket.accept()

            client = Client(client_socket, address)
            self.clients.append(client)

            print(f"Client {address} connected")

            self.in_AcceptClient = False
            return client_socket
        
        except socket.timeout:
            print("AcceptClient timeout")
            self.in_AcceptClient = False
            return None
        