import logging
import tkinter as tk
from random import randint
from tkinter import messagebox


class RecoverFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    RecoverFrame allows any user type to recover a password, same functionality as
    register frame but updates password instead of creating a new account.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.parent = parent
        self.email = None
        self.email_code = None

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
        btn_register = tk.Button(self, text="Recover Account", command=lambda: self.recover_account())
        btn_register.grid(row=4, column=0, columnspan=2, pady=(30,20))

    def send_code(self):
        # Update code to prevent doubly sending it
        self.email_code = randint(100000, 999999)
        self.email = self.entry_username.get().lower()
        content = "Dear User, \n\nPlease use the code " \
                  + str(self.email_code) \
                  + " to recover your account. \n\nKind regards, \nUCL Care Team."
        subject = "UCL Care Recovery"
        to_email = self.entry_username.get().lower()

        if self.window.valid_email(to_email):
            self.window.send_email(to_email, content, subject=subject)

    def recover_account(self):
        email = self.email
        password = self.entry_password.get()
        code_entered = self.entry_code.get()

        if email is None:
            messagebox.showinfo("Information", "Please enter your email and generate an email code before registering")
            return
        if not self.parent.valid_pass(password):
            logging.info("invalid password")
            return
        try:
            code_entered = int(code_entered)
        except ValueError:
            logging.info("non-numeric code input")
            messagebox.showinfo("Information", "The code must be a number")
        except Exception as e:
            logging.error(e)
        else:
            if code_entered == self.email_code and self.entry_password.get() == self.entry_repeat.get():
                try:
                    query = "SELECT * FROM Auth WHERE username = ?"
                    user = self.window.query(query, (email,))[0]
                except IndexError:
                    # User could try to change their password before registering
                    messagebox.showinfo("Information", "Couldn't find this user, please register")
                except Exception as e:
                    logging.error(e)
                else:
                    try:
                        query = "UPDATE Auth SET password = ? WHERE username = ?"
                        self.window.query(query, (self.parent.hash_pass(password), email))
                        logging.error("Password updated")
                        messagebox.showinfo("Information", "Success")
                    except Exception as e:
                        logging.error("Failed to update password")
                        logging.error(e)
                        messagebox.showinfo("Information", "Failed to update password")
            elif code_entered != self.email_code:
                logging.info("incorrect email code")
                messagebox.showinfo("Information", "Code incorrect")
            elif self.entry_password.get() != self.entry_repeat.get():
                logging.info("passwords don't match")
                messagebox.showinfo("Information", "Your passwords don't match")
