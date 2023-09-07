from Server.Client import Client
from Server.Logic.Grid import Grid

class Room:
    def __init__(self, host):
        self.host = host
        self.name = host.GetUsername()
        self.clients = [host]

        self.turn = 0

        self.num_of_mines = 0
        self.board_size = 0
        

    def AddClient(self, client):
        self.clients.append(client)
        return True
    
    def StartGame(self):
        self.grid = Grid(self.num_of_mines, self.board_size)
        self.turn = 0

    def GetUsersNames(self):
        return [client.GetUsername() for client in self.clients]
    
    def MyTurn(self, client):
        return self.clients[self.turn] == client

    def NextTurn(self):
        self.turn = (self.turn + 1) % len(self.clients)
        return self.turn