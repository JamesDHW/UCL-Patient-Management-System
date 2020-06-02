import csv
import logging
import pickle
import tkinter as tk
from tkinter import messagebox


class LoginFrame(tk.Frame):
    """
    Inherits from the tk.Frame.
    LoginFrame allows users to log in to any user account.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.parent = parent

        # Initialise entry labels
        tk.Label(self, text="Username:").grid(row=0, column=0)
        tk.Label(self, text="Password:").grid(row=1, column=0)
        tk.Label(self, text="Remember me").grid(row=2, column=0)

        # Initialise login entry fields
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        # Initialise save details checkbutton
        self.var = tk.IntVar()
        self.cb_save_details = tk.Checkbutton(self, variable=self.var)
        self.cb_save_details.grid(row=2, column=1, sticky="W")

        # Initialise button to login
        btn_verify_auth = tk.Button(self, text="Login", width=7, command=lambda: self.verify_auth())
        btn_verify_auth.grid(row=3, column=0, columnspan=2, pady=(30, 20))

        # Check for locally saved details
        self.read_local_auth()

    def verify_auth(self):
        email = self.entry_username.get().lower()
        password = self.parent.hash_pass(self.entry_password.get())

        # Return if email given is valid form
        # Technically not needed
        if not self.window.valid_email(email):
            return

        try:
            # Query database for existence of user
            user_auth = self.window.query("SELECT * FROM Auth WHERE username = ?", (email,))
        except Exception as e:
            logging.error(e)
        else:
            if len(user_auth) == 1:
                # If only one user is found
                if user_auth[0][1] == password:
                    self.save_local_auth(self.var.get())
                    self.window.email = email
                    self.window.swap_view(user_auth[0][2])
                else:
                    messagebox.showinfo("Information", "Invalid password")
            else:
                messagebox.showinfo("Information", "This email couldn't be found")
                logging.info("couldn't find user")

    def read_local_auth(self):
        try:
            file = open("Data/local_auth.p", "rb")
            with file:
                auth = pickle.load(file)
        except FileNotFoundError:
            logging.error("local_auth.p couldn't be found")
        except EOFError:
            logging.info("No auth saved")
        except Exception as e:
            logging.error(e)
        else:
            if auth is not None:
                self.entry_username.insert(0, auth["username"])
                self.entry_password.insert(0, auth["password"])
                self.cb_save_details.select()

    def save_local_auth(self, checked):
        try:
            file = open("Data/local_auth.p", 'wb')
        except FileNotFoundError:
            logging.error("local_auth.p couldn't be found")
        except Exception as e:
            logging.error(e)
        else:
            auth = {"username": self.entry_username.get(), "password": self.entry_password.get()}
            if checked:
                pickle.dump(auth, file)
