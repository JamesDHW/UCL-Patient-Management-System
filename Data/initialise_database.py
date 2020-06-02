import sqlite3

connection = sqlite3.connect('Data/uch_care.db')
cursor = connection.cursor()

# === DELETE EXISTING TABLES ===
cursor.execute("DROP TABLE Auth")
cursor.execute("DROP TABLE Appointments")
cursor.execute("DROP TABLE Assignments")
cursor.execute("DROP TABLE Doctors")
cursor.execute("DROP TABLE Notes")
cursor.execute("DROP TABLE Patients")
cursor.execute("DROP TABLE Prescriptions")
cursor.execute("DROP TABLE Medicines")
connection.commit()

# === CREATE NEW TABLES ===
# APPOINTMENTS
cursor.execute("CREATE TABLE Appointments (doctor TEXT, datetime NUM, patient TEXT, appID TEXT, "
               "PRIMARY KEY(doctor, datetime))")
# DOCTOR-PATIENT ASSIGNMENTS (Temporary)
cursor.execute("CREATE TABLE Assignments (patient TEXT PRIMARY KEY, doctor TEXT)")
# AUTHENTIFICATION
cursor.execute("CREATE TABLE Auth (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
# DOCTOR DETAILS
cursor.execute("CREATE TABLE Doctors (username TEXT PRIMARY KEY, fName TEXT, lName TEXT, title TEXT, position TEXT)")
# PATIENT DETAILS
cursor.execute("CREATE TABLE Patients (username TEXT PRIMARY KEY, fName TEXT, mName TEXT,lName TEXT, sex TEXT, "
               "DOB TEXT, mobile TEXT, doctor TEXT)")
# PRESCRIPTION DETAILS
cursor.execute("CREATE TABLE Prescriptions (username TEXT, medicine TEXT, startDate TEXT, dose TEXT, frequency TEXT, "
               "duration TEXT, note TEXT, PRIMARY KEY(username, medicine, startDate))")
# PATIENT NOTES
cursor.execute("CREATE TABLE Notes (datetime TEXT, username TEXT, note TEXT, PRIMARY KEY(datetime, username))")
# AVAILABLE PRESCRIPTION MEDICINES
cursor.execute("CREATE TABLE Medicines (medicine TEXT PRIMARY KEY, treats TEXT)")
connection.commit()

# === TEST DATA ===
# USER AUTHENTIFICATION
cursor.execute("INSERT INTO Auth VALUES ('admin1@uch.org', "
               "'e33cea2baf42b373bd7be0d05d639731347e33270dce33c362bf3b7597f5d68af0bed09c969156465d88cd92ede7f5fd2ce29a609a09f5a8e82bcb067b7dc0b2', "
               "'Admin')")
cursor.execute("INSERT INTO Auth VALUES ('admin2@uch.org', "
               "'ba3cc0ac8652821c5b509c29c382653df25f78090ea083e1fbcbfff3e650fdb3281577f4ce41a59c0edc1c9691dccc298adee9d0c2c98f7e83d3a0f499844dc0', "
               "'Admin')")

cursor.execute("INSERT INTO Auth VALUES ('gp1@uch.org', "
               "'d2ce89725ce41a1caf9ba2e8d577e6d4d55c7978ff62af4b28bd54e97b61c31a68f5b37e6a0887969bbda43677a896b8eeb7f62f03e8c48a2d473fc11c1db8be', "
               "'Doctor')")
cursor.execute("INSERT INTO Auth VALUES ('gp2@uch.org', "
               "'1f5713b8a3f66a75680548b2607962a2055e1f71400e5a582e55dffb9db2940d2988acc29247e839206fb109f3e4cdd11c3192f7d052806f29742a685056ab9f', "
               "'Doctor')")

cursor.execute("INSERT INTO Auth VALUES ('patient1@gmail.com', "
               "'5978d1bbe696c6257b17139bda05030126485e52537a772b37d957082556a15f52cc3ea182362c41c2dd4205ade69cbbd255815bfa53b66bf1c391c9d467bcc3', "
               "'Patient')")
cursor.execute("INSERT INTO Auth VALUES ('patient2@gmail.com', "
               "'9bc521495b9597e6c53fe32bcb890c32e62a74144d744cd1c36c6c57e63ce0e11e5265f24237725f9a5a981ef3f8b2167ba87d57c6a49d946feeaea5153f0799', "
               "'Patient')")

# DOCTOR DETAILS DATA
cursor.execute("INSERT INTO Doctors VALUES('gp1@uch.org','John','Smith','Dr','GP')")
cursor.execute("INSERT INTO Doctors VALUES('gp2@uch.org','Jane','Bloggs','Dr','GP')")

# PATIENT DETAILS DATA
cursor.execute("INSERT INTO Patients VALUES ('patient1@gmail.com', 'David', 'Thomas', 'Lewis', 'Male', "
               "'1980-08-08', '07333454545', 'gp1@uch.org')")
cursor.execute("INSERT INTO Patients VALUES ('patient2@gmail.com', 'Sarah', 'Jane', 'Howarth', 'Female', "
               "'1990-09-09', '07888450450', 'gp1@uch.org')")

# PRESCRIPTION ENTRIES
cursor.execute("INSERT INTO Prescriptions VALUES('patient1@gmail.com', 'Penicillin', '2020-02-12', '30mg', '5 Day(s)', "
               "'10 Per Week', 'Taken with Lunch')")
cursor.execute("INSERT INTO Prescriptions VALUES('patient1@gmail.com', 'Aspirin', '2020-02-02', '20mg', '2 Week(s)', "
               "'2 Per Day', 'Taken in the Evening')")
cursor.execute("INSERT INTO Prescriptions VALUES('patient2@gmail.com', 'Ramipril', '2020-02-05', '40mg', '2 Day(s)', "
               "'5 Per Week', 'Taken with Water')")
cursor.execute("INSERT INTO Prescriptions VALUES('patient2@gmail.com', 'Aspirin', '2020-02-08', '10mg', '1 Month(s)', "
               "'20 Per Month', 'Taken with Breakfast')")

# PATIENT NOTES ENTRIES
cursor.execute("INSERT INTO Notes VALUES('2020-01-05 12:34','patient1@gmail.com', 'David had a fever')")
cursor.execute("INSERT INTO Notes VALUES('2020-01-10 12:34','patient1@gmail.com', 'Fever subsided')")
cursor.execute("INSERT INTO Notes VALUES('2020-01-01 12:34','patient2@gmail.com', 'Sarah has been fainting')")
cursor.execute("INSERT INTO Notes VALUES('2020-01-11 12:34','patient2@gmail.com', 'Low blood pressure reported')")

# EXAMPLE PRESCRIPTION MEDICINES
cursor.execute("INSERT INTO Medicines VALUES('Penicillin', 'Antibiotic')")
cursor.execute("INSERT INTO Medicines VALUES('Aspirin', 'Pain')")
cursor.execute("INSERT INTO Medicines VALUES('Atorvastatin', 'High Cholesterol')")
cursor.execute("INSERT INTO Medicines VALUES('Levothyroxine Sodium', 'Hypothyroidism')")
cursor.execute("INSERT INTO Medicines VALUES('Omeprazole', 'Acid Reflux')")
cursor.execute("INSERT INTO Medicines VALUES('Ramipril', 'High Blood Pressure')")
cursor.execute("INSERT INTO Medicines VALUES('Amlodipine', 'High Blood Pressure')")
cursor.execute("INSERT INTO Medicines VALUES('Simvastatin', 'High Cholesterol')")
cursor.execute("INSERT INTO Medicines VALUES('Lansoprazole', 'Acid Reflux')")
cursor.execute("INSERT INTO Medicines VALUES('Colecalciferol', 'Vitamin D Deficiency')")
cursor.execute("INSERT INTO Medicines VALUES('Bisoprolol Fumarate', 'High Blood Pressure')")

connection.commit()
connection.close()
