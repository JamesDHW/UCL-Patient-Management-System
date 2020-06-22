UCH Care: Health Care Management Software
=========================================

https://youtu.be/V4CEpHWVvWY

<img src="https://github.com/JamesDHW/recordManagment/blob/master/img1.png" width="400">
<img src="https://github.com/JamesDHW/recordManagment/blob/master/img2.png" width="400">
<img src="https://github.com/JamesDHW/recordManagment/blob/master/img3.png" width="400">

Requirements
------------

Admins:
 * Add new GP accounts.
 * Deactivate or remove GP accounts.
 * Confirm registration of patients.
 * Manage patients' records.

GPs:
 * Add their availability.
 * Confirm appointments made by patients.
 * Input prescriptions.

Patients:
 * Register their details.
 * Book and cancel appointments.


Project Structure
-----------------

The project can be run from '\_\_main__.py', which creates an instance of the Window class, which inherits from the 'Tk'
class in the tkinter module. This is a controller class, containing static methods which are used throughout the 
application. Window also contains a 'swap_view' method, which child classes can call to swap the view of the window. 

There are four main views: Login (where there is no user assigned); Admin (where an admin user is logged in); Doctor 
(where a GP is logged in); and Patient (where a patient is logged in). When 'swap_view' is called, a '<view>Controller' 
object from the 'window_<view>.py' module is packed into the window. This contains static methods which relate solely to 
the functionalities required to be performed within that view. This class inherits from the tkinter Frame class and, 
upon initialisation, creates a tkinter notebook (tabbed activity), with each tab of the notebook containing a different 
functionality of the application.


Storing Persistent Data
-----------------------

The built-in sqlite3 module was used to store data locally in a '.db' file. This was implemented by creating a static 
method in the Window class, which interprets SQL queries required from anywhere within the program, returning the result. 
As sqlite3 is a local database module, this doesn't allow for data consistency between computers, however it does allow 
SQL queries to be evaluated throughout the application. In the future, this method can be replaced with one that interacts 
with a MySQL database, introducing data consistency to the software whilst only requiring a small change to the program 
as a whole.


Setting Doctor Availabilities
----------------------------

Availabilities are split into 5 minute segments in the database (with the GP username and time slot as primary key). 
A single appointment ID is assigned to each appointment (so a 15 minute appointment is three 5 minute slots with the 
same appointment ID). When setting an availability the application starts at the given time and iterates forwards in 5 
minute increments for the number of slots needed for one appointment and after checking that the entire appointment 
length is free it assigns the slots to the appointment. This ensures that there are no overlaps in appointments. If a 
time slot is not available, the application checks the next slot and repeats the process, minimising the number of gaps 
between availabilities. If the application can't fit an appointment before the end of the allotted time span, the availability 
is not set, so that the doctor doesn't overrun on their schedule (GPs can add a shorter appointment at the end of that 
period, e.g. if they have been doing 15 minute appointments and have 10 minutes at the end of their day which a 15 minute 
appointment wouldn't have fit into, they can book another 10 minute availability at the end of their day).
