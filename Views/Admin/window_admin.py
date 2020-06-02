import tkinter as tk
from tkinter import ttk

from Views.Admin.frame_add_medicine import AddNewMedicine as AM
from Views.Admin.frame_all_doctors import AllDoctorsFrame as AD
from Views.Admin.frame_all_patients import AllPatientsFrame as AP
from Views.Admin.frame_new_admin import NewAdminFrame as NA
from Views.Admin.frame_new_doctor import NewDocFrame as ND
from Views.frame_logout import LogoutFrame as LF


class AdminController(tk.Frame):
    """
    Inherits from tk.Frame.
    AdminController controls the Admin view and implements a tkinter Notebook.
    """
    def __init__(self, window):
        tk.Frame.__init__(self, window)

        notebook = ttk.Notebook(self)
        notebook.add(AD(window, self), text="All Doctors")
        notebook.add(AP(window, self), text="All Patients")
        notebook.add(ND(window, self), text="New GP")
        notebook.add(NA(window, self), text="New Admin")
        notebook.add(AM(window, self), text="Medicines")
        notebook.add(LF(window, self), text="Logout")
        notebook.pack()


