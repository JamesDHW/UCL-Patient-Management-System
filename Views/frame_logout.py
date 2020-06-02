import tkinter as tk


class LogoutFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    LogoutFrame allows users to logout, available from all user views.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Initialise button to logout
        btn_register = tk.Button(self, text="Logout", command=lambda: self.logout())
        btn_register.pack(pady=(50, 50))

    def logout(self):
        self.window.swap_view("Login")
        self.window.email = None


