import tkinter as tk

from Client.GUI.windows.windsows_constants import *
from Client.GUI.windows.login_window import LoginWindow
from Client.GUI.windows.register_window import RegisterWindow
from Client.GUI.windows.window import Window


class LobbyWindow(Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title(GAME_NAME)
        self.resizable(False, False)

        self.connection_status_label = tk.Label(self, text="Disconnected", bg="#FF0000", width=SCREEN_WIDTH, height=CONNECTION_STATUS_BAR_HEIGHT)
        self.title_label = tk.Label(self, text = LOBBY_TITLE_TXT, bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)
        

