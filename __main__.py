import logging
import random                           # DOCUMENTATION REFERENCES
import smtplib                          # https://docs.python.org/3/library/smtplib.html
import sqlite3                          # https://docs.python.org/3/library/sqlite3.html
import tkinter as tk                    # https://tkdocs.com/
from email.message import EmailMessage
from tkinter import messagebox

# Import my modules
from Views.Admin.window_admin import AdminController as Admin
from Views.Doctor.window_doctor import DoctorController as Doctor
from Views.Login.window_login import LoginController as Login
from Views.Patient.window_patient import PatientController as Patient

# Set logging preferences
logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    filemode='w',
                    format='%(module)s - %(levelname)s - %(message)s')


class Window(tk.Tk):
    """
    This is the controller class for the patient management system.
    The Window class inherits from the tkinter window 'Tk', as Window objects represent the main program window.
    This class can be accessed by view objects as 'parent' in order to swap view objects.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("UCH Care")
        self.email = None
        self.view = Login(self)
        self.view.pack()

    def swap_view(self, view_key):
        """
        This class destroys a current frame and populates the window with a new frame of a specified role.

        :param view_key: contains the key holding the class for that view.
        :return: void.
        """
        view_dict = {"Login": Login, "Admin": Admin, "Doctor": Doctor, "Patient": Patient}

        try:
            # Check the role of user inside method (prevent calling of this method by anyone to sign in as an admin)
            query = "SELECT role FROM Auth WHERE username = ?"
            role = self.query(query, (self.email,))[0][0]
        except IndexError:
            messagebox.showinfo("Error", "Unable to find user in database")
        except Exception as e:
            logging.error(e)
        else:
            if role == view_key or role == "Admin" or view_key == "Login":
                if self.view is not None:
                    self.view.destroy()
                self.view = view_dict[view_key](self)
                self.view.pack()
            else:
                logging.info(role + " tried to switch view to " + view_key)

    @staticmethod
    def query(sql, params=()):
        """
        Queries the uch_care.db database. Returns SELECT, otherwise executes query
        :param params: any parameters that need to be bound to the sql statement, defaults to empty tuple.
        :param sql: the sql to be executed.
        :return: list of tuples containing results.
        """
        try:
            connection = sqlite3.connect('Data/uch_care.db')
        except FileNotFoundError:
            messagebox.showinfo("Warning", "Failed to connect")
            logging.error("Failed to find Data/uch_care.db")
        except Exception as e:
            messagebox.showinfo("Warning", "Failed to connect")
            logging.error("Failed to connect to database: ", e)
        else:
            cursor = connection.cursor()
            if sql[:6] == "SELECT":
                cursor.execute(sql, params)
                return cursor.fetchall()
            else:
                cursor.execute(sql, params)
                connection.commit()
            connection.close()

    @staticmethod
    def send_email(to_email, content, subject="UCH Care", from_email="UCL.Care.JDHW@gmail.com"):
        """
        Can be called to send an email to a user.
        :param from_email: By default emails sent from this email
        :param subject: the subject of the email.
        :param content: the message to be sent to the user.
        :param to_email: the email address to send the message to.
        :return: void.
        """
        print("REMOVED EMAIL FUNCTIONALITY FOR GITHUB")
        # msg = EmailMessage()
        #
        # msg["To"] = to_email
        # msg["Subject"] = subject
        # msg.set_content(content)
        # msg["From"] = from_email
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.send_message(msg)
        # server.quit()

    @staticmethod
    def valid_email(email):
        """
        Check to see if a given email is in a reasonable form.
        :param email: the given email as a string.
        :return: boolean.
        """
        if len(email) > 5 and email != "" and "@" in email and "." in email:
            return True
        else:
            messagebox.showinfo("Information", "Invalid email")
            return False

    @staticmethod
    def random_str(length=32):
        """
        Generates a string of given length to be used for appointment IDs and temporary passwords
        :param length: length of string to generate
        :return: String.
        """
        chars = "0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ!_?<>/'{}[]()*&^%$£@"
        password = ""
        for i in range(length):
            char = random.randrange(len(chars))
            password += chars[char]
        return password


if __name__ == "__main__":
    Session = Window()  # Create Window object
    Session.mainloop()  # Draw Window
