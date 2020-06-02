import hashlib
import logging
import tkinter as tk
from tkinter import messagebox


class NewAdminFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    NewDocFrame allows Admins to create a new Admin account.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Initialise title
        tk.Label(self, text="Add a New Admin Account", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, pady=(30, 20), padx=(120, 0))

        # Initialise field label
        tk.Label(self, text="Admin email address : ").grid(row=1, column=0, padx=(80, 0), columnspan=3, sticky="E")
        tk.Label(self, text="Repeat email address : ").grid(row=2, column=0, padx=(80, 0), columnspan=3, sticky="E")

        # Initialise entry field
        self.email_entry = tk.Entry(self, width=15)
        self.repeat_entry = tk.Entry(self, width=15)
        self.email_entry.grid(row=1, column=3)
        self.repeat_entry.grid(row=2, column=3)

        # Initialise button to create the new account
        btn_confirm = tk.Button(self, text="Create Account", command=lambda: self.create_account())
        btn_confirm.grid(row=6, column=1, padx=(100, 0), columnspan=3, pady=(30, 20))

    def create_account(self):
        """
        Inserts new values into the table.
        :return: Void.
        """
        email = self.email_entry.get().lower()
        if not self.window.valid_email(email):
            messagebox.showinfo("Information", "Check that the email you entered exists")
            return

        if email != self.repeat_entry.get().lower():
            messagebox.showinfo("Information", "Check that both emails match")
            return

        query_auth = "INSERT INTO Auth VALUES(?, ?, ?)"
        password = hashlib.sha512(self.window.random_str().encode("utf-8")).hexdigest()
        values_auth = (email, password, "Admin")

        try:
            self.window.query(query_auth, values_auth)
        except Exception as e:
            # Error could be that Admin tries to create an existing account
            messagebox.showinfo("Error", "An Error occurred, check that the user doesn't already exist")
            logging.error(e)
        else:
            # Reloads page
            self.window.swap_view("Admin")
