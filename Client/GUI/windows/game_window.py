import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *
from Client.GUI.Grid import *

class GameWindow(Window):
    def __init__(self, parent, serverAPI, grid_size):
        super().__init__(parent)

        self.parent = parent
        self.serverAPI = serverAPI

        self.geometry(f"{GAME_SCREEN_WIDTH}x{GAME_SCREEN_HEIGHT}")
        self.title('game')
        self.resizable(False, False)


        self.UpdateTurnIndicator()

        size = serverAPI.GetGameSettings()[1]
        self.grid = Grid(size)

        # Create grid of buttons
        self.buttons = []
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                btn = tk.Button(self, 
                                text=str(" " if self.grid.grid[y][x] == CLOSED_CELL else self.grid.grid[y][x]), 
                                width=2, height=1)
                btn.grid(row=y + 1, column=x)
                btn.bind('<Button-1>', self.left_click)
                btn.bind('<Button-3>', self.right_click)
                row.append(btn)
            self.buttons.append(row)


    def left_click(self, event):
        clicked_button = event.widget
        button_info = clicked_button.grid_info()
        row, column = button_info['row'], button_info['column']
        print(f"Button clicked at (row={row}, column={column})")

    def right_click(self, event):
        pass

    def UpdateTurnIndicator(self):
        your_turn = False
        TEXT = "Turn"
        for i in range(len(TEXT)):
            l = tk.Label(self, text=TEXT[i], bg=YOUR_TURN_COLOR if your_turn else NOT_YOUR_TURN_COLOR, width=1, height=1)
            l.grid(row=0, column=i)