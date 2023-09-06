import tkinter as tk

from Client.GUI.windows.windsows_constants import *
from Client.GUI.windows.login_window import LoginWindow
from Client.GUI.windows.register_window import RegisterWindow
from Client.GUI.windows.window import Window


class LobbyWindow(Window):
    def __init__(self, parent, serverAPI):
        super().__init__(parent)

        self.selected_player = None

        self.need_update = True # flag to check for available users
        self.parent = parent
        self.serverAPI = serverAPI
        
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title(GAME_NAME)
        self.resizable(False, False)

        self.connection_status_label = tk.Label(self, text="Disconnected", bg="#FF0000", width=SCREEN_WIDTH, height=CONNECTION_STATUS_BAR_HEIGHT)
        self.title_label = tk.Label(self, text = LOBBY_TITLE_TXT, bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)

        self.connection_status_label.pack()
        self.title_label.pack()

        self.users_selection = tk.Listbox(self, width=SCREEN_WIDTH, height=int(SCREEN_HEIGHT / 4))
        for user in self.serverAPI.GetAvailableUsers():
            self.users_selection.insert(tk.END, str(user))
        self.users_selection.pack()

        self.parent.after(1000, self.get_available_users)


    def get_available_users(self):

        if(self.check_selected()):
            return
        

        self.users_selection.delete(0, 'end')

        for user in self.serverAPI.GetAvailableUsers():
            self.users_selection.insert(tk.END, str(user))
        

        if(self.need_update):
            self.parent.after(1000, self.get_available_users)

    def check_selected(self):
        if(self.users_selection.curselection()):
            self.selected_player = self.users_selection.get(self.users_selection.curselection())
            self.need_update = False
            return True
        else:
            return False
    


