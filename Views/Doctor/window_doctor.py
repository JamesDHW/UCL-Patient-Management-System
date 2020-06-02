import datetime
import logging
import tkinter as tk
from tkinter import ttk, messagebox

from Views.Doctor import frame_appointments as FA
from Views.Doctor import frame_my_patients as MP
from Views.frame_logout import LogoutFrame as LF


class DoctorController(tk.Frame):
    """
    Inherits from tk.Frame.
    DoctorController controls the Doctor view and implements a tkinter Notebook.
    """
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.window = window
        self.top = None
        self.patient = None

        notebook = ttk.Notebook(self)
        notebook.add(FA.AppointmentsFrame(window, self), text='Appointments')
        notebook.add(MP.MyPatientsFrame(window, self), text='My Patients')
        notebook.add(LF(window, self), text="Logout")
        notebook.pack()

    def get_details(self, username):
        """
        Returns necessary details required in both frame_appointments.py and frame_my_patients.py.
        :param username: the email of the patient to return details for
        :return: 2 lists of personal details and any prescriptions respectively
        """
        try:
            # Query to find existing details
            query = "SELECT * FROM Patients WHERE username = ?"
            details = self.window.query(query, (username,))[0]
            # Query to get patient prescriptions
            query = "SELECT * FROM Prescriptions WHERE username = ?"
            prescriptions = self.window.query(query, (username,))
        except IndexError:
            messagebox.showinfo("Warning", "Your details couldn't be found in the database")
            logging.error("No user details returned from query")
        except Exception as e:
            messagebox.showinfo("Warning", "An error occurred whilst retrieving your details")
            logging.error(e)
        else:
            return details, prescriptions

    def details_toplevel(self, lb=None, app_or_patient_IDs=None, patient=None):
        """
        Toplevel created to show the details and prescriptions of a given patient.
        :param lb: Listbox from which selection is made
        :param app_or_patient_IDs: list of appointment ID or patient emails depending on where the funciton is called.
        :param patient: Can optionally give the patient email straight away to avoid the need to deduce this when
        reloading toplevel and this is already known.
        :return: Void.
        """
        # If patient not given, find from selection from Listbox
        if patient is not None:
            self.patient = patient
        elif lb is None or app_or_patient_IDs is None or lb.curselection() is None or len(lb.curselection()) == 0:
            logging.info("No patient selected")
            return
        else:
            # Get patient username depending on where the view details section is selected from
            try:
                query = "SELECT patient FROM Appointments WHERE appID = ?"
                self.patient = self.window.query(query, (app_or_patient_IDs[lb.curselection()[0]],))[0][0]
            except IndexError:
                self.patient = app_or_patient_IDs[lb.curselection()[0]]
                logging.info("Patient viewed from My Patients page")
            except Exception as e:
                logging.error(e)

        details, prescriptions = self.get_details(self.patient)
        self.top = tk.Toplevel()

        patient_details_fields = ["First name", "Middle name", "Last name", "Sex", "DOB", "Mobile no"]
        prescription_fields = ["Medicine", "Start Date", "Dose", "Duration", "Frequency", "Note"]

        def load_prescriptions():
            if lb_prescriptions.curselection() is None or len(lb_prescriptions.curselection()) == 0:
                logging.info("No prescription selected")
                j = 0
            else:
                j = lb_prescriptions.curselection()[0]
            for k in range(len(prescription_fields)):
                tk.Label(frame_presc, text=prescriptions[j][k+1]+"\t").grid(row=k+1, column=4, columnspan=3, sticky="W")

        def delete_prescription():
            if lb_prescriptions.curselection() is None or len(lb_prescriptions.curselection()) == 0:
                logging.info("No prescription selected")
            else:
                prescription = prescriptions[lb_prescriptions.curselection()[0]]
                query = "DELETE FROM Prescriptions WHERE username = ? AND medicine = ? AND startDate = ?"
                try:
                    self.window.query(query, (prescription[0], prescription[1], prescription[2]))
                except Exception as e:
                    messagebox.showinfo("Error", "Prescription couldn't be removed")
                    logging.error(e)
                else:
                    # Reload page
                    self.top.destroy()
                    self.details_toplevel(patient=self.patient)

        def load_notes():
            # Redraws notes Listbox
            tk.Label(frame_details, text="Patient Notes:").grid(row=7, column=0, columnspan=3, sticky="W")
            self.top.lb_notes = tk.Listbox(frame_details, width=50)
            sb_notes = tk.Scrollbar(frame_details, orient="vertical", command=self.top.lb_notes.yview)
            self.top.lb_notes.configure(yscrollcommand=sb_notes.set)

            query = "SELECT * FROM Notes WHERE username = ?"
            notes = self.window.query(query, (self.patient,))

            for note in notes:
                self.top.lb_notes.insert("end", note[0][:10] + " :\t" + note[2])

            self.top.lb_notes.grid(row=8, column=0, columnspan=2)
            sb_notes.grid(row=8, column=2, sticky="W")

            btn_add_note = tk.Button(frame_details, text="Delete Selected Note",
                                     command=lambda: delete_note(self.top.lb_notes, notes))
            btn_add_note.grid(row=10, column=0, columnspan=2, padx=(20, 0), pady=(20, 0))

        def add_note():
            # Adds a note to the Note's table
            if self.top.entry_notes.get() == "":
                return
            try:
                # Query to add a new prescription
                query = "INSERT INTO Notes VALUES(?,?,?)"
                self.window.query(query, (datetime.datetime.today(), self.patient, self.top.entry_notes.get()))
            except Exception as e:
                logging.error(e)
            else:
                self.top.entry_notes.delete(0, "end")
                load_notes()

        def delete_note(lb, notes):
            # Deletes a selected note from the Notes table
            if lb.curselection() is None or len(lb.curselection()) == 0:
                logging.info("No Note selected")
                return
            note = notes[lb.curselection()[0]]
            try:
                # Query to add a new prescription
                query = "DELETE FROM Notes WHERE datetime = ? AND username = ?"
                self.window.query(query, (note[0], self.patient))
            except Exception as e:
                logging.error(e)
            else:
                load_notes()

        # Frame personal details (left hand side of toplevel)
        frame_details = tk.Frame(self.top)
        # Frame prescription details (right hand side of toplevel)
        frame_presc = tk.Frame(self.top)

        # Initialise title
        tk.Label(frame_details, text="Patient Details", font=(None, 18)).grid(row=0, column=0, columnspan=4, pady=(30, 20))

        # Draw details fields and values
        for i in range(len(patient_details_fields)):
            tk.Label(frame_details, text=patient_details_fields[i] + ": ", height=2).grid(row=i+1, column=0, sticky="W")
            if i == 4:
                tk.Label(frame_details, text=str(details[i + 1])[:10]).grid(row=i+1, column=1, columnspan=3, sticky="W")
            else:
                tk.Label(frame_details, text=details[i + 1]).grid(row=i + 1, column=1, columnspan=3, sticky="W")

        # Entry and Button for new notes
        self.top.entry_notes = tk.Entry(frame_details, width=40)
        self.top.entry_notes.grid(row=9, column=0, columnspan=2, padx=(20, 0), pady=(30, 0), sticky="W")
        btn_add_note = tk.Button(frame_details, text="Add Note",
                                 command=lambda: add_note())
        btn_add_note.grid(row=9, column=2, pady=(30, 0))

        # Draw prescriptions fields and values
        if len(prescriptions) > 0:
            # Prescriptions found
            tk.Label(frame_presc, text="Prescriptions", font=(None, 18)).grid(row=0, column=1, columnspan=5, pady=(30, 20))

            for i in range(len(prescription_fields)):
                tk.Label(frame_presc, text=prescription_fields[i] + ": ", height=2).grid(row=i+1, column=2, sticky="W")

            # All prescriptions Listbox
            lb_prescriptions = tk.Listbox(frame_presc)
            sb_prescriptions = tk.Scrollbar(frame_presc, orient="vertical", command=lb_prescriptions.yview)
            lb_prescriptions.configure(yscrollcommand=sb_prescriptions.set)
            lb_prescriptions.grid(row=7, column=2, columnspan=3, pady=(25, 0))
            sb_prescriptions.grid(row=7, column=5, padx=(0, 20), pady=(25, 0))

            for prescription in prescriptions:
                lb_prescriptions.insert("end", prescription[1])

            # Initialise Buttons to view a selected prescription and add a prescription
            btn_view_prescription = tk.Button(frame_presc, text="View Prescription",
                                              command=lambda: load_prescriptions())
            btn_add_prescription = tk.Button(frame_presc, text="Add Prescription",
                                             command=lambda: self.new_prescription_toplevel())
            btn_delete_prescription = tk.Button(frame_presc, text="Delete Prescription",
                                                command=lambda: delete_prescription())
            btn_view_prescription.grid(row=8, column=2, columnspan=3, pady=(30, 20))
            btn_add_prescription.grid(row=9, column=2, columnspan=3, pady=(0, 20))
            btn_delete_prescription.grid(row=10, column=2, columnspan=3, pady=(0, 20))

        else:
            # No prescriptions found
            tk.Label(frame_presc, text="No Prescriptions", font=(None, 18)).grid(row=0, column=1, columnspan=5, pady=(30, 20))

        # Initialise Notes and Prescriptions Listboxes
        load_notes()
        load_prescriptions()

        # Add frames to the toplevel
        frame_details.grid(row=1, column=0, sticky="n", padx=(20, 20), pady=(20, 20))
        frame_presc.grid(row=1, column=1, sticky="n", padx=(20, 20), pady=(20, 20))

    def new_prescription_toplevel(self):
        """
        Creates a toplevel for the doctor to add a new prescription.
        :param parent: the "parent" toplevel, the view details toplevel
        :return: Void.
        """
        presc_top = tk.Toplevel()
        prescription_fields = ["Medicine", "Dose", "Frequency", "Start Date", "Duration", "Note"]

        tk.Label(presc_top, text="New Prescription", font=(None, 18)).grid(row=0, column=0, columnspan=4, pady=(30, 20))

        for i in range(len(prescription_fields)):
            tk.Label(presc_top, text=prescription_fields[i] + ": ", height=2).grid(row=i + 1, column=0, sticky="W")

        # All Medicines
        query = "SELECT medicine FROM Medicines"
        medicines = self.window.query(query)
        for i in range(len(medicines)):
            medicines[i] = medicines[i][0]

        presc_top.med_var = tk.StringVar(self)
        presc_top.med_var.set(medicines[0])
        op_men_med = tk.OptionMenu(presc_top, presc_top.med_var, *medicines)
        op_men_med.grid(row=1, column=1, columnspan=3)

        presc_top.entry_dose = tk.Entry(presc_top)
        presc_top.entry_dose.grid(row=2, column=1, columnspan=3)
        tk.Label(presc_top, text="mg").grid(row=2, column=4)

        # Frequency units
        presc_top.entry_freq = tk.Entry(presc_top)
        presc_top.entry_freq.grid(row=3, column=1, columnspan=3)
        freq_units = [" Per Day", " Per Week", " Per Month"]
        presc_top.freq_var = tk.StringVar(presc_top)
        presc_top.freq_var.set(freq_units[0])
        op_men_duration = tk.OptionMenu(presc_top, presc_top.freq_var, *freq_units)
        op_men_duration.grid(row=3, column=4)

        # Start Date
        start_date = [datetime.date.today() + datetime.timedelta(days=i) for i in range(28)]
        presc_top.start_date_var = tk.StringVar(presc_top)
        presc_top.start_date_var.set(start_date[0])
        op_men_start = tk.OptionMenu(presc_top, presc_top.start_date_var, *start_date)
        op_men_start.grid(row=4, column=1, columnspan=3)

        # Duration & duration units
        presc_top.entry_duration = tk.Entry(presc_top)
        presc_top.entry_duration.grid(row=5, column=1, columnspan=3)
        duration_units = [" Day(s)", " Week(s)", " Months(s)"]
        presc_top.duration_var = tk.StringVar(presc_top)
        presc_top.duration_var.set(duration_units[0])
        op_men_duration = tk.OptionMenu(presc_top, presc_top.duration_var, *duration_units)
        op_men_duration.grid(row=5, column=4)

        presc_top.entry_note = tk.Entry(presc_top)
        presc_top.entry_note.grid(row=6, column=1, columnspan=3)

        btn_new_prescription = tk.Button(presc_top, text="Add Prescription",
                                         command=lambda: new_prescription(presc_top))
        btn_new_prescription.grid(row=7, column=0, columnspan=4, pady=(30, 20))

        def new_prescription(presc_top):
            try:
                dose = float(presc_top.entry_dose.get())
                freq = int(presc_top.entry_freq.get())
                dur = int(presc_top.entry_duration.get())
                if dose <= 0 or freq <= 0 or dur <= 0:
                    return
            except TypeError:
                logging.error("Number fields not valid")
                messagebox.showinfo("Information", "Please Check your number fields")
            except Exception as e:
                logging.error(e)
            else:
                args = (self.patient, presc_top.med_var.get(), presc_top.start_date_var.get(), str(dose) + " mg",
                        str(dur) + presc_top.duration_var.get(), str(freq) + presc_top.freq_var.get(), presc_top.entry_note.get())
                # Query to add a new prescription
                pres_query = "INSERT INTO Prescriptions VALUES(?,?,?,?,?,?,?)"
                try:
                    self.window.query(pres_query, args)
                except Exception as e:
                    messagebox.showinfo("Error", "Task Failed, check for duplicate prescription")
                    logging.error(e)
                else:
                    messagebox.showinfo("Information", "Task Complete")
                    self.top.destroy()
                    self.details_toplevel(patient=self.patient)
                    presc_top.destroy()
