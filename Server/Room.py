from Server.Client import Client


class Room:
    def __init__(self, host):
        self.host = host
        self.name = host.GetUsername()
        self.clients = [host]

    def AddClient(self, client):
        self.clients.append(client)
        return True

    def GetUsersNames(self):
        return [client.GetUsername() for client in self.clients]