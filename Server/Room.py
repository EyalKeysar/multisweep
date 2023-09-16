from Server.Client import Client
from Server.Logic.Grid import Grid
from shared.NetConstants import *

class Room:
    def __init__(self, host):
        self.host = host
        self.name = host.GetUsername()
        self.clients = [host]

        self.game_started = False

        self.grid = None

        self.lost = False
        self.won = False


        self.turn = 0

        self.num_of_mines = 0
        self.board_size = 0
        
    def StartGame(self):
        self.grid = Grid(self.board_size, self.board_size, self.num_of_mines)
        self.game_started = True
        self.turn = 0

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

        res = self.grid.open_cell(x, y)

        cur_changes = self.grid.collect_changes()
        for client in self.clients:
            client.game_changes.extend(cur_changes)

        wc = self.grid.win_condition()
        lc = self.grid.lose_condition()
        if(lc):
            for client in self.clients:
                client.game_changes.append((GAMELOST, 0, 0))
            return res
        elif(wc):
            for client in self.clients:
                client.game_changes.append((GAMEWON, 0, 0))
            return res
        else:
            return res
