

class Client:
    def __init__(self, client_socket, address) -> None:
        self.in_handle = False
        self.in_game = False
        self.data = {
            "client_socket": client_socket,
            "address": address,
            "is_authenticated": False,
            "username": None
        }
        self.game_changes = []
        print(f"Client {self.data} initialized")

    def IsAuthenticated(self):
        return self.data["is_authenticated"]
    
    def SetAuthenticated(self, value):
        self.data["is_authenticated"] = value

    def GetUsername(self):
        return self.data["username"]
    
    def SetUsername(self, value):
        self.data["username"] = value

    def GetSocket(self):
        return self.data["client_socket"]

    def SetSocket(self, value):
        self.data["client_socket"] = value

    def GetAddress(self):
        return self.data["address"]

    def SetAddress(self, value):
        self.data["address"] = value
    
    def GetClientData(self):
        return self.data