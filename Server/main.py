import threading
import socket

from Server.Logic.Grid import Grid
from Server.ServerNetHandler import ServerNetHandler


class Server:
    def __init__(self) -> None:
        print("Server init")

        self.net_handler = ServerNetHandler()

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
                print("Starting client thread")
                try:
                    data = client.GetSocket().recv(1024)
                    print(data)
                    if(data == b"ping"):
                        client.GetSocket().send(b"pong")
                except socket.timeout:
                    continue

if(__name__ == "__main__"):
    server = Server().run()