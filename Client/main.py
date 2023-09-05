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

    if(serverAPI.is_authenticated and window_handler.GetCurWindow() == MainWindow):
        window_handler.ChangeWindow(LobbyWindow)
    elif(serverAPI.is_authenticated == True and window_handler.GetCurWindow() != MainWindow):
        print(str(window_handler.GetCurWindow()))

    root.after(1000, periodic, root, window_handler, serverAPI)



if __name__ == "__main__":
    main()



