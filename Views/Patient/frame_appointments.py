import datetime
import logging
import tkinter as tk
from datetime import date
from tkinter import messagebox


class AppointmentsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    AppointmentsFrame class allows users to view, edit and create new appointments
    selected from their assigned doctor's availabilities.
    """
    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.top = None
        self.appointments = self.get_appointments()

        tk.Label(self, text="My Appointments", font=(None, 18))\
            .grid(row=0, column=0, columnspan=2, padx=(150, 0), pady=(30, 20))

        # All appointments Listbox
        lb_appointments = tk.Listbox(self)
        sb_appointments = tk.Scrollbar(self, orient="vertical", command=lb_appointments.yview)
        lb_appointments.configure(yscrollcommand=sb_appointments.set)
        lb_appointments.grid(row=1, column=0, columnspan=2, padx=(150, 0))
        sb_appointments.grid(row=1, column=2)

        # Add datetime for each appointment to Listbox
        for i in range(len(self.appointments)):
            lb_appointments.insert("end", self.appointments[i][0])

        # Initialise button to remove an appointment
        btn_remove_app = tk.Button(self, text="Remove Appointment",
                                   command=lambda: self.remove_appointment(lb_appointments))
        btn_remove_app.grid(row=2, column=0, columnspan=2, padx=(150, 0), pady=(30, 20))

        # Initialise button to add an appointment
        btn_add_app = tk.Button(self, text="Add Appointment", command=lambda: self.appointment_toplevel())
        btn_add_app.grid(row=3, column=0, columnspan=2, padx=(150, 0), pady=(0, 20))

    def appointment_toplevel(self):
        """
        Creates a tkinter Toplevel to select a date and time for an appointment from doctor's availabilities.
        :return: Void.
        """
        try:
            try:
                doc_selected_query = "SELECT doctor FROM Patients WHERE username = ?"
                doctor = self.window.query(doc_selected_query, (self.window.email,))[0][0]
                if doctor == "-":
                    # Doctor hasn't been selected by patient yet
                    messagebox.showinfo("Information", "Select your doctor to book an appointment")
                    logging.warning("No Doctor Assigned yet")
                    return
            except Exception as e:
                logging.error(e)
                return

            query = "SELECT datetime, appID FROM Appointments WHERE doctor = (SELECT doctor FROM Patients WHERE " \
                    "username = ?) AND patient = '-' "
            appointments = self.window.query(query, (self.window.email,))
        except Exception as e:
            logging.error(e)
        else:
            if len(appointments) == 0:
                messagebox.showinfo("Information", "No Appointments Available")
                logging.warning("No appointments found")
                return

            self.top = tk.Toplevel()
            tk.Label(self.top, text="Select an Appointment Slot", font=(None, 15)).grid(row=0, column=0)

            def reload_lb(*args):
                # All appointments available for that day
                lb_appointments = tk.Listbox(self.top, width=25)
                sb_appointments = tk.Scrollbar(self.top, orient="vertical", command=lb_appointments.yview)
                lb_appointments.configure(yscrollcommand=sb_appointments.set)
                lb_appointments.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
                sb_appointments.grid(row=2, column=2)

                # Variable to work out the length of the appointment to tell the user
                app_length = 5
                available_appointments = []
                for i in range(len(appointments)):
                    app_date = appointments[i][0]
                    # Don't add appointments of the same appointment ID (or past appointments)
                    if (app_var.get() == "All" or appointments[i][0][:10] == app_var.get())\
                        and datetime.date(year=int(app_date[0:4]), month=int(app_date[5:7]), day=int(app_date[8:10])) \
                        >= datetime.date.today():
                        # appointments[i][1] is the appointment ID (comparing to the app ID of the next 5 minutes)
                        if i == len(appointments) - 1 or i < len(appointments) - 1 and appointments[i][1] != appointments[i + 1][1]:
                            available_appointments.append(appointments[i])
                            # Don't show the date if already selected
                            if app_var.get() == "All":
                                appointment = appointments[i + 1 - app_length//5][0]
                            else:
                                appointment = appointments[i + 1 - app_length//5][0][10:]
                            lb_appointments.insert("end", appointment + " (" + str(app_length) + " mins)")
                            app_length = 5
                        else:
                            # Not the final 5 minutes of that appointment (increment and don't add the appointment to
                            # the Listbox until the total lime of the appointment is known)
                            app_length += 5

                # Initialise save appointment button
                btn_save = tk.Button(self.top, text="Save Appointment",
                                     command=lambda: self.add_appointment(lb_appointments, available_appointments))
                btn_save.grid(row=4, column=0, columnspan=2, pady=(30, 20))

            # Date of appointments
            appointment_date = [date.today() + datetime.timedelta(days=i) for i in range(28)]
            appointment_date.insert(0, "All")
            app_var = tk.StringVar(self.top)
            app_var.set(appointment_date[0])
            app_var.trace("w", reload_lb)
            op_men_app = tk.OptionMenu(self.top, app_var, *appointment_date)
            op_men_app.grid(row=1, column=0)

            # Initialise listbox and button
            reload_lb()

            self.top.winfo_toplevel().title("Make New Appointment")

    def get_appointments(self):
        query = "SELECT * FROM Appointments WHERE patient = ?"
        result = self.window.query(query, (self.window.email,))
        try:
            appointments = [[result[0][1], result[0][3]]]
        except IndexError:
            logging.info("No appointments")
            return []
        except Exception as e:
            logging.error(e)
        else:
            for i in range(len(result)):
                if i > 0 and result[i][3] != result[i - 1][3]:
                    appointments.append([result[i][1], result[i][3]])
            return appointments

    def add_appointment(self, lb, appointments):
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return

        new = appointments[lb.curselection()[0]][1]
        new_date = appointments[lb.curselection()[0]][0][:10]
        for i in range(len(self.appointments)):
            if new_date == self.appointments[i][0][:10]:
                messagebox.showinfo("Information", "You may only select one appointment per day")
                return

        query = "UPDATE Appointments SET patient = ? WHERE appID = ?"
        try:
            self.window.query(query, (self.window.email, new))
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Error", "Task couldn't be completed")
        else:
            self.window.swap_view("Patient")
            self.top.destroy()

    def remove_appointment(self, lb):
        # Check that something is selected
        if lb.curselection() is None or len(lb.curselection()) == 0:
            return
        appointment = self.appointments[lb.curselection()[0]][1]
        query = "UPDATE Appointments SET patient = '-' WHERE appID = ? "
        try:
            self.window.query(query, (appointment,))
        except Exception as e:
            logging.error(e)
            messagebox.showinfo("Error", "Task couldn't be completed")
        else:
            self.window.swap_view("Patient")
