import hashlib  # https://docs.python.org/3/library/hashlib.html
import logging
import tkinter as tk
from tkinter import ttk, messagebox

from Views.Login.frame_login import LoginFrame as LF
from Views.Login.frame_recover import RecoverFrame as RecF
from Views.Login.frame_register import RegisterFrame as RegF


class LoginController(tk.Frame):
    """
    LoginController inherits from tk.Frame.
    :param window: the Window object within which the LoginController in packed.
    :return: Void.
    """
    def __init__(self, window):
        tk.Frame.__init__(self, window)

        # Initialise logo on login screen
        global logo_photo
        logo_photo = tk.PhotoImage(file="Data/UCH_logo.png")
        tk.Label(self, image=logo_photo).grid(row=0, column=0)

        # Define ttk.notebook and add frames to login and register
        notebook = ttk.Notebook(self)
        notebook.add(LF(window, self), text="Login")
        notebook.add(RegF(window, self), text="Register")
        notebook.add(RecF(window, self), text="Recover Account")
        notebook.grid(row=1, column=0)

    @staticmethod
    def valid_pass(password):
        numbers = "0123456789"
        special = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        # List comprehension to find any numbers/ special characters in the password
        nValid = [x for x in password if x in numbers]
        sValid = [x for x in password if x in special]
        # Returns True if there is a number, a special, and at least 8 characters
        if (len(nValid) > 0) and (len(sValid) > 0) and (len(password) > 7):
            return True
        else:
            logging.info("invalid password entered")
            messagebox.showinfo("Information", "Your password must contain 8 characters including a number and a "
                                               "special character")
            return False

    @staticmethod
    def hash_pass(password):
        # salt = uuid.uuid4().hex # Add a salt later
        hashed = hashlib.sha512(password.encode("utf-8")).hexdigest()
        return hashed
