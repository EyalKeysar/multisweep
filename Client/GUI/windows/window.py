import tkinter as tk

class Window(tk.Toplevel):
    def update(self):
        pass
    
    def destroy(self) -> None:
        return super().destroy()


