import datetime
import logging
import tkinter as tk
from tkinter import messagebox


class EditDetailsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    EditDetailsFrame shows the users their current details statically and creates a Toplevel to edit details.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.top = None
        self.details = self.get_details()

        tk.Label(self, text="My Personal Details", font=(None, 18))\
            .grid(row=0, column=0, columnspan=5, padx=(150, 0), pady=(30, 20))

        details_fields = ["First name", "Middle name", "Last name", "Sex", "DOB", "Mobile no"]
        for i in range(len(details_fields)):
            tk.Label(self, text=details_fields[i] + ": ", height=2) \
                .grid(row=i + 1, column=0, padx=(150, 0), sticky="W")

        tk.Label(self, text=self.details[1]).grid(row=1, column=1, columnspan=3, sticky="W")
        tk.Label(self, text=self.details[2]).grid(row=2, column=1, columnspan=3, sticky="W")
        tk.Label(self, text=self.details[3]).grid(row=3, column=1, columnspan=3, sticky="W")
        tk.Label(self, text=self.details[4]).grid(row=4, column=1, columnspan=3, sticky="W")
        tk.Label(self, text=str(self.details[5])[:10]).grid(row=5, column=1, columnspan=3, sticky="W")
        tk.Label(self, text=self.details[6]).grid(row=6, column=1, columnspan=3, sticky="W")

        # Initialise button to edit details
        btn_confirm = tk.Button(self, text="Edit Details", command=lambda: self.edit_details_toplevel())
        btn_confirm.grid(row=8, column=0, columnspan=2, padx=(150, 0), pady=(30, 20))

    def edit_details_toplevel(self):
        # Initialise top level
        if self.top is not None:
            self.top.destroy()

        self.top = tk.Toplevel()
        tk.Label(self.top, text="Edit your Personal Details", width=30, height=3, font=(None, 18)) \
            .grid(row=0, column=0, columnspan=5)

        edit_details_fields = ["First name", "Middle name", "Last name", "Sex", "DOB", "Mobile no"]
        for i in range(len(edit_details_fields)):
            tk.Label(self.top, text=edit_details_fields[i] + ": ", height=2) \
                .grid(row=i + 1, column=0, sticky="W")

        self.top.f_name_entry = tk.Entry(self.top)
        self.top.f_name_entry.insert(0, self.details[1])
        self.top.f_name_entry.grid(row=1, column=1, columnspan=3)

        self.top.m_name_entry = tk.Entry(self.top)
        self.top.m_name_entry.insert(0, self.details[2])
        self.top.m_name_entry.grid(row=2, column=1, columnspan=3)

        self.top.l_name_entry = tk.Entry(self.top)
        self.top.l_name_entry.insert(0, self.details[3])
        self.top.l_name_entry.grid(row=3, column=1, columnspan=3)

        sex = ["Sex", "Female", "Male"]
        self.top.sex_var = tk.StringVar(self.top)
        self.top.sex_var.set(self.details[4])
        self.top.sex_entry = tk.OptionMenu(self.top, self.top.sex_var, *sex)
        self.top.sex_entry.grid(row=4, column=1, columnspan=3, sticky="W")

        self.top.DOB_D_entry = tk.Entry(self.top, width=2)
        self.top.DOB_D_entry.insert(0, str(self.details[5])[8:10])
        self.top.DOB_D_entry.grid(row=5, column=1, sticky="W")
        self.top.DOB_M_entry = tk.Entry(self.top, width=2)
        self.top.DOB_M_entry.insert(0, str(self.details[5])[5:7])
        self.top.DOB_M_entry.grid(row=5, column=2, sticky="W")
        self.top.DOB_Y_entry = tk.Entry(self.top, width=4)
        self.top.DOB_Y_entry.insert(0, str(self.details[5])[:4])
        self.top.DOB_Y_entry.grid(row=5, column=3, sticky="W")

        self.top.MOB_entry = tk.Entry(self.top)
        self.top.MOB_entry.insert(0, self.details[6])
        self.top.MOB_entry.grid(row=6, column=1, columnspan=3)

        btn_save = tk.Button(self.top, text="Save Details", command=lambda: self.save_details(), height=2, width=10)
        btn_save.grid(row=7, column=0, columnspan=5)

    def get_details(self):
        try:
            # Query to find existing details
            query = "SELECT * FROM Patients WHERE username = ?"
            details = self.window.query(query, (self.window.email,))[0]
        except IndexError:
            messagebox.showinfo("Warning", "Your details couldn't be found in the database")
            logging.error("No user details returned from query")
        except Exception as e:
            messagebox.showinfo("Warning", "An error occurred whilst retrieving your details")
            logging.error(e)
        else:
            return details

    def save_details(self):
        try:
            int(self.top.MOB_entry.get())
            D = int(self.top.DOB_D_entry.get())
            M = int(self.top.DOB_M_entry.get())
            Y = int(self.top.DOB_Y_entry.get())
            DOB = datetime.datetime(year=Y, month=M, day=D)
        except ValueError:
            logging.info("non-numeric date input")
            messagebox.showinfo("Information", "Check number fields")
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Information", "Check number fields")
        else:
            if self.top.f_name_entry.get() == "" or self.top.l_name_entry.get() == "":
                messagebox.showinfo("Information", "You must not leave your name blank")
            elif len(self.top.MOB_entry.get()) != 11:
                messagebox.showinfo("Information", "Check your mobile number is correct")
            elif self.top.sex_var.get() == "Sex" or self.top.sex_var.get() is None:
                messagebox.showinfo("Information", "Please set your sex")
            else:
                query = "UPDATE Patients SET fName =?, mName =?, lName =?, sex =?, DOB =?, mobile =? WHERE username = ?"
                vals = (self.top.f_name_entry.get(), self.top.m_name_entry.get(), self.top.l_name_entry.get(),
                        self.top.sex_var.get(), DOB, self.top.MOB_entry.get(), self.window.email)
                self.window.query(query, vals)
                self.window.swap_view("Patient")
                self.top.destroy()
