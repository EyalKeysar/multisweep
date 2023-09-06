import threading
import socket

from Server.Logic.Grid import Grid
from Server.ServerNetHandler import ServerNetHandler
from Server.repo_api import RepoAPI
from shared.NetConstants import *


class Server:
    def __init__(self) -> None:
        print("Server init")

        self.net_handler = ServerNetHandler()

        self.repoAPI = RepoAPI()

        self.repoAPI.add_account("test", "test", "asd")


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

            elif(command == GET_AVAILABLE_USERS_REQ):
                if(client.IsAuthenticated()):
                    users = self.net_handler.clients
                    users = [user.GetUsername() for user in users if user.IsAuthenticated()]
                    users = ';'.join(users)
                    client_socket.send((GET_AVAILABLE_USERS_RES + users).encode())
                    print(f"GET_AVAILABLE_USERS {users}")

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


            
            else:
                print("!@!@!@! UNKNOWN  " + str(data))

        except socket.timeout:
            print("HandleClient timeout")
        client.in_handle = False

if(__name__ == "__main__"):
    server = Server().run()