import socket

from shared.NetConstants import *

class ServerAPI:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.settimeout(0.5)

        self.server_socket.connect((IP, PORT))
        print("Connected to server")

    def CheckConnection(self):
        self.server_socket.send(b"ping")
        try:
            self.server_socket.recv(1024)
            
            return True
        except socket.timeout:
            return False

    def Login(self, username, password):
        pass