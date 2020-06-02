import logging
import tkinter as tk
from tkinter import messagebox


class AllDoctorsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    AllDoctorsFrame shows all doctors in the database, allowing an Admin to
    search through them and delete or sign into a given account.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Initialise title
        tk.Label(self, text="All Doctors", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, padx=(80, 0), pady=(30, 20))

        # Initialise entry and search button for search bar
        entry_search = tk.Entry(self, width=30)
        entry_search.grid(row=1, column=0, padx=(80, 0))
        btn_search = tk.Button(self, text="Search", command=lambda: self.reload_lb(entry_search.get()))
        btn_search.grid(row=1, column=1)

        # Load the initial Listbox of doctor search results
        self.reload_lb()

        # Initialise buttons to delete a doctor account or sign in as doctor
        btn_delete = tk.Button(self, text="Delete Account",
                               command=lambda: self.delete_account(self.lb_all_doctors, self.doctors_displayed))
        btn_sign_in = tk.Button(self, text="Sign In as Selected User",
                                command=lambda: self.sign_in(self.lb_all_doctors, self.doctors_displayed))
        btn_delete.grid(row=3, column=0, columnspan=2, pady=(30, 20), padx=(80, 0))
        btn_sign_in.grid(row=4, column=0, columnspan=2, pady=(0, 20), padx=(80, 0))

    def reload_lb(self, search=""):
        """
        Draws the Listbox given a search term to look for (searches for similarities in first/ last names and email)
        :param search: search term
        :return: Void.
        """
        if search == "":
            # If there is nothing searched, just return all patients
            query = "SELECT * FROM Doctors"
            doctors = self.window.query(query)
        else:
            search = "%" + search + "%"
            query = "SELECT * FROM Doctors WHERE username LIKE ? OR fName LIKE ? or lName LIKE ?"
            doctors = self.window.query(query, (search, search, search))

        # Initialise all doctors ListBox
        self.lb_all_doctors = tk.Listbox(self, width=40, height=20)
        sb_all_doctors = tk.Scrollbar(self, orient="vertical", command=self.lb_all_doctors.yview)
        self.lb_all_doctors.configure(yscrollcommand=sb_all_doctors.set)
        self.lb_all_doctors.grid(row=2, column=0, columnspan=2, padx=(80, 0))
        sb_all_doctors.grid(row=2, column=2, padx=(0, 20), sticky="ns")

        # Create a list of doctors emails that are displayed and insert entries into Listbox
        self.doctors_displayed = []
        for i in range(len(doctors)):
            doctor = doctors[i]
            self.doctors_displayed.append(doctor[0])
            self.lb_all_doctors.insert("end", doctor[0] + "\t" + doctor[3] + " " + doctor[1] + " " + doctor[2])

    def delete_account(self, lb, doctors):
        """
        Deletes a Doctor account from the database.
        :param lb: Listbox from which selection is made
        :param doctors: List of all doctors displayed in the search
        :return: Void.
        """
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        doctor = doctors[lb.curselection()[0]]
        doctors_query = "DELETE FROM Doctors WHERE username = ?"
        auth_query = "DELETE FROM Auth WHERE username = ?"
        assignments_query = "DELETE FROM Assignments WHERE doctor = ?"
        try:
            self.window.query(doctors_query, (doctor,))
            self.window.query(auth_query, (doctor,))
            self.window.query(assignments_query, (doctor,))
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Error", "Task couldn't be completed")
        else:
            # Reload page
            self.window.swap_view("Admin")

    def sign_in(self, lb, doctors):
        """
        Allows an Admin to sign into a selected Doctor's account.
        :param lb: Listbox from which selection is made
        :param doctors: List of all doctors displayed in the search
        :return:
        """
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        doctor = doctors[lb.curselection()[0]]
        self.window.email = doctor
        # Swap view as selected doctor
        logging.info("Admin Logged in as " + doctor)
        self.window.swap_view("Doctor")
