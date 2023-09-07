import threading
import socket

from Server.Logic.Grid import Grid
from Server.ServerNetHandler import ServerNetHandler
from Server.repo_api import RepoAPI
from Server.Room import Room
from shared.NetConstants import *


class Server:
    def __init__(self) -> None:
        print("Server init")

        self.net_handler = ServerNetHandler()

        self.repoAPI = RepoAPI()

        self.rooms = []


    def run(self):
        while True:
            if(not self.net_handler.in_AcceptClient):
                # Accept client
                print("Starting accept thread the in accept client is" + str(self.net_handler.in_AcceptClient))
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
        client_socket = client.GetSocket()
        try:
            data = client_socket.recv(1024).decode()
            command = data[:6]
            parameters = data[6:]
            
            if(command == PING_REQ):
                print("PING")
                client_socket.send(PING_RES.encode())

            elif(command == LOGIN_REQ):
                username, password = parameters.split(';')
                res = self.repoAPI.check_account_password(username, password)
                
                if(res):
                    client.SetAuthenticated(True)
                    client.SetUsername(username)
                    client_socket.send(LOGIN_RES_TRUE.encode())
                    print(f"LOGIN {username} {password} success")
                else:
                    print(f"LOGIN {username} {password} failed")
                    client_socket.send(LOGIN_RES_FALSE.encode())

            elif(command == REGISTER_REQ):
                username, password, email = parameters.split(';')
                res = self.repoAPI.add_account(username, password, email)

                if(res):
                    client.SetAuthenticated(True)
                    client.SetUsername(username)
                    client_socket.send(REGISTER_RES_TRUE.encode())
                    print(f"REGISTER {username} {password} {email} success")
                else:
                    print(f"REGISTER {username} {password} {email} failed")
                    client_socket.send(REGISTER_RES_FALSE.encode())

            elif(command == GET_AVAILABLE_ROOMS_REQ):
                if(client.IsAuthenticated()):
                    rooms_names = [room.name for room in self.rooms]
                    rooms_names = ';'.join(rooms_names)
                    client_socket.send((GET_AVAILABLE_ROOMS_RES + rooms_names).encode())
                    print(f"GET_AVAILABLE_USERS {rooms_names}")

            elif(command == ADD_ROOM_REQ):
                if(client.IsAuthenticated()):
                    room = Room(client)
                    self.rooms.append(room)
                    client_socket.send(ADD_ROOM_RES_TRUE.encode())
                    print(f"ADD_ROOM {room.name} success")

            elif(command == JOIN_ROOM_REQ):
                if(client.IsAuthenticated()):
                    room_name = parameters
                    room = [room for room in self.rooms if room.name == room_name][0]
                    res = room.AddClient(client)
                    if(res):
                        client_socket.send(JOIN_ROOM_RES_TRUE.encode())
                        print(f"JOIN_ROOM {room.name} success")
                    else:
                        client_socket.send(JOIN_ROOM_RES_FALSE.encode())
                        print(f"JOIN_ROOM {room.name} failed")

            elif(command == GET_USERS_IN_MY_ROOM_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if room.host == client][0]
                    users = room.GetUsersNames()
                    users = ';'.join(users)
                    client_socket.send((GET_USERS_IN_MY_ROOM_RES + users).encode())
                    print(f"GET_USERS_IN_MY_ROOM {users}")

            elif(command == GET_HOST_USERNAME_REQ):
                if(client.IsAuthenticated()):
                    room = [room for room in self.rooms if client in room.clients][0]
                    host_username = room.host.GetUsername()
                    client_socket.send((GET_HOST_USERNAME_RES + host_username).encode())
                    print(f"GET_HOST_USERNAME {host_username}")
                    


            
            else:
                print("!@!@!@! UNKNOWN  " + str(data))

        except socket.timeout:
            print("HandleClient timeout")
        client.in_handle = False

if(__name__ == "__main__"):
    server = Server().run()