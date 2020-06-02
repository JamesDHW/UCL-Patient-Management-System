import logging
import tkinter as tk
from tkinter import messagebox


class AddNewMedicine(tk.Frame):
    """
    Inherits from tk.Frame.
    AddNewMedicine allows Admins to edit which medicines doctors can prescribe.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        # Remove Medicines
        tk.Label(self, text="Remove Available Medicines", font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5, padx=(150, 0), pady=(30, 20))

        # Get all Medicines
        query = "SELECT medicine FROM Medicines"
        medicines = window.query(query)

        # Populate a Listbox with all existing medicines
        lb_medicines = tk.Listbox(self)
        lb_medicines.grid(row=1, column=0, columnspan=2, padx=(150, 0))
        for i in range(len(medicines)):
            lb_medicines.insert("end", medicines[i][0])
            medicines[i] = medicines[i][0]

        # Initialise button to delete the selected medicine
        btn_delete_med = tk.Button(self, text="Delete Selected Medicine",
                                   command=lambda: self.delete_med(lb_medicines, medicines))
        btn_delete_med.grid(row=2, column=0, columnspan=2, padx=(150, 0), pady=(30, 20))

        # Add a Medicine
        tk.Label(self, text="Add Medicine", font=(None, 18)) \
            .grid(row=3, column=0, columnspan=5, padx=(150, 0), pady=(30, 20))

        # Add entries and titles for fields for new medicine
        tk.Label(self, text="Name of Medicine").grid(row=4, column=0, padx=(150, 0), sticky="SE")
        tk.Label(self, text="What it treats").grid(row=5, column=0, padx=(150, 0), sticky="NE")
        self.entry_med = tk.Entry(self, width="15")
        self.entry_med.grid(row=4, column=1, sticky="S")
        self.entry_treats = tk.Entry(self, width="15")
        self.entry_treats.grid(row=5, column=1, sticky="N")

        # Initialise button to add new medicine
        btn_add_med = tk.Button(self, text="Add New Medicine", command=lambda: self.add_med())
        btn_add_med.grid(row=6, column=0, columnspan=2, padx=(150, 0), pady=(30, 20))

    def delete_med(self,  lb, medicines):
        """
        Deletes a medicine from the database.
        :param lb: Listbox from which selection is made
        :param medicines: List of all medicines
        :return: Void.
        """
        # Check that there is a selection made
        if lb.curselection() is None or len(lb.curselection()) == 0:
            logging.info("No patient selected")
            return
        medicine = medicines[lb.curselection()[0]]
        query = "DELETE FROM Medicines WHERE medicine = ?"
        self.window.query(query, (medicine,))
        # Reload page
        self.window.swap_view("Admin")

    def add_med(self):
        """
        Adds a new medicine to the database.
        :return: Void.
        """
        query = "INSERT INTO Medicines VALUES(?,?)"
        try:
            self.window.query(query, (self.entry_med.get(), self.entry_treats.get()))
        except Exception as e:
            # Exception could occur when a user tries to input a preexisting medicine
            messagebox.showinfo("Warning", "An error has occurred, ")
            logging.error(e)
        else:
            # Reload page
            self.window.swap_view("Admin")
