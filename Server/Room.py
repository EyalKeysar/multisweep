from Server.Client import Client
from Server.Logic.Grid import Grid

class Room:
    def __init__(self, host):
        self.host = host
        self.name = host.GetUsername()
        self.clients = [host]

        self.grid = None

        self.turn = 0

        self.num_of_mines = 0
        self.board_size = 0
        
    def StartGame(self):
        self.grid = Grid(self.board_size, self.board_size, self.num_of_mines)
        self.turn = 0

    def DoTurn(self):
        self.turn = (self.turn + 1) % len(self.clients)
        return self.turn

    def AddClient(self, client):
        self.clients.append(client)
        return True
    
    def StartGame(self):
        self.grid = Grid(self.board_size, self.board_size, self.num_of_mines)
        self.turn = 0

    def GetUsersNames(self):
        return [client.GetUsername() for client in self.clients]
    
    def MyTurn(self, client):
        return self.clients[self.turn] == client

    def NextTurn(self):
        self.turn = (self.turn + 1) % len(self.clients)
        return self.turn
    
    def OpenCell(self, x, y):
        self.grid.OpenCell(x, y)

        cur_changes = self.grid.collect_changes()
        for client in self.clients:
            client.game_changes.extend(cur_changes)
