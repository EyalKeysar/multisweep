import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *
from Client.GUI.windows.game_window import GameWindow

class WaitingRoomWindow(Window):
    def __init__(self, parent, serverAPI):
        super().__init__(parent)

        self.serverAPI = serverAPI
        self.parent = parent

        self.need_update = True
        self.game_started = False
        self.check_game_start()

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title('room creation')
        self.resizable(False, False)

        self.title_label = tk.Label(self, text=("Waiting " + str(self.serverAPI.GetHostUsername())), bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)


        # NEED TO CHANGE

        self.title_label.pack()

        pass

    def check_game_start(self):
        if(self.need_update):
            if(self.serverAPI.IsGameStarted()):
                self.need_update = False
                self.game_started = True

            self.parent.after(1000, self.check_game_start)





