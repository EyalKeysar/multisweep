import threading
import socket

from Server.Logic.Grid import Grid
from Server.ServerNetHandler import ServerNetHandler
from Server.repo_api import RepoAPI
from Server.Room import Room
from Server.Logic.LogicConstants import *
from shared.NetConstants import *
from shared.socket_protocol import send, recv


class Server:
    def __init__(self):
        print("Server init")

        self.net_handler = ServerNetHandler()

        self.repoAPI = RepoAPI()

        self.rooms = []


    def run(self):
        while True:

            for room in self.rooms:
                if(room.clients == []):
                    self.rooms.remove(room)

            if(not self.net_handler.in_AcceptClient):
                # Accept client
                self.net_handler.in_AcceptClient = True
                accept_thread = threading.Thread(target=self.net_handler.AcceptClient)
                accept_thread.start()


            # Handle clients
            for client in self.net_handler.clients:
                if(not client.in_handle):
                    client.in_handle = True
                    handle_thread = threading.Thread(target=self.HandleClient, args=(client,))
                    handle_thread.start()

    def HandleClient(self, client):
        if(client.in_game):
            room = [room for room in self.rooms if client in room.clients][0]
            if(room == None):
                client.in_handle = False
                return
            self.handle_client_ingame(client, room)
            client.in_game = False
            client.in_handle = False
            return

        client_socket = client.GetSocket()
        
        try:
            data = recv(client_socket, 1024).decode()
            command = data[:6]
            parameters = data[6:]
            
            if(command == PING_REQ):
                send(client_socket, PING_RES.encode())

            elif(command == LOGIN_REQ):
                username, password = parameters.split(';')
                res = self.repoAPI.check_account_password(username, password)
                
                if(res):
                    client.SetAuthenticated(True)
                    client.SetUsername(username)
                    send(client_socket, LOGIN_RES_TRUE.encode())
                else:
                    send(client_socket, LOGIN_RES_FALSE.encode())

            elif(command == REGISTER_REQ):
                username, password, email = parameters.split(';')
                res = self.repoAPI.add_account(username, password, email)

                if(res):
                    client.SetAuthenticated(True)
                    client.SetUsername(username)
                    send(client_socket, REGISTER_RES_TRUE.encode())
                else:
                    send(client_socket, REGISTER_RES_FALSE.encode())

            elif(command == GET_AVAILABLE_ROOMS_REQ):
                if(client.IsAuthenticated()):
                    rooms_names = []
                    for room in self.rooms:
                        if(not room.game_started):
                            rooms_names.append(room.name)
                    rooms_names = ';'.join(rooms_names)
                    send(client_socket, (GET_AVAILABLE_ROOMS_RES + rooms_names).encode())

            elif(command == ADD_ROOM_REQ):
                if(client.IsAuthenticated()):
                    client.game_changes = []
                    for room in self.rooms:
                        if(client in room.clients):
                            room.clients.remove(client)
                    room = Room(client)
                    self.rooms.append(room)
                    send(client_socket, ADD_ROOM_RES_TRUE.encode())

            elif(command == JOIN_ROOM_REQ):
                if(client.IsAuthenticated()):
                    client.game_changes = []
                    for room in self.rooms:
                        if(client in room.clients):
                            room.clients.remove(client)


                    room_name = parameters
                    room = [room for room in self.rooms if room.name == room_name][0]
                    res = room.AddClient(client)
                    if(res):
                        send(client_socket, JOIN_ROOM_RES_TRUE.encode())
                    else:
                        send(client_socket, JOIN_ROOM_RES_FALSE.encode())

            elif(command == GET_USERS_IN_MY_ROOM_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if room.host == client][0]
                    users = room.GetUsersNames()
                    users = ';'.join(users)
                    send(client_socket, (GET_USERS_IN_MY_ROOM_RES + users).encode())

            elif(command == GET_HOST_USERNAME_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client in room.clients][0]
                    host_username = room.host.GetUsername()
                    send(client_socket, (GET_HOST_USERNAME_RES + host_username).encode())

            elif(command == SET_GAME_SETTINGS_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client == room.host][0]
                    if(room == None):
                        send(client_socket, SET_GAME_SETTINGS_RES_FALSE.encode())
                    else:
                        numofmines = int(parameters.split(';')[0])
                        boardsize = int(parameters.split(';')[1])

                        if(numofmines < MIN_MINES or numofmines > MAX_MINES or boardsize < MIN_SIZE or boardsize > MAX_SIZE):
                            send(client_socket, SET_GAME_SETTINGS_RES_FALSE.encode())
                        else:
                            room.num_of_mines = numofmines
                            room.board_size = boardsize
                            send(client_socket, SET_GAME_SETTINGS_RES_TRUE.encode())
                    
            elif(command == GET_GAME_SETTINGS_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client in room.clients][0]
                    if(room == None):
                        send(client_socket, GET_GAME_SETTINGS_RES.encode())
                    else:
                        send(client_socket, (GET_GAME_SETTINGS_RES + str(room.num_of_mines) + ';' + str(room.board_size)).encode())
            
            elif(command == IS_GAME_STARTED_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client in room.clients][0]
                    if(room == None):
                        send(client_socket, IS_GAME_STARTED_RES_FALSE.encode())
                    else:
                        if(room.game_started):
                            send(client_socket, IS_GAME_STARTED_RES_TRUE.encode())
                        else:
                            send(client_socket, IS_GAME_STARTED_RES_FALSE.encode())

            elif(command == START_GAME_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client == room.host][0]
                    if(room == None):
                        send(client_socket, START_GAME_RES_FALSE.encode())
                    else:
                        send(client_socket, START_GAME_RES_TRUE.encode())
                        room.game_started = True
                        for cur_client in room.clients:
                            cur_client.in_game = True
                        self.handle_client_ingame(client, room)


            elif(command == GET_GAME_CHANGES):
                num_of_changes = int(parameters)
                if(num_of_changes > len(client.game_changes)):
                    num_of_changes = len(client.game_changes)
                changes = client.GetAndFlushChanges(num_of_changes)
                respond = ""
                for change in changes:
                    respond += str(change[0]) + ',' + str(change[1]) + ',' + str(change[2]) + ';'
                send(client_socket, (GET_GAME_CHANGES + respond).encode())

            elif(command == OPEN_CELL_REQ):
                send(client_socket, OPEN_CELL_RES_FALSE.encode())


            else:
                print("!@!@!@! UNKNOWN  " + str(data))

        except socket.timeout:
            print("HandleClient timeout")
        client.in_handle = False

    def handle_client_ingame(self, client, room):
        is_host = (client == room.host)
        if(is_host):
            room.StartGame()

        while True:
            if((room.won or room.lost) and is_host):
                for client in room.clients:
                    if(room.won):
                        client.game_changes.append((GAMEWON, 0, 0))
                    else:
                        client.game_changes.append((GAMELOST, 0, 0))
                return
            
            elif(room.won or room.lost):
                client.game_changes.append((GAMEWON, 0, 0) if room.won else (GAMELOST, 0, 0))
                client.in_game = False
                room.clients.remove(client)
                return

            client_socket = client.GetSocket()
            try:
                data = recv(client_socket, 1024).decode()
                command = data[:6]
                parameters = data[6:]
            except socket.timeout:
                continue

            if(command == PING_REQ):
                send(client_socket, PING_RES.encode())

            elif(command == IS_GAME_STARTED_REQ):
                send(client_socket, IS_GAME_STARTED_RES_TRUE.encode())

            elif(command == GET_GAME_SETTINGS_REQ):
                send(client_socket, (GET_GAME_SETTINGS_RES + str(room.num_of_mines) + ';' + str(room.board_size)).encode())

            elif(command == IS_IT_MY_TURN_REQ):
                if(room.MyTurn(client)):
                    send(client_socket, IS_IT_MY_TURN_RES_TRUE.encode())
                else:
                    send(client_socket, IS_IT_MY_TURN_RES_FALSE.encode())

            elif(command == GET_GAME_CHANGES):
                if(client in room.clients):
                    num_of_changes = int(parameters)
                    if(num_of_changes > len(client.game_changes)):
                        num_of_changes = len(client.game_changes)
                    changes = client.GetAndFlushChanges(num_of_changes)
                    respond = ""
                    for change in changes:
                        respond += str(change[0]) + ',' + str(change[1]) + ',' + str(change[2]) + ';'
                    send(client_socket, (GET_GAME_CHANGES + respond).encode())
                    

            elif(command == GET_HOST_USERNAME_REQ):
                if(client.IsAuthenticated()):
                    host_username = room.host.GetUsername()
                    send(client_socket, (GET_HOST_USERNAME_RES + host_username).encode())
            
            elif(command == OPEN_CELL_REQ):
                if(client.IsAuthenticated()):
                    if(room.lost or room.won):
                        send(client_socket, OPEN_CELL_RES_FALSE.encode())
                    else:
                        if(room.MyTurn(client)):
                            x, y = parameters.split(';')
                            x = int(x)
                            y = int(y)
                            res = room.OpenCell(x, y)
                            if(res):
                                send(client_socket, OPEN_CELL_RES_TRUE.encode())
                                room.NextTurn()
                            else:
                                send(client_socket, OPEN_CELL_RES_FALSE.encode())
                            

                        else:
                            send(client_socket, OPEN_CELL_RES_FALSE.encode())
                else:
                    print("OPEN_CELL not authenticated")
                    send(client_socket, OPEN_CELL_RES_FALSE.encode())

            else:
                print("!$!$!$! UNKNOWN  " + str(data))


if(__name__ == "__main__"):
    server = Server().run()
