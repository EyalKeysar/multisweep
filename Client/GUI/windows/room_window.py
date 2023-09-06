import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *


class RoomWindow(Window):
    def __init__(self, serverAPI):
        self.serverAPI = serverAPI

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title("Room")
        self.resizable(False, False)

        self.title_label = tk.Label(self, text = serverAPI.GetTeammate(), bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)

        pass

