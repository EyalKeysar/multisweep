import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *

MIN_MINES = 1
MAX_MINES = 50

MIN_SIZE = 10
MAX_SIZE = 50

class RoomWindow(Window):
    def __init__(self, parent, serverAPI):
        super().__init__(parent)

        self.parent = parent

        self.need_update = True

        self.serverAPI = serverAPI

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title('room creation')
        self.resizable(False, False)

        self.title_label = tk.Label(self, text=("room " + self.serverAPI.GetUsername()), bg = TITLE_BG_CLR, width=SCREEN_WIDTH, height=SIGN_IN_TITLE_HEIGHT, font = TITLE_TXT_FONT)
        self.num_of_mines_scale = tk.Scale(self, from_=MIN_MINES, to=MAX_MINES, orient=tk.HORIZONTAL, length=int(SCREEN_WIDTH / 2), label="number of mines") 
        self.boardsize_scale = tk.Scale(self, from_=MIN_SIZE, to=MAX_SIZE, orient=tk.HORIZONTAL, length=int(SCREEN_WIDTH / 2), label="grid size")

        self.Listbox = tk.Listbox(self, width=SCREEN_WIDTH, height=int(SCREEN_HEIGHT / 4))
        self.get_players_in_my_room()

        self.title_label.pack()
        self.num_of_mines_scale.pack()
        self.boardsize_scale.pack()
        self.Listbox.pack()

        pass

    def get_players_in_my_room(self):
        self.Listbox.delete(0, 'end')
        for player in self.serverAPI.GetUsersInMyRoom():
            self.Listbox.insert(tk.END, str(player))

        if(self.need_update):
            self.parent.after(1000, self.get_players_in_my_room)


