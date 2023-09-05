import socket

from shared.NetConstants import *

class ServerAPI:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.settimeout(0.5)

        self.is_authenticated = False

        self.server_socket.connect((IP, PORT))
        print("Connected to server")

    def CheckConnection(self):
        self.server_socket.send(PING_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            return data == PING_RES
        
        except socket.timeout:
            return False

    def Login(self, username, password):
        self.server_socket.send((LOGIN_REQ + username + ';' + password).encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data == LOGIN_RES_TRUE):
                self.is_authenticated = True
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def Register(self, username, password, email):
        self.server_socket.send((REGISTER_REQ + username + ';' + password + ';' + email).encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data == REGISTER_RES_TRUE):
                self.is_authenticated = True
                return True
            else:
                return False
        
        except socket.timeout:
            return False