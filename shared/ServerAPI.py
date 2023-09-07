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
                self.username = username
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
                self.username = username
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def GetUsername(self):
        return self.username
        
    def GetAvailableRooms(self):
        self.server_socket.send(GET_AVAILABLE_ROOMS_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data.startswith(GET_AVAILABLE_ROOMS_RES)):
                return data[len(GET_AVAILABLE_ROOMS_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []
        
    def CreateRoom(self):
        self.server_socket.send(ADD_ROOM_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data == ADD_ROOM_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def JoinRoom(self, roomname):
        self.server_socket.send((JOIN_ROOM_REQ + roomname).encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data == JOIN_ROOM_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        

    def GetHostUsername(self):
        self.server_socket.send(GET_HOST_USERNAME_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data.startswith(GET_HOST_USERNAME_RES)):
                return data[len(GET_HOST_USERNAME_RES):]
            else:
                return None
        
        except socket.timeout:
            return None
    
    def GetUsersInMyRoom(self):
        self.server_socket.send(GET_USERS_IN_MY_ROOM_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data.startswith(GET_USERS_IN_MY_ROOM_RES)):
                return data[len(GET_USERS_IN_MY_ROOM_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []
        
    def SetGameSettings(self, num_of_mines, boardsize):
        self.server_socket.send((SET_GAME_SETTINGS_REQ + str(num_of_mines) + ';' + str(boardsize)).encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data == SET_GAME_SETTINGS_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def GetGameSettings(self):
        self.server_socket.send(GET_GAME_SETTINGS_REQ.encode())
        try:
            data = self.server_socket.recv(1024).decode()
            print(data)
            if(data.startswith(GET_GAME_SETTINGS_RES)):
                return data[len(GET_GAME_SETTINGS_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []