import logging
import tkinter as tk


class PrescriptionsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    PrescriptionsFrame shows a user what their doctor has prescribed them.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window

        query = "SELECT * FROM Prescriptions WHERE username = ?"
        prescriptions = window.query(query, (window.email,))

        if len(prescriptions) > 0:
            tk.Label(self, text="My Prescriptions", font=(None, 18))\
                .grid(row=0, column=0, columnspan=3, padx=(150, 0), pady=(30, 20))

            # All prescriptions
            lb_prescriptions = tk.Listbox(self)
            sb_prescriptions = tk.Scrollbar(self, orient="vertical", command=lb_prescriptions.yview)
            lb_prescriptions.configure(yscrollcommand=sb_prescriptions.set)
            lb_prescriptions.grid(row=7, column=0, columnspan=2, padx=(150, 0))
            sb_prescriptions.grid(row=7, column=2)

            prescription_fields = ["Medicine", "Start Date", "Dose", "Duration", "Frequency", "Note"]
            for i in range(len(prescription_fields)):
                tk.Label(self, text=prescription_fields[i] + ": ", height=2) \
                    .grid(row=i + 1, column=0, sticky="W", padx=(150, 0))

            def reload_prescription():
                if lb_prescriptions.curselection() is None or len(lb_prescriptions.curselection()) == 0:
                    logging.info("No prescription selected")
                    i = 0
                else:
                    i = lb_prescriptions.curselection()[0]
                for j in range(len(prescription_fields)):
                    tk.Label(self, text=prescriptions[i][j+1]+"\t\t\t").grid(row=j+1, column=1, columnspan=3, sticky="W")

            # Initialise prescriptions
            reload_prescription()

            # Add other prescriptions to Listbox to allow user to select and view
            for prescription in prescriptions:
                lb_prescriptions.insert("end", prescription[1])

            btn_view_prescription = tk.Button(self, text="View Prescription",
                                              command=lambda: reload_prescription())
            btn_view_prescription.grid(row=8, column=0, columnspan=3, padx=(150, 0), pady=(30, 20))

        else:
            tk.Label(self, text="No Prescriptions", font=(None, 18))\
                .grid(row=0, column=0, columnspan=5, padx=(150, 0), pady=(30, 20))
