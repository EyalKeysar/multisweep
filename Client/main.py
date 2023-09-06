from Client.GUI.WindowHandler import WindowHandler
from Client.GUI.TkHandler import TkHandler
from Client.GUI.windows.main_window import MainWindow
from Client.GUI.windows.login_window import LoginWindow
from Client.GUI.windows.register_window import RegisterWindow
from Client.GUI.windows.lobby_window import LobbyWindow
from shared.ServerAPI import ServerAPI

def main():

    serverAPI = ServerAPI()

    root = TkHandler().root
    window_handler = WindowHandler(root)
    window_handler.ChangeWindow(MainWindow, window_handler, serverAPI)

    root.after(1000, periodic, root, window_handler, serverAPI)

    root.mainloop()

def periodic(root, window_handler, serverAPI):
    
    serverAPI.CheckConnection()

    auth_check(serverAPI, window_handler)
    select_player_check(serverAPI, window_handler)

    root.after(1000, periodic, root, window_handler, serverAPI)

def auth_check(serverAPI, window_handler):
    if(serverAPI.is_authenticated 
       and ( type(window_handler.GetCurWindow()) == MainWindow 
       or type(window_handler.GetCurWindow()) == LoginWindow 
       or type(window_handler.GetCurWindow()) == RegisterWindow)):
        
        window_handler.ChangeWindow(LobbyWindow, serverAPI)


def select_player_check(serverAPI, window_handler):
    if(serverAPI.is_authenticated 
       and type(window_handler.GetCurWindow()) == LobbyWindow):
        if(window_handler.current_window.selected_player != None):
            print("selected player: " + window_handler.current_window.selected_player)
            window_handler.GetCurWindow().destroy()


if __name__ == "__main__":
    main()



