import socket

from shared.NetConstants import *
from shared.socket_protocol import send, recv

class ServerAPI:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.settimeout(0.5)

        self.is_authenticated = False

        self.server_socket.connect((IP, PORT))
        print("Connected to server")

    def CheckConnection(self):
        send(self.server_socket, PING_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            return data == PING_RES
        
        except socket.timeout:
            return False

    def Login(self, username, password):
        send(self.server_socket, (LOGIN_REQ + username + ';' + password).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == LOGIN_RES_TRUE):
                self.is_authenticated = True
                self.username = username
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def Register(self, username, password, email):
        send(self.server_socket, (REGISTER_REQ + username + ';' + password + ';' + email).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
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
        send(self.server_socket, GET_AVAILABLE_ROOMS_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data.startswith(GET_AVAILABLE_ROOMS_RES)):
                return data[len(GET_AVAILABLE_ROOMS_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []
        
    def CreateRoom(self):
        send(self.server_socket, ADD_ROOM_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == ADD_ROOM_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def JoinRoom(self, roomname):
        send(self.server_socket, (JOIN_ROOM_REQ + roomname).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == JOIN_ROOM_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        

    def GetHostUsername(self):
        send(self.server_socket, GET_HOST_USERNAME_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data.startswith(GET_HOST_USERNAME_RES)):
                return data[len(GET_HOST_USERNAME_RES):]
            else:
                return None
        
        except socket.timeout:
            return None
    
    def GetUsersInMyRoom(self):
        send(self.server_socket, GET_USERS_IN_MY_ROOM_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data.startswith(GET_USERS_IN_MY_ROOM_RES)):
                return data[len(GET_USERS_IN_MY_ROOM_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []
        
    def SetGameSettings(self, num_of_mines, boardsize):
        send(self.server_socket, (SET_GAME_SETTINGS_REQ + str(num_of_mines) + ';' + str(boardsize)).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == SET_GAME_SETTINGS_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def GetGameSettings(self):
        send(self.server_socket, GET_GAME_SETTINGS_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data.startswith(GET_GAME_SETTINGS_RES)):
                return data[len(GET_GAME_SETTINGS_RES):].split(';')
            else:
                return []
        
        except socket.timeout:
            return []
        
    def StartGame(self):
        send(self.server_socket, START_GAME_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == START_GAME_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def IsGameStarted(self):
        send(self.server_socket, IS_GAME_STARTED_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == IS_GAME_STARTED_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:  
            return False
        
    def GetGameChanges(self, num_of_changes=NUM_OF_CHANGES_EACH_PASS):
        send(self.server_socket, (GET_GAME_CHANGES + str(num_of_changes)).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data.startswith(GET_GAME_CHANGES)):
                current = data[len(GET_GAME_CHANGES):].split(';')
                changes_tuple_list = []
                for change in current:
                    if(len(change.split(',')) != 3):
                        # Format of a change is: x,y,value
                        continue
                    if(change.split(',')[0] == GAMELOST or change.split(',')[0] == GAMEWON):
                        changes_tuple_list.append(change.split(','))
                        return changes_tuple_list
                    changes_tuple_list.append(tuple(int(x) for x in change.split(','))) 

                return changes_tuple_list
            else:
                return []
        
        except socket.timeout:
            print("timeout")
            return []
        
    def IsItMyTurn(self):
        send(self.server_socket, IS_IT_MY_TURN_REQ.encode())
        try:
            data = recv(self.server_socket, 1024).decode()
            if(data == IS_IT_MY_TURN_RES_TRUE):
                return True
            else:
                return False
        
        except socket.timeout:
            return False
        
    def OpenCell(self, x, y):
        send(self.server_socket, (OPEN_CELL_REQ + str(x) + ';' + str(y)).encode())
        try:
            data = recv(self.server_socket, 1024).decode()
        except socket.timeout:
            return False
        

