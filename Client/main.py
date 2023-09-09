from Client.GUI.WindowHandler import WindowHandler
from Client.GUI.TkHandler import TkHandler
from Client.GUI.windows.main_window import MainWindow
from Client.GUI.windows.login_window import LoginWindow
from Client.GUI.windows.register_window import RegisterWindow
from Client.GUI.windows.lobby_window import LobbyWindow
from Client.GUI.windows.room_window import RoomWindow
from Client.GUI.windows.waiting_room_window import WaitingRoomWindow
from Client.GUI.windows.game_window import GameWindow
from shared.ServerAPI import ServerAPI


def main():

    serverAPI = ServerAPI()

    root = TkHandler().root
    window_handler = WindowHandler(root)
    window_handler.ChangeWindow(MainWindow, window_handler, serverAPI)
    # window_handler.ChangeWindow(GameWindow, 30)

    root.after(1000, periodic, root, window_handler, serverAPI)

    root.mainloop()

def periodic(root, window_handler, serverAPI):
    
    serverAPI.CheckConnection()

    auth_check(serverAPI, window_handler)
    select_room_check(serverAPI, window_handler)
    start_game_check(serverAPI, window_handler)

    root.after(1000, periodic, root, window_handler, serverAPI)

def auth_check(serverAPI, window_handler):
    if(serverAPI.is_authenticated 
       and ( type(window_handler.GetCurWindow()) == MainWindow 
       or type(window_handler.GetCurWindow()) == LoginWindow 
       or type(window_handler.GetCurWindow()) == RegisterWindow)):
        
        window_handler.ChangeWindow(LobbyWindow, serverAPI)


def select_room_check(serverAPI, window_handler):
    if(serverAPI.is_authenticated 
       and type(window_handler.GetCurWindow()) == LobbyWindow):
        if(window_handler.current_window.selected_room != None):
            print("selected room: " + window_handler.current_window.selected_room)
            serverAPI.JoinRoom(window_handler.current_window.selected_room)
            window_handler.current_window.selected_room = None
            window_handler.current_window.destroy()
            window_handler.ChangeWindow(WaitingRoomWindow, serverAPI)

        elif(window_handler.current_window.created_room):
            window_handler.current_window.created_room = False
            window_handler.current_window.destroy()
            window_handler.ChangeWindow(RoomWindow, serverAPI)

def start_game_check(serverAPI, window_handler):
    if(serverAPI.is_authenticated 
       and (type(window_handler.GetCurWindow()) == WaitingRoomWindow 
            or type(window_handler.GetCurWindow()) == RoomWindow)):
        if(serverAPI.IsGameStarted()):
            print("game started")
            window_handler.current_window.destroy()
            window_handler.ChangeWindow(GameWindow, serverAPI, int(serverAPI.GetGameSettings()[1]))

            


if __name__ == "__main__":
    main()



