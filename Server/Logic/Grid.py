import random

from Server.Logic.LogicConstants import *


class Grid():
    def __init__(self) -> None:
        pass

    def random_grid(self, high, width, num_of_mines):
        self.grid = [[0 for x in range(width )] for y in range(high )]
        self.upper_grid = [[0 for x in range(width )] for y in range(high )]
        self.high = high
        self.width = width
        self.num_of_mines = num_of_mines

        for i in range(num_of_mines):
            random_x = random.randint(0, width - 1)
            random_y = random.randint(0, high -1)
            print(random_x, random_y)
            if self.grid[random_y][random_x] == MINE:
                i -= 1
            else:
                self.grid[random_y][random_x] = MINE

    def calculate_nums(self):
        for y in range(self.high):
            for x in range(self.width):
                if self.grid[y][x] == MINE:

                    if(y < self.high - 1):
                        self.grid[y+1][x] += 1
                    if(y > 0):
                        self.grid[y-1][x] += 1
                    if(x < self.width - 1):
                        self.grid[y][x+1] += 1
                    if(x > 0):
                        self.grid[y][x-1] += 1
                    if(y < self.high - 1 and x < self.width - 1 ):
                        self.grid[y+1][x+1] += 1
                    if(y > 0 and x > 0):
                        self.grid[y-1][x-1] += 1
                    if(y < self.high -1 and x > 0):
                        self.grid[y+1][x-1] += 1
                    if(y > 0 and x < self.width - 1):
                        self.grid[y-1][x+1] += 1
                    


    def print_grid(self):
        for y in range(self.high):
            print(self.grid[y])


    def open_cell(self, x, y):
        if self.grid[y][x] == MINE:
            return MINE
        else:
            self.upper_grid[y][x] = OPEN
            return 0
        

    



if __name__ == "__main__":
    grid = Grid()
    grid.random_grid(10, 10, 1)
    grid.calculate_nums()
    grid.print_grid()