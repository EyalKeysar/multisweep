import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *

from Client.GUI.windows.lobby_window import LobbyWindow

class WinWindow(Window):

    def __init__(self, parent, window_handler):
        super().__init__(parent)

        self.parent = parent
        self.window_handler = window_handler

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title('win')
        self.resizable(False, False)

        self.title_label = tk.Label(self, text="You Win!", bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)

        self.goback_button = tk.Button(self, text="Go Lobby", command=self.GoBack)

        self.title_label.pack()
        self.goback_button.pack()

    def GoBack(self):
        self.window_handler.ChangeWindow(LobbyWindow, self.parent.serverAPI)
