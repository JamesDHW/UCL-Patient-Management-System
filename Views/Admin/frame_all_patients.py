import logging
import tkinter as tk
from tkinter import messagebox


class AllPatientsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    AllPatientsFrame shows all patients in the database and allows admins to remove patient assignments,
    delete patient accounts and sign in as a given patient account"""
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Initialise title
        tk.Label(self, text="All Patients", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, padx=(80, 0), pady=(30, 20))

        # Initialise entry and search button for search bar
        entry_serach = tk.Entry(self, width=30)
        entry_serach.grid(row=1, column=0, padx=(80, 0))
        btn_search = tk.Button(self, text="Search", command=lambda: self.reload_lb(entry_serach.get()))
        btn_search.grid(row=1, column=1)

        # Load the initial Listbox of patient search results
        self.reload_lb()

        # Initialise buttons to delete a patient account, remove patient-doctor assignment or sign in as patient
        btn_delete = tk.Button(self, text="Delete Account",
                                command=lambda: self.delete_account(self.lb_all_patients, self.patients_displayed))
        btn_deassign = tk.Button(self, text="De Assign from Current Doctor",
                                command=lambda: self.deassign(self.lb_all_patients, self.patients_displayed))
        btn_sign_in = tk.Button(self, text="Sign In as Selected User",
                                command=lambda: self.sign_in(self.lb_all_patients, self.patients_displayed))
        btn_delete.grid(row=3, column=0, columnspan=2, pady=(30, 20), padx=(80, 0))
        btn_deassign.grid(row=4, column=0, columnspan=2, pady=(0, 20), padx=(80, 0))
        btn_sign_in.grid(row=5, column=0, columnspan=2, pady=(0, 20), padx=(80, 0))

    def reload_lb(self, search=""):
        """
        Draws the Listbox given a search term to look for (searches for similarities in first/ last names and email)
        :param search: search term
        :return: Void.
        """
        if search == "":
            # If there is nothing searched, just return all patients
            query = "SELECT * FROM Patients"
            patients = self.window.query(query)
        else:
            search = "%" + search + "%"
            query = "SELECT * FROM Patients WHERE username LIKE ? OR fName LIKE ? or lName LIKE ?"
            patients = self.window.query(query, (search, search, search))

        # Initialise all patients ListBox
        self.lb_all_patients = tk.Listbox(self, width=40, height=20)
        sb_all_patients = tk.Scrollbar(self, orient="vertical", command=self.lb_all_patients.yview)
        self.lb_all_patients.configure(yscrollcommand=sb_all_patients.set)
        self.lb_all_patients.grid(row=2, column=0, columnspan=2, padx=(80, 0))
        sb_all_patients.grid(row=2, column=2, padx=(0, 20), sticky="ns")

        # Create a list of patients emails that are displayed and insert entries into Listbox
        self.patients_displayed = []
        for i in range(len(patients)):
            patient = patients[i]
            self.patients_displayed.append(patient[0])
            self.lb_all_patients.insert("end", patient[0] + "\t" + patient[1] + " "
                                        + patient[3] + "\t Doctor: " + patient[7])

    def delete_account(self, lb, patients):
        """
        Deletes a Patient account from the database.
        :param lb: Listbox from which selection is made
        :param patients: List of all patients displayed in the search
        :return: Void.
        """
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        patient = patients[lb.curselection()[0]]
        patients_query = "DELETE FROM Patients WHERE username = ?"
        auth_query = "DELETE FROM Auth WHERE username = ?"
        assignments_query = "DELETE FROM Assignments WHERE patient = ?"
        try:
            self.window.query(patients_query, (patient,))
            self.window.query(auth_query, (patient,))
            self.window.query(assignments_query, (patient,))
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Error", "Task couldn't be completed")
        else:
            self.window.swap_view("Admin")

    def deassign(self, lb, patients):
        """
        Removes the doctor-patient assignment.
        :param lb: Listbox from which selection is made
        :param patients: List of all patients displayed in the search
        :return: Void.
        """
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        patient = patients[lb.curselection()[0]]
        patients_query = "UPDATE Patients SET doctor = '-' WHERE username = ?"
        assignments_query = "DELETE FROM Assignments WHERE patient = ?"
        try:
            self.window.query(patients_query, (patient,))
            self.window.query(assignments_query, (patient,))
        except Exception as e:
            messagebox.showinfo("Error", "Task couldn't be completed")
            logging.error(e)
        else:
            # Reload page
            self.window.swap_view("Admin")

    def sign_in(self, lb, patients):
        """
        Allows an Admin to sign into a selected Patient's account.
        :param lb: Listbox from which selection is made
        :param patients: List of all patients displayed in the search
        :return: Void.
        """
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        patient = patients[lb.curselection()[0]]
        self.window.email = patient
        # Swap view to patient
        logging.info("Admin Logged in as " + patient)
        self.window.swap_view("Patient")
