import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *


class WaitingRoomWindow(Window):
    def __init__(self, parent, serverAPI):
        super().__init__(parent)

        self.serverAPI = serverAPI
        self.parent = parent

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title('room creation')
        self.resizable(False, False)

        self.title_label = tk.Label(self, text=("Waiting " + self.serverAPI.GetHostUsername()), bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)

        # NEED TO CHANGE

        self.title_label.pack()

        pass



