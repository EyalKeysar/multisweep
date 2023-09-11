

CLOSED_CELL = -1


class Grid:
    def __init__(self, size):
        self.size = int(size)
        self.grid = [[CLOSED_CELL for x in range(self.size)] for y in range(self.size)]
        self.changes = []

    def apply_changes(self):
        for change in self.changes:
            if(len(change) != 3):
                print("Error: change is not in the right format: " + str(change))
                continue
            print(change)
            self.grid[change[1]][change[0]] = change[2]
            print("[" + str(change[0]) + ", " + str(change[1]) + "] = " + str(change[2]))
        self.changes = []
