import logging
import tkinter as tk
from tkinter import messagebox


class MyDoctorFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    MyDoctorFrame is a shows the patient the details of their doctor, allows them to find their doctor, and send a short
    message to their doctor via email (without revealing the doctor's email address)
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.top = None
        try:
            query = "SELECT * FROM Doctors WHERE username = (SELECT doctor FROM Patients WHERE username = ?)"
            details = window.query(query, (window.email,))[0]
        except IndexError:
            # Have they selected a doctor yet?
            query = "SELECT * FROM Assignments WHERE patient = ?"
            if len(window.query(query, (window.email,))) == 0:
                # No doctor selected
                logging.info("Doctor not selected yet")
                tk.Label(self, text="You haven't selected your doctor yet", font=(None, 18)) \
                    .grid(row=0, column=0, columnspan=5, padx=(100, 0), pady=(30, 20))

                # Button to show toplevel to allow user to select their doctor
                btn_select = tk.Button(self, text="Select Your Doctor", command=lambda: self.select_doctor_toplevel())
                btn_select.grid(row=1, column=0, padx=(150, 0))
            else:
                logging.info("Waiting for confirmation from your Doctor")
                tk.Label(self, text="Waiting for confirmation from your doctor", font=(None, 18)) \
                    .grid(row=0, column=0, columnspan=5, padx=(100, 0), pady=(30, 20))
        except Exception as e:
            messagebox.showinfo("Warning", "An error occurred whilst retrieving your doctor's details")
            logging.error(e)
        else:
            tk.Label(self, text="Your Doctor", font=(None, 18)) \
                .grid(row=0, column=0, columnspan=5, padx=(150, 0), pady=(30, 20))

            tk.Label(self, text="Name : ", height=2).grid(row=1, column=0, padx=(150, 0), sticky="W")
            tk.Label(self, text="Position : ", height=2).grid(row=2, column=0, padx=(150, 0), sticky="W")
            tk.Label(self, text="Send Short Message : ", height=2).grid(row=3, column=0, padx=(50, 0), sticky="W")

            tk.Label(self, text=details[3] + " " + details[1] + " " + details[2], height=2).grid(row=1, column=1,
                                                                                                 sticky="W")
            tk.Label(self, text=details[4], height=2).grid(row=2, column=1, sticky="W")
            entry_contact = tk.Entry(self)
            entry_contact.grid(row=3, column=1, sticky="W")

            # Button to send email to patient's doctor (rather than showing email for contact)
            btn_contact = tk.Button(self, text="Send Message",
                                    command=lambda: self.window.send_email(details[0], entry_contact.get(),
                                                                           "Patient Message from "+self.window.email))
            btn_contact.grid(row=3, column=2, sticky="W")

    def select_doctor_toplevel(self, search=""):
        try:
            details_query = "SELECT fName, mName, lName, sex, DOB, mobile FROM Patients WHERE username = ?"
            details = self.window.query(details_query, (self.window.email,))[0]
        except IndexError:
            messagebox.showinfo("Error", "Couldn't finding your details")
            return
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Error", "Error loading details")
            return
        else:
            if "-" in details or "0" in details:
                messagebox.showinfo("Information", "Please fill out all your details before selecting a doctor")
                return

        # Initialise toplevel
        if self.top is not None:
            self.top.destroy()
        self.top = tk.Toplevel()

        tk.Label(self.top, text="Search for your Doctor by name : ", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, pady=(30, 20))

        search_entry = tk.Entry(self.top)
        search_entry.insert(0, search[1:-1])
        search_entry.grid(row=1, column=0, columnspan=3, padx=(10, 0))

        # Button to search
        btn_search = tk.Button(self.top, text="Search",
                               command=lambda: self.select_doctor_toplevel(search="%"+search_entry.get().lower()+"%"))
        btn_search.grid(row=1, column=3)

        if search == "":
            query = "SELECT * FROM Doctors"
            results = self.window.query(query)
        else:
            query = "SELECT * FROM Doctors WHERE LOWER(fName) LIKE ? or LOWER(lName) LIKE ?"
            results = self.window.query(query, (search, search))

        lb_doctors = tk.Listbox(self.top, width=30, height=20)
        lb_doctors.grid(row=2, column=0, columnspan=4, padx=(10, 0))
        sb_prescriptions = tk.Scrollbar(self.top, orient="vertical", command=lb_doctors.yview)
        sb_prescriptions.grid(row=2, column=4, padx=(0, 10))

        doctors = []
        for i in range(len(results)):
            doctors.append(results[i][0])
            lb_doctors.insert("end", results[i][3] + " " + results[i][1] + " " + results[i][2])

        # Button to select searched doctor
        btn_select = tk.Button(self.top, text="This is my doctor",
                               command=lambda: self.select_my_doctor(lb_doctors, doctors))
        btn_select.grid(row=3, column=0, columnspan=4, pady=(30, 20))

    def select_my_doctor(self, lb, doctors):
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        doctor = doctors[lb.curselection()[0]]
        try:
            query = "INSERT INTO Assignments VALUES(?, ?)"
            self.window.query(query, (self.window.email, doctor))
        except Exception as e:
            logging.error(e)
            query = "UPDATE Assignments SET doctor = ? WHERE patient = ?"
            self.window.query(query, (doctor, self.window.email))
        finally:
            self.window.swap_view("Patient")
            self.top.destroy()
