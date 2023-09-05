

class WindowHandler():
    def __init__(self, root):
        self.root = root
        self.current_window = None
        self.stack = []

    def ChangeWindow(self, new_window, *args, **kwargs):
        if(self.current_window != None):
            while(self.stack != []): # Remove all windows from the stack
                some_window = self.stack.pop()
                some_window.destroy()
        else:
            self.stack = []
        self.current_window = new_window(self.root, *args, **kwargs)
        self.stack.append(self.current_window)
    
    def PopWindow(self, new_window, *args, **kwargs):
        self.current_window = new_window(self.root, *args, **kwargs)
        self.stack.append(self.current_window)

    def GetCurWindow(self):
        return self.current_window