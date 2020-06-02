import hashlib
import logging
import tkinter as tk
from tkinter import messagebox


class NewDocFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    NewDocFrame allows Admins to create a new Doctor account.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Initialise title
        tk.Label(self, text="Add a New Doctor Account", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, pady=(30, 20), padx=(150, 0))

        # Initialise field labels
        tk.Label(self, text="NHS email address : ").grid(row=1, column=0, padx=(80, 0), columnspan=3, sticky="E")
        tk.Label(self, text="First Name : ").grid(row=2, column=0, columnspan=3, padx=(80, 0), sticky="E")
        tk.Label(self, text="Last Name : ").grid(row=3, column=0, columnspan=3, sticky="E")
        tk.Label(self, text="Honorific : ").grid(row=4, column=0, columnspan=3, sticky="E")
        tk.Label(self, text="Job Role : ").grid(row=5, column=0, columnspan=3, sticky="E")

        # Initialise entry fields
        self.email_entry = tk.Entry(self, width=15)
        self.email_entry.grid(row=1, column=3, columnspan=3, sticky="W")
        self.f_name_entry = tk.Entry(self, width=15)
        self.f_name_entry.grid(row=2, column=3, columnspan=3, sticky="W")
        self.l_name_entry = tk.Entry(self, width=15)
        self.l_name_entry.grid(row=3, column=3, columnspan=3, sticky="W")

        # Initialise honorific drop-down menu
        honorifics = ["Dr", "Miss", "Mr", "Mrs", "Ms"]
        self.hon_var = tk.StringVar(self)
        self.hon_var.set(honorifics[0])
        op_men_hon = tk.OptionMenu(self, self.hon_var, *honorifics)
        op_men_hon.grid(row=4, column=3, sticky="W")

        # Initialise option for type of doctor
        doc_type = ["GP"]
        self.doc_var = tk.StringVar(self)
        self.doc_var.set(doc_type[0])
        op_men_doc = tk.OptionMenu(self, self.doc_var, *doc_type)
        op_men_doc.grid(row=5, column=3, sticky="W")

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

        query_auth = "INSERT INTO Auth VALUES(?, ?, ?)"
        query_doctors = "INSERT INTO Doctors VALUES(?, ?, ?, ?, ?)"

        password = hashlib.sha512(self.window.random_str().encode("utf-8")).hexdigest()
        values_auth = (email, password, "Doctor")
        values_doctors = (email, self.f_name_entry.get(),
                          self.l_name_entry.get(), self.hon_var.get(), self.doc_var.get())
        try:
            self.window.query(query_auth, values_auth)
            self.window.query(query_doctors, values_doctors)
        except Exception as e:
            # Error could be that Admin tries to create an existing account
            messagebox.showinfo("Error", "An Error occurred, check that the user doesn't already exist")
            logging.error(e)
        else:
            # Reloads page
            self.window.swap_view("Admin")
