import logging
import tkinter as tk
from random import randint
from tkinter import messagebox


class RegisterFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    RegisterFrame allows input to register a new patient (only patients).
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.parent = parent
        self.email_code = None
        self.email = None

        # Initialise entry labels
        tk.Label(self, text=" Email Address: ").grid(row=0, column=0)
        tk.Label(self, text="Create Password: ").grid(row=1, column=0)
        tk.Label(self, text="Repeat Password: ").grid(row=2, column=0)

        # Initialise entry fields
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_repeat = tk.Entry(self, show="*")
        self.entry_code = tk.Entry(self)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.entry_repeat.grid(row=2, column=1)
        self.entry_code.grid(row=3, column=1)

        # Initialise button to send confirmation email
        btn_confirm = tk.Button(self, text="Generate Email Code", command=lambda: self.send_code())
        btn_confirm.grid(row=3, column=0)

        # Initialise button to register
        btn_register = tk.Button(self, text="Register Account", command=lambda: self.register_account())
        btn_register.grid(row=4, column=0, columnspan=2, pady=(30, 20))

    def send_code(self):
        # save the email that the code was sent to so the user can't change it after sending the code
        # and update code to prevent doubly sending it
        self.email_code = randint(100000, 999999)
        self.email = self.entry_username.get().lower()
        content = "Dear New User, \n\nPlease use the code " \
                  + str(self.email_code) \
                  + " to verify your account. \n\nKind regards, \nUCL Care Team."
        subject = "UCL Care Confirmation"
        to_email = self.entry_username.get().lower()

        if self.window.valid_email(to_email):
            self.window.send_email(to_email, content, subject=subject)

    def register_account(self):
        email = self.email
        password = self.entry_password.get()
        code_entered = self.entry_code.get()

        # Check valid email and passwords given
        if email is None:
            messagebox.showinfo("Information", "Please enter your email and generate an email code before registering")
            return
        if not self.window.valid_email(email):
            return
        if not self.parent.valid_pass(password):
            return

        try:
            code_entered = int(code_entered)
        except ValueError:
            logging.info("non-numeric code input")
            messagebox.showinfo("Information", "The code must be a number")
        except Exception as e:
            logging.error(e)
        else:
            if code_entered == self.email_code:
                try:
                    query = "INSERT INTO Auth VALUES(?, ?, ?)"
                    self.window.query(query, (email, self.parent.hash_pass(password), "Patient"))
                    query = "INSERT INTO Patients VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
                    self.window.query(query, (email, '-', '-', '-', '-', 0, 0, '-'))
                except Exception as e:
                    logging.error("Failed to insert values into tables")
                    logging.error(e)
                    messagebox.showinfo("Information", "This account already exists")
                else:
                    messagebox.showinfo("Information", "Your registration is complete")
            elif code_entered == self.email_code:
                logging.info("incorrect email code")
                messagebox.showinfo("Information", "Code incorrect")
