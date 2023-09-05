import tkinter as tk


from Client.GUI.windows.windsows_constants import *

class TkHandler():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()
        # self.root.title(GAME_NAME)
        # self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        # self.root.resizable(False, False)
        # self.root.configure(bg=SCREENBGCOLOR)

