import tkinter as tk


from Client.GUI.windows.windsows_constants import *
from Client.GUI.windows.window import Window

class LoginWindow(Window):
    def __init__(self, parent, serverAPI):
        super().__init__(parent)
        self.serverAPI = serverAPI

        self.geometry(f"{LOGIN_WINDOW_WIDTH}x{LOGIN_WINDOW_HEIGHT}")
        self.title("Login")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.username = ""
        self.password = ""

        self.username_label = tk.Label(self, text="Username", font=LOGIN_TXT_FONT)
        self.username_entry = tk.Entry(self, width=LOGIN_TXT_INPUT_WIDTH, font=LOGIN_TXT_FONT)
        self.password_label = tk.Label(self, text="Password", font=LOGIN_TXT_FONT)
        self.password_entry = tk.Entry(self, show="●", width=LOGIN_TXT_INPUT_WIDTH, font=LOGIN_TXT_FONT)
        self.login_button = tk.Button(self, text="Login", command=self.login)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        print("logging in by username: " + self.username + " and password: " + self.password)

        res = self.serverAPI.Login(self.username, self.password)

        if(res):
            tk.messagebox.showinfo("Success", "Logged in successfully")
            self.destroy()

        else:
            tk.messagebox.showerror("Error", "Login failed")
            self.destroy()

    def destroy(self) -> None:
        return super().destroy()