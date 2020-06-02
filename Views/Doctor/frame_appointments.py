import datetime
import logging
import tkinter as tk
from datetime import date
from tkinter import messagebox


class AppointmentsFrame(tk.Frame):
    """
    Inherits from tk.Frame.
    AppointmentsFrame allows Doctors to view all their appointments, add availability,
    and remove availabilities/ appointments.
    """

    def __init__(self, window, parent):
        tk.Frame.__init__(self, parent)
        self.window = window
        self.parent = parent
        self.top = None

        # Draw titles
        tk.Label(self, text="My Appointments", font=(None, 18)).grid(row=0, column=1, columnspan=5, pady=(30, 20))
        tk.Label(self, text="Availabilities", font=(None, 16)).grid(row=1, column=1, padx=(20, 0), pady=(30, 20))
        tk.Label(self, text="Scheduled Appointments", font=(None, 16)).grid(row=1, column=4, padx=(20, 0), pady=(30, 20))

        # Drop-down for date of availabilities
        availability_date = [date.today() + datetime.timedelta(days=i) for i in range(28)]
        availability_date.insert(0, "All")
        self.avail_var = tk.StringVar(self)
        self.avail_var.set(availability_date[0])
        self.avail_var.trace("w", self.reload_lb)
        op_men_avail = tk.OptionMenu(self, self.avail_var, *availability_date)
        op_men_avail.grid(row=2, column=1)

        # Drop-down for date of appointments
        appointment_date = [date.today() + datetime.timedelta(days=i) for i in range(28)]
        appointment_date.insert(0, "All")
        self.app_var = tk.StringVar(self)
        self.app_var.set(appointment_date[0])
        self.app_var.trace("w", self.reload_lb)
        op_men_app = tk.OptionMenu(self, self.app_var, *appointment_date)
        op_men_app.grid(row=2, column=4)

        # Initialise the Listboxes for appointments and availability
        self.reload_lb()

        # Initialise button to remove an availability
        btn_remove_avail = tk.Button(self, text="Remove Selected",
                                     command=lambda: self.remove_availability(
                                         self.lb_availabilities, self.availability_app_IDs))
        btn_remove_avail.grid(row=4, column=0, columnspan=2, pady=(30, 0))

        # Initialise button to add an availability
        btn_add_avail = tk.Button(self, text="Add Availability", command=lambda: self.add_availability_toplevel())
        btn_add_avail.grid(row=5, column=0, columnspan=2, pady=(30, 20))

        # Initialise button to cancel a selected appointment
        btn_remove_avail = tk.Button(self, text="Cancel Selected",
                                     command=lambda: self.remove_availability(
                                         self.lb_appointments, self.appointments_app_IDs))
        btn_remove_avail.grid(row=4, column=4, columnspan=2, pady=(30, 0))

        # Initialise button to view the patient details of that appointment
        btn_add_avail = tk.Button(self, text="View Patient",
                                  command=lambda: self.parent.details_toplevel(
                                      self.lb_appointments, self.appointments_app_IDs))
        btn_add_avail.grid(row=5, column=4, columnspan=2, pady=(30, 20))

    def add_availability_toplevel(self):
        """
        Creates a tkinter Toplevel to select a time and date for an appointment
        :return: Void.
        """
        self.top = tk.Toplevel()
        tk.Label(self.top, text="Add Appointment Availabilities", font=(None, 16))\
            .grid(row=0, column=0, columnspan=2, pady=(30, 20))

        # Date of availabilities
        tk.Label(self.top, text="Date of Availability : ").grid(row=1, column=0, sticky="E")
        availability_date = [date.today() + datetime.timedelta(days=i) for i in range(28)]
        date_var = tk.StringVar(self)
        date_var.set(availability_date[0])
        option_menu = tk.OptionMenu(self.top, date_var, *availability_date)
        option_menu.grid(row=1, column=1, columnspan=2, sticky="W")

        # Number of repeats of appointments to be made
        tk.Label(self.top, text="Repeat Availability Schedule for ").grid(row=2, column=0, sticky="E")
        tk.Label(self.top, text=" Day(s)").grid(row=2, column=2, sticky="W")
        repeats = [1, 2, 3, 4, 5, 6, 7]
        rep_var = tk.StringVar(self)
        rep_var.set(repeats[0])
        option_menu = tk.OptionMenu(self.top, rep_var, *repeats)
        option_menu.grid(row=2, column=1, sticky="W")

        # Length of appointments to be made
        tk.Label(self.top, text="Length of Appointments (mins) : ").grid(row=3, column=0, sticky="E")
        app_length = [5, 10, 15, 20]
        len_var = tk.StringVar(self)
        len_var.set(app_length[1])
        option_menu = tk.OptionMenu(self.top, len_var, *app_length)
        option_menu.grid(row=3, column=1, sticky="W")

        # Start hour of availabilities
        tk.Label(self.top, text="Available from : ").grid(row=4, column=0, sticky="E")
        availability_start_hour = [i for i in range(7, 24)]
        start_hour_var = tk.StringVar(self)
        start_hour_var.set(availability_start_hour[0])
        option_menu = tk.OptionMenu(self.top, start_hour_var, *availability_start_hour)
        option_menu.grid(row=4, column=1, sticky="W")

        # Start min of availabilities
        availability_start_min = [i for i in range(0, 56, 5)]
        start_min_var = tk.StringVar(self)
        start_min_var.set(availability_start_min[0])
        option_menu = tk.OptionMenu(self.top, start_min_var, *availability_start_min)
        option_menu.grid(row=4, column=2, sticky="W")

        # End hour of availabilities
        tk.Label(self.top, text="Until : ").grid(row=5, column=0, sticky="E")
        availability_end_hour = [i for i in range(7, 24)]
        end_hour_var = tk.StringVar(self)
        end_hour_var.set(availability_end_hour[0])
        option_menu = tk.OptionMenu(self.top, end_hour_var, *availability_end_hour)
        option_menu.grid(row=5, column=1, sticky="W")

        # End min of availabilities
        availability_end_min = [i for i in range(0, 56, 5)]
        end_min_var = tk.StringVar(self)
        end_min_var.set(availability_end_min[0])
        option_menu = tk.OptionMenu(self.top, end_min_var, *availability_end_min)
        option_menu.grid(row=5, column=2, sticky="W")

        # Initialise add appointment button
        btn_register = tk.Button(self.top, text="Save Availabilities",
                                 command=lambda: self.add_availability(len_var.get(), date_var.get(), rep_var.get(),
                                                                        start_hour_var.get(), start_min_var.get(),
                                                                        end_hour_var.get(), end_min_var.get()))
        btn_register.grid(row=6, column=0, columnspan=3, pady=(30, 20))

    def details_toplevel(self, patient):
        details, prescriptions = self.parent.get_details(patient)
        top = tk.Toplevel()

        tk.Label(top, text="Patient Details", font=(None, 18)).grid(row=0, column=0, columnspan=5, pady=(30, 20))

        patient_details_fields = ["First name", "Middle name", "Last name", "Sex", "DOB", "Mobile no"]
        for i in range(len(patient_details_fields)):
            tk.Label(top, text=patient_details_fields[i] + ": ", height=2).grid(row=i + 1, column=0, sticky="W")

        tk.Label(top, text=details[1]).grid(row=1, column=1, columnspan=3, sticky="W")
        tk.Label(top, text=details[2]).grid(row=2, column=1, columnspan=3, sticky="W")
        tk.Label(top, text=details[3]).grid(row=3, column=1, columnspan=3, sticky="W")
        tk.Label(top, text=details[4]).grid(row=4, column=1, columnspan=3, sticky="W")
        tk.Label(top, text=str(details[5])[:2]+'/'+str(details[5])[2:4]+'/'+str(details[5])[4:])\
            .grid(row=5, column=1, columnspan=3, sticky="W")
        tk.Label(top, text=details[6]).grid(row=6, column=1, columnspan=3, sticky="W")

    def reload_lb(self, *args):
        query = "SELECT * FROM Appointments WHERE doctor = ?"
        app_query_result = self.window.query(query, (self.window.email,))

        # Availabilities for the next 28 days
        self.lb_availabilities = tk.Listbox(self, width=30)
        sb_availabilities = tk.Scrollbar(self, orient="vertical", command=self.lb_availabilities.yview)
        self.lb_availabilities.configure(yscrollcommand=sb_availabilities.set)
        self.lb_availabilities.grid(row=3, column=1, padx=(20, 0))
        sb_availabilities.grid(row=3, column=2, padx=(0, 20), sticky="ns")

        # Appointments for the next 28 days
        self.lb_appointments = tk.Listbox(self, width=30)
        sb_appointments = tk.Scrollbar(self, orient="vertical", command=self.lb_appointments.yview)
        self.lb_appointments.configure(yscrollcommand=sb_appointments.set)
        self.lb_appointments.grid(row=3, column=4, padx=(20, 0))
        sb_appointments.grid(row=3, column=5, padx=(0, 20), sticky="ns")

        self.availability_app_IDs = []
        self.appointments_app_IDs = []
        for i in range(len(app_query_result)):
            patient = app_query_result[i][2]
            app_date = app_query_result[i][1]
            # Add to listbox if the appointment idea is different from the last 5 mins and it is in the future
            if (i == 0 or i > 0 and app_query_result[i][3] != app_query_result[i - 1][3]) \
                    and datetime.date(year=int(app_date[0:4]), month=int(app_date[5:7]), day=int(app_date[8:10])) \
                    >= datetime.date.today():

                if patient == "-" and (self.avail_var.get() == "All" or self.avail_var.get() == app_query_result[i][1][:10]):
                    self.availability_app_IDs.append(app_query_result[i][3])
                    appointment_time = app_query_result[i][1][11:16]
                    if self.avail_var.get() == "All":
                        appointment_time += "\t" + app_query_result[i][1][:11]
                    self.lb_availabilities.insert("end", appointment_time + " (not booked)")
                elif patient != "-" and (self.app_var.get() == "All" or self.app_var.get() == app_query_result[i][1][:10]):
                    self.appointments_app_IDs.append(app_query_result[i][3])
                    appointment_time = app_query_result[i][1][11:16]
                    if self.app_var.get() == "All":
                        appointment_time += "\t" + app_query_result[i][1][:11]
                    self.lb_appointments.insert("end", appointment_time + " (booked)")

    def add_availability(self, len_var, date, repeats, start_hour_var, start_min_var, end_hour_var, end_min_var):
        # Check that start hour is before end hour
        if int(start_hour_var) > int(end_hour_var) or (
                int(start_hour_var) == int(end_hour_var) and int(start_min_var > end_min_var)):
            messagebox.showinfo("Information", "Please ensure your start and end times are correct")
            logging.warning("End time before start time")
            return

        start_datetime = datetime.datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]),
                                           hour=int(start_hour_var), minute=int(start_min_var))
        end_datetime = datetime.datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]),
                                         hour=int(end_hour_var), minute=int(end_min_var))
        time_overstep = False
        for day in range(1,int(repeats)+1):
            skipped_time_slots = []
            while start_datetime < end_datetime and not time_overstep:
                exists = False
                # Loop through 5 minute increments for length of appointments
                for i in range(0, int(len_var), 5):
                    query = "SELECT * FROM Appointments WHERE doctor = ? AND datetime = ?"
                    check_time = start_datetime + datetime.timedelta(minutes=i)
                    if check_time >= end_datetime:
                        time_overstep = True
                        exists = True
                        break
                    result = self.window.query(query, (self.window.email, check_time))
                    if len(result) != 0:
                        # If already exists
                        exists = True
                        skipped_time_slots.append(result[0][1][11:16])
                        logging.warning("Appointment overlap")
                        # Increment time (to next free slot)
                        start_datetime += datetime.timedelta(minutes=i + 5)
                        break
                # If none exist in appointment range add full appointment
                if not exists:
                    appID = self.window.random_str()
                    for i in range(0, int(len_var), 5):
                        query = "INSERT INTO Appointments VALUES(?, ?, ?, ?)"
                        check_time = start_datetime + datetime.timedelta(minutes=i)
                        self.window.query(query, (self.window.email, check_time, "-", appID))
                else:
                    # If already exist continue before updating time
                    continue
                start_datetime += datetime.timedelta(minutes=int(len_var))
            # Repeat for next day if repeats specified
            start_datetime = datetime.datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]),
                                               hour=int(start_hour_var), minute=int(start_min_var)) \
                             + datetime.timedelta(days=day)

            end_datetime = datetime.datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]),
                                             hour=int(end_hour_var), minute=int(end_min_var)) \
                           + datetime.timedelta(days=day)

            # Let the user know about how many time slots were skipped
            if len(skipped_time_slots) != 0:
                msg = "Some overlaps were avoided at : "
                for time in skipped_time_slots:
                    msg += "\n" + time
                messagebox.showinfo("Information", msg)

        # Reload page to update
        messagebox.showinfo("Information", "Completed")
        self.window.swap_view("Doctor")

    def remove_availability(self, lb, appIDs):
        # Check that something is selected
        if lb.curselection() is not None and len(lb.curselection()) > 0:
            appID = appIDs[lb.curselection()[0]]

            query = "SELECT patient FROM Appointments WHERE appID = ?"
            result = self.window.query(query, (appID,))

            if len(result) > 0 and result[0][0] != "-":
                patient = result[0][0]
                content = "Dear Patient, \n\nUnfortunately an appointment booked with your GP has had to be canceled," \
                          " please select another appointment through UCH Care. \n\nKind regards, \nUCL Care Team."
                subject = "UCL Care Confirmation"
                if self.window.valid_email(patient):
                    logging.info("notifying " + patient + " of appointment cancellation")
                    self.window.send_email(patient, content, subject=subject)

            query = "DELETE FROM Appointments WHERE appID = ? "
            self.window.query(query, (appID,))
            logging.info("Deleted appointment: " + appID)
            self.window.swap_view("Doctor")
        else:
            logging.info("No appointment selected")
