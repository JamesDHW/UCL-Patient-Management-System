import tkinter as tk
from tkinter import ttk

from Views.Patient.frame_appointments import AppointmentsFrame as FA
from Views.Patient.frame_edit_details import EditDetailsFrame as FE
from Views.Patient.frame_my_doctor import MyDoctorFrame as FM
from Views.Patient.frame_prescriptions import PrescriptionsFrame as FP
from Views.frame_logout import LogoutFrame as LF


class PatientController(tk.Frame):
    """
    Inherits from tk.Frame
    PatientController controls the Patient view and implements a tkinter Notebook.
    """
    def __init__(self, window):
        tk.Frame.__init__(self, window)

        notebook = ttk.Notebook(self)
        notebook.add(FA(window, self), text="Appointments")
        notebook.add(FE(window, self), text="Edit Details")
        notebook.add(FM(window, self), text="My Doctor")
        notebook.add(FP(window, self), text="My Prescriptions")
        notebook.add(LF(window, self), text="Logout")
        notebook.pack()



