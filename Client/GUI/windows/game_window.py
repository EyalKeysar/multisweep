import tkinter as tk

from Client.GUI.windows.window import Window
from Client.GUI.windows.windsows_constants import *
from Client.GUI.Grid import *

from shared.NetConstants import *

class GameWindow(Window):
    def __init__(self, parent, serverAPI, grid_size):
        super().__init__(parent)

        self.in_update = False

        self.parent = parent
        self.serverAPI = serverAPI

        self.game_running = True
        self.game_res = None

        self.geometry(f"{GAME_SCREEN_WIDTH}x{GAME_SCREEN_HEIGHT}")
        self.title('game')
        self.resizable(False, False)

        size = serverAPI.GetGameSettings()[1]
        self.grid = Grid(size)
        self.flags = []

        # Create grid of buttons
        self.buttons = []
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                
                if((x, y) in self.flags):
                    btn = tk.Button(self, text="F", width=2, height=1, font=GAME_BUTTON_FONT)
                else:
                    btn = tk.Button(self, 
                                text=str(" " if self.grid.grid[y][x] == CLOSED_CELL else self.grid.grid[y][x]), 
                                width=2, height=1, font=GAME_BUTTON_FONT,
                                state=tk.DISABLED if self.grid.grid[y][x] != CLOSED_CELL else tk.NORMAL)

                btn.grid(row=y, column=x)
                btn.bind('<Button-1>', self.left_click)
                btn.bind('<Button-3>', self.right_click)
                row.append(btn)
            self.buttons.append(row)

        self.UpdateGrid()


    def UpdateGrid(self):
        if(self.in_update):
            print("blocked")
            self.parent.after(100, self.UpdateGrid)

        self.in_update = True
        gcngs = self.serverAPI.GetGameChanges()

        if(gcngs == []):
            print("No changes")
            pass
        else:
            for change in gcngs:
                if(change[0] == GAMELOST):
                    print(change)
                    self.game_running = False
                    self.game_res = False
                    print("Game Lost")
                    return
                elif(change[0] == GAMEWON):
                    self.game_running = False
                    self.game_res = True
                    print("Game Won")
                    return
                self.grid.changes.append(change)

            self.grid.apply_changes()
            for y in range(len(self.grid.grid)):
                for x in range(len(self.grid.grid)):
                    if((x, y) in self.flags):
                        self.buttons[y][x].config(text="F")
                    else:
                        self.buttons[y][x].config(text=str(" " if self.grid.grid[y][x] == CLOSED_CELL else str(self.grid.grid[y][x])),
                                                state=tk.DISABLED if self.grid.grid[y][x] != CLOSED_CELL else tk.NORMAL)
                    

                    if(self.grid.grid[y][x] in DIGITS):
                        color = DIGIT_TO_COLOR[self.grid.grid[y][x]]
                        self.buttons[y][x].config(bg=color)
                    
        self.in_update = False

        if(self.game_running):
            self.parent.after(100, self.UpdateGrid)
        else:
            print("Game Ended")



    def left_click(self, event):
        clicked_button = event.widget
        button_info = clicked_button.grid_info()
        row, column = button_info['row'], button_info['column']
        print(f"Button clicked at (row={row}, column={column})")

        if((column, row) in self.flags):
            return

        self.serverAPI.OpenCell(column, row)
        return
        

    def right_click(self, event):
        # Get Button and flag it
        clicked_button = event.widget
        button_info = clicked_button.grid_info()
        row, column = button_info['row'], button_info['column']
        print(f"Flag Placed at (row={row}, column={column})")
        if((column, row) in self.flags):
            self.buttons[row][column].config(text=" ")
            self.flags.remove((column, row))
        else:
            self.buttons[row][column].config(text="F")
            self.flags.append((column, row))

    def UpdateTurnIndicator(self):
        your_turn = False
        TEXT = "Turn"
        for i in range(len(TEXT)):
            l = tk.Label(self, text=TEXT[i], bg=YOUR_TURN_COLOR if your_turn else NOT_YOUR_TURN_COLOR, width=1, height=1)
            l.grid(row=0, column=i)