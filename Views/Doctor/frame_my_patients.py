import logging
import tkinter as tk


class MyPatientsFrame(tk.Frame):
    """This class shows all assigned patients to a doctor"""

    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.parent = parent

        self.draw_page()

    def draw_page(self, search=""):

        query_assign = "SELECT username, fName, lName FROM Patients WHERE username = " \
                "(SELECT patient FROM Assignments WHERE doctor = ?)"
        assign = self.window.query(query_assign, (self.window.email,))

        search = "%" + search + "%"
        query_patients = "SELECT * FROM Patients WHERE doctor = ? AND (username LIKE ? OR fName LIKE ? OR lName LIKE?)"
        patients = self.window.query(query_patients, (self.window.email, search, search, search))

        # All patients waiting to be assigned
        self.lb_assignments = tk.Listbox(self, width=40, height=5)
        sb_assignments = tk.Scrollbar(self, orient="vertical", command=self.lb_assignments.yview)
        self.lb_assignments.configure(yscrollcommand=sb_assignments.set)

        # All assigned patients
        self.lb_patients = tk.Listbox(self, width=40, height=20)
        sb_patients = tk.Scrollbar(self, orient="vertical", command=self.lb_patients.yview)
        self.lb_patients.configure(yscrollcommand=sb_patients.set)

        all_patients = []
        for i in range(len(patients)):
            all_patients.append(patients[i][0])
            self.lb_patients.insert("end", patients[i][1] + " " + patients[i][3])

        all_assignments = []
        for i in range(len(assign)):
            if assign[i][0] not in all_patients:
                all_assignments.append(assign[i][0])
                self.lb_assignments.insert("end", assign[i][1] + " " + assign[i][2])

        # Define buttons to assign/ deny patient assignment and view patient details/ prescriptions
        btn_confirm = tk.Button(self, text="Confirm my Patient",
                                command=lambda: self.assign_patient(self.lb_assignments, all_assignments, True))
        btn_deny = tk.Button(self, text="Not my Patient",
                             command=lambda: self.assign_patient(self.lb_assignments, all_assignments, False))
        btn_details = tk.Button(self, text="View Details",
                                command=lambda: self.parent.details_toplevel(self.lb_patients, all_patients))

        i = 0
        # If we need to draw a listBox for assignment requests
        if len(assign) != 0:
            i = 4
            tk.Label(self, text="Assign Patients", font=(None, 18))\
                .grid(row=0, column=1, columnspan=5, padx=(150, 0), pady=(20, 20))

            self.lb_assignments.grid(row=1, column=1, columnspan=2, padx=(150, 0))
            sb_assignments.grid(row=1, column=3, sticky="ns")
            btn_confirm.grid(row=2, column=1, columnspan=2, padx=(150, 0), pady=(10, 5))
            btn_deny.grid(row=3, column=1, columnspan=2, padx=(150, 0))

        tk.Label(self, text="My Patients", font=(None, 18))\
            .grid(row=0+i, column=1, columnspan=5, padx=(150, 0), pady=(30, 20))

        entry_search = tk.Entry(self, width=30)
        btn_search = tk.Button(self, text="Search", command=lambda: self.draw_page(entry_search.get()))
        entry_search.grid(row=1+i, column=1, padx=(150, 0))
        btn_search.grid(row=1+i, column=2)

        self.lb_patients.grid(row=2+i, column=1, columnspan=2, padx=(150, 0))
        sb_patients.grid(row=2+i, column=3, sticky="ns")

        btn_details.grid(row=3+i, column=1, columnspan=2, padx=(150, 0), pady=(30, 20))

    def assign_patient(self, lb, patients, confirmed):
        if lb.curselection() is None or len(lb.curselection()) == 0:
            logging.info("No patient selected")
            return
        else:
            patient = patients[lb.curselection()[0]]

        if confirmed:
            query = "UPDATE Patients SET doctor = ? WHERE username = ?"
            self.window.query(query, (self.window.email, patient))
        else:
            msg = "Dear patient, \n\tYour request for doctor assignment has not been successful, please ensure that " \
                  "you have selected the correct doctor and try selection again. \n\nKind regards,\nUCH Care Team "
            self.window.send_email(patient, msg, subject="Doctor Assignment")

        query = "DELETE FROM Assignments WHERE patient = ?"
        self.window.query(query, (patient,))
        self.window.swap_view("Doctor")

