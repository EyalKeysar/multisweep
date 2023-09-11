import random

from Server.Logic.LogicConstants import *
# from LogicConstants import *


class Grid():
    def __init__(self, high, width, num_of_mines) -> None:
        self.grid = [[0 for x in range(width )] for y in range(high )]
        self.upper_grid = [[0 for x in range(width )] for y in range(high )]
        self.hight = high
        self.width = width
        self.num_of_mines = num_of_mines

        for i in range(num_of_mines):
            random_x = random.randint(0, width - 1)
            random_y = random.randint(0, high -1)
            if self.grid[random_y][random_x] == MINE:
                i -= 1
            else:
                self.grid[random_y][random_x] = MINE
        self.calculate_nums()
        self.changes = []

    def calculate_nums(self):
        for y in range(self.hight):
            for x in range(self.width):
                if self.grid[y][x] == MINE:

                    if(y < self.hight - 1):
                        if(self.grid[y+1][x] != MINE):
                            self.grid[y+1][x] += 1
                    if(y > 0):
                        if(self.grid[y-1][x] != MINE):
                            self.grid[y-1][x] += 1
                    if(x < self.width - 1):
                        if(self.grid[y][x+1] != MINE):
                            self.grid[y][x+1] += 1
                    if(x > 0):
                        if(self.grid[y][x-1] != MINE):
                            self.grid[y][x-1] += 1

                    if(y < self.hight - 1 and x < self.width - 1 ):
                        if(self.grid[y+1][x+1] != MINE):
                            self.grid[y+1][x+1] += 1
                    if(y > 0 and x > 0):
                        if(self.grid[y-1][x-1] != MINE):
                            self.grid[y-1][x-1] += 1
                    if(y < self.hight -1 and x > 0):
                        if(self.grid[y+1][x-1] != MINE):
                            self.grid[y+1][x-1] += 1
                    if(y > 0 and x < self.width - 1):
                        if(self.grid[y-1][x+1] != MINE):
                            self.grid[y-1][x+1] += 1
                    
    def collect_changes(self):
        ret = [x for x in self.changes]
        self.changes = []
        return ret


    def print_grid(self):
        for y in range(self.hight):
            for x in range(self.width):
                if(self.grid[y][x] >= 0):
                    print(" " + str(self.grid[y][x]), end=" ")
                else:
                    print(self.grid[y][x], end=" ")
            print()

    def print_upper_grid(self):
        for y in range(self.hight):
            print(self.upper_grid[y])

    def print_as_shown(self):
        for y in range(self.hight):
            for x in range(self.width):
                if(self.upper_grid[y][x] == OPEN):
                    if(self.grid[y][x] > 0):
                        print(" " + str(self.grid[y][x]), end=" ")
                    elif(self.grid[y][x] == 0):
                        print(" " + " ", end=" ")
                    else:
                        print(self.grid[y][x], end=" ")
                else:
                    print(" x", end=" ")

            print()

    def open_cell(self, x, y):
        if self.grid[y][x] == MINE:
            return MINE
        else:
            self.open_recursive(x, y)
            return True
        
    def open_recursive(self, x, y):
        if self.grid[y][x] == EMPTY and self.upper_grid[y][x] != OPEN:
            self.upper_grid[y][x] = OPEN
            self.changes.append((x, y, self.grid[y][x]))
            if(y < self.hight - 1):
                self.open_recursive(x, y+1)
            if(y > 0):
                self.open_recursive(x, y-1)
            if(x < self.width - 1):
                self.open_recursive(x+1, y)
            if(x > 0):
                self.open_recursive(x-1, y)

            if(y < self.hight - 1 and x < self.width - 1 ):
                self.open_recursive(x+1, y+1)
            if(y > 0 and x > 0):
                self.open_recursive(x-1, y-1)
            if(y < self.hight -1 and x > 0):
                self.open_recursive(x-1, y+1)
            if(y > 0 and x < self.width - 1):
                self.open_recursive(x+1, y-1)
        elif(self.upper_grid[y][x] != OPEN):
            self.upper_grid[y][x] = OPEN
            self.changes.append((x, y, self.grid[y][x]))
        

    



if __name__ == "__main__":
    grid = Grid(15, 15, 30)
    grid.print_grid()
    x, y = int(input("x")), int(input("y"))
    grid.open_cell(x, y)
    grid.print_as_shown()
    print(grid.changes)