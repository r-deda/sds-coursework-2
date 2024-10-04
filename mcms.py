from tkinter import *
from tkinter import ttk
from csv import *
from datetime import *
from time import *
from operations import *
import os
from hashlib import *


os.system("python3 patientGenerator.py")
os.system("python3 doctorGenerator.py")

csvFile = "doctorRecords.csv"
dummyRecord = [["Reinald", "Deda", "Male", "19", "01/10/2004", "rd123@hospital.com", "+44 07813765489"]]
with open(csvFile, "a", newline="") as file:
    file = writer(file)
    file.writerows(dummyRecord)

os.system("python3 appointmentGenerator.py")

del csvFile
del dummyRecord
del file

csvFile = "adminLogins.csv"
dummyRecords = [["rd123@hospital.com", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"], ["admin@hospital.com", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"]]
with open(csvFile, "w", newline="") as file:
    file = writer(file)
    file.writerows(dummyRecords)


usersName = []
appointmentDetails = []


'''
with open("requests.csv", "w", newline="") as file:
    data = writer(file)
'''

class roleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("500x500")
        
        self.label = Label(self.root, text="Select who you are:", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        self.r1 = Button(self.root, text="Administrator", width=10, command=self.admin, font=("Arial", 20))
        self.r1.pack()
        self.r2 = Button(self.root, text="Doctor", width=10, command=self.doctor, font=("Arial", 20))
        self.r2.pack()
        self.r3 = Button(self.root, text="Patient", width=10, command=self.patient, font=("Arial", 20))
        self.r3.pack()
    
    def admin(self):
        self.root.destroy()
        self.root1 = Tk()
        loginWindow(self.root1, "Admin")
        self.root1.mainloop()
        
    def doctor(self):
        self.root.destroy()
        self.root1 = Tk()
        loginWindow(self.root1, "Doctor")
        self.root1.mainloop()
        
    def patient(self):
        self.root.destroy()
        self.root1 = Tk()
        patientSelect(self.root1)
        self.root1.mainloop()

class loginWindow:
    def __init__(self, root, role):
        self.root = root
        self.root.title("")
        self.root.geometry("500x500")
        self.role = role
        
        self.label = Label(self.root, text="Please login:", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        self.userText = Label(self.root, text="Email:", font=("Arial", 20))
        self.userText.place(x=50, y=250)
        self.passText = Label(self.root, text="Password:", font=("Arial", 20))
        self.passText.place(x=50, y=300)
        self.userBox = ttk.Entry(font=("Arial", 20))
        self.userBox.place(x=175, y=250)
        self.passBox = ttk.Entry(font=("Arial", 20), show="•")
        self.passBox.place(x=175, y=300)
        
        self.login = Button(self.root, text="Login", width=10, command=self.checkLogin)
        self.login.place(x=175, y=350)
    
    def checkLogin(self):
        if self.role == "Doctor":
            self.csvFile = "doctorLogins.csv"
        elif self.role == "Admin":
            self.csvFile = "adminLogins.csv"
            
        with open(self.csvFile, "r", newline="") as file:
            self.data = reader(file)
            self.email = self.userBox.get().lower().strip()
            self.password = sha256(self.passBox.get().encode("utf-8")).hexdigest().strip()
            self.authenticated = False
            for row in file:
                self.details = row.split(",")
                if self.role == "Doctor":
                    self.details[0] = self.details[0].strip('"')
                    self.details[1] = self.details[1][1:len(self.details)-5]
                    
                if self.email == self.details[0].strip() and self.password == self.details[1].strip():
                    if self.role == "Doctor":
                            self.launchDoctor()
                            self.authenticated = True
                            break
                    elif self.role == "Admin":
                            self.launchAdmin()
                            self.authenticated = True
                            break
            
            if self.authenticated == False:
                credentialsIncorrect(self.root)
    
    def launchDoctor(self):
        self.root.destroy()
        self.root1 = Tk()
        doctorDashboard(self.root1, self.email)
        self.root1.mainloop()
        
    def launchAdmin(self):
        self.root.destroy()
        self.root1 = Tk()
        adminDashboard(self.root1, self.email)

class adminDashboard:
    def __init__(self, root, email):
        self.root = root
        self.email = email
                
        self.csvFile = "patientRecords.csv"
        with open(self.csvFile, "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row[5] == self.email:
                    self.adminName = [row[0], row[1]]
        
        self.nameText = Label(self.root, text=self.email, font=("Arial", 15))
        self.nameText.place(x=1200, y=103)        
        
        self.label = Label(self.root, text="Admin Dashboard", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        self.root.title("")
        self.root.attributes('-fullscreen',True)
        
        self.logOut = Button(self.root, text="<< Log Out", command=self.logOut)
        self.logOut.place(x=150, y=100)
        
        self.editDetails = Button(self.root, text="Edit Details", command=self.editAdminDetails)
        self.editDetails.place(x=350, y=100)
        
        self.writeReport = Button(self.root, text="Write Report", command=self.generateReport)
        self.writeReport.place(x=1000, y=100)
        
        self.patientLabel = Label(self.root, text="Patient Records:", font=("Arial", 25))
        self.patientLabel.place(x=25, y=200)
        self.appLabel = Label(self.root, text="Appointments:", font=("Arial", 25))
        self.appLabel.place(x=850, y=200)
        self.doctorLabel = Label(self.root, text="Doctor Records:", font=("Arial", 25))
        self.doctorLabel.place(x=25, y=650)
        
        self.allPatients = []
        with open("patientRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.allPatients.append(row)
                
        self.patientText = Label(self.root, text="Patient Name:", font=("Arial", 20))
        self.patientText.place(x=25, y=250)
        self.patientBox = ttk.Entry()
        self.patientBox.place(x=175, y=252)
        self.patientButton = Button(self.root, text="Show", command=self.searchPatients)
        self.patientButton.place(x=375, y=250)
        
        self.patientTable = ttk.Treeview(self.root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"), show="headings", height=15)
        self.patientTable.column("# 1", anchor=CENTER, width=80)
        self.patientTable.heading("# 1", text="Patient Forename")
        self.patientTable.column("# 2", anchor=CENTER, width=80)
        self.patientTable.heading("# 2", text="Patient Surname")
        self.patientTable.column("# 3", anchor=CENTER, width=80)
        self.patientTable.heading("# 3", text="Sex")
        self.patientTable.column("# 4", anchor=CENTER, width=80)
        self.patientTable.heading("# 4", text="Age")
        self.patientTable.column("# 5", anchor=CENTER, width=80)
        self.patientTable.heading("# 5", text="DOB")
        self.patientTable.column("# 6", anchor=CENTER, width=80)
        self.patientTable.heading("# 6", text="Address")
        self.patientTable.column("# 7", anchor=CENTER, width=80)
        self.patientTable.heading("# 7", text="Postcode")
        self.patientTable.column("# 8", anchor=CENTER, width=80)
        self.patientTable.heading("# 8", text="Email")
        self.patientTable.column("# 9", anchor=CENTER, width=80)
        self.patientTable.heading("# 9", text="Phone")
        self.patientTable.column("# 10", anchor=CENTER, width=80)
        self.patientTable.heading("# 10", text="Medical Problem:")
        
        self.groupButton = Button(self.root, text="Group By Family", command=self.groupFamily)
        self.groupButton.place(x=442, y=250)
        
        self.bookAppointment = Button(self.root, text="Book Appointment", command=self.selectDateForAppointment)
        self.bookAppointment.place(x=575, y=250)
        self.editPatient = Button(self.root, text="Edit Patient", command=self.displayPatientRecordWindow)
        self.editPatient.place(x=725, y=250)
        
        self.patientTable.place(x=25, y=300)
            
        self.allDoctors = []
        with open("doctorRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.allDoctors.append(row)
        
        self.doctorTable = ttk.Treeview(self.root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings", height=10)
        self.doctorTable.column("# 1", anchor=CENTER, width=114)
        self.doctorTable.heading("# 1", text="Doctor Forename")
        self.doctorTable.column("# 2", anchor=CENTER, width=114)
        self.doctorTable.heading("# 2", text="Doctor Surname")
        self.doctorTable.column("# 3", anchor=CENTER, width=114)
        self.doctorTable.heading("# 3", text="Sex")
        self.doctorTable.column("# 4", anchor=CENTER, width=114)
        self.doctorTable.heading("# 4", text="Age")
        self.doctorTable.column("# 5", anchor=CENTER, width=114)
        self.doctorTable.heading("# 5", text="DOB")
        self.doctorTable.column("# 6", anchor=CENTER, width=114)
        self.doctorTable.heading("# 6", text="Email")
        self.doctorTable.column("# 6", anchor=CENTER, width=114)
        self.doctorTable.column("# 7", anchor=CENTER, width=114)
        self.doctorTable.heading("# 7", text="Phone")
        
        self.newDoctor = Button(self.root, text="New Doctor", command=self.createDoctorWindow)
        self.newDoctor.place(x=490, y=660)
        self.adjustDoctor = Button(self.root, text="Edit Doctor", command=self.updateDoctorWindow)
        self.adjustDoctor.place(x=600, y=660)
        self.deleteDoctor = Button(self.root, text="Delete Doctor", command=self.deleteDoctor)
        self.deleteDoctor.place(x=705, y=660)
        
        for x in range(len(self.allDoctors)):
            self.doctorTable.insert("", "end", text=str(x+1), values=self.allDoctors[x])
        
        self.doctorTable.place(x=25, y=700)
    
        self.dateLabel = Label(self.root, text="Date:", font=("Arial", 20))
        self.dateLabel.place(x=850,y=250)
        
        self.dates = ["Any"]
        for x in range(0, 31):
            currentDate = date.today() + timedelta(days=x)
            currentDate = currentDate.strftime("%d/%m/%Y")
            self.dates.append(currentDate)
                
        self.date = StringVar()
        self.dateOption = ttk.Combobox(self.root, textvariable=self.date, values=self.dates, height=35, state="readonly", width=10)
        self.dateOption.place(x=925, y=254)
        
        self.select = Button(self.root, text="Show", command=self.viewUpcomingAppointments)
        self.select.place(x=1040, y=250)
        
        self.requestsButton = Button(self.root, text="Requests", command=self.viewRequestedPatients)
        self.requestsButton.place(x=1110, y=250)
        
        self.treatedPatients = Button(self.root, text="See Treated Patients", command=self.viewTreatedPatients, width=15)
        self.treatedPatients.place(x=1200, y=250)
        
        self.appTable = ttk.Treeview(self.root, column=("c1", "c2", "c3", "c4", "c5", "c6"), show="headings", height=32)
        self.appTable.column("# 1", anchor=CENTER, width=100)
        self.appTable.heading("# 1", text="Date")
        self.appTable.column("# 2", anchor=CENTER, width=100)
        self.appTable.heading("# 2", text="Patient Forename")
        self.appTable.column("# 3", anchor=CENTER, width=100)
        self.appTable.heading("# 3", text="Patient Surname")
        self.appTable.column("# 4", anchor=CENTER, width=100)
        self.appTable.heading("# 4", text="Time")
        self.appTable.column("# 5", anchor=CENTER, width=100)
        self.appTable.heading("# 5", text="Doctor Forename")
        self.appTable.column("# 6", anchor=CENTER, width=100)
        self.appTable.heading("# 6", text="Doctor Surname")
        
        self.allAppointments = displayAllApps()

        self.appTable.place(x=850, y=300)
        for x in range(len(self.allAppointments)):
            self.appTable.insert("", "end", text=str(x+1), values=self.allAppointments[x])
        
        for x in range(len(self.allPatients)):
            self.patientTable.insert("", "end", text=str(x+1), values=self.allPatients[x])
    
    def groupFamily(self):
        self.allAddresses = []
        with open("patientRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.allAddresses.append(row)
        
        self.orderedFamily = sorted(self.allAddresses, key=lambda record: (record[5], record[6], record[1]), reverse=True)

        for row in self.patientTable.get_children():
            self.patientTable.delete(row)
        
        for x in range(len(self.orderedFamily)):
            self.patientTable.insert("", "end", text=str(x+1), values=self.orderedFamily[x])
            
    def searchPatients(self):
        with open("patientRecords.csv", "r", newline="") as file:
                wholePatients = list(reader(file))
            
        for row in self.patientTable.get_children():
            self.patientTable.delete(row)
        
        for x in range(len(wholePatients)):
            self.patientTable.insert("", "end", text=str(x+1), values=wholePatients[x])
                
        self.searchedPatient = list(self.patientBox.get().split(" "))
        if self.searchedPatient != [""]:
            for x in range(len(self.searchedPatient)):
                for item in self.patientTable.get_children():                
                    itemValues = self.patientTable.item(item, "values")
                    if itemValues[0].startswith(self.searchedPatient[x]) == False and itemValues[1].startswith(self.searchedPatient[x]) == False:
                        self.patientTable.delete(item)
        
    def viewRequestedPatients(self):
        self.requestsButton.destroy()
        self.treatedPatients.destroy()
        
        self.allRequested = []
        with open("requests.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                currentDate = date.today() + timedelta(days=0) # generates the days the appointments will be on
                today = currentDate.strftime("%d/%m/%Y")
                today = strptime(today, "%d/%m/%Y")
                timeRow = row[0]
                timeRow = strptime(timeRow, "%d/%m/%Y")
                if timeRow >= today:
                    self.allRequested.append(row)
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
        
        for x in range(len(self.allRequested)):
            self.appTable.insert("", "end", text=str(x+1), values=self.allRequested[x])
    
        self.acceptButton = Button(self.root, text="✔", command=self.acceptRequestedAppointment)
        self.deleteButton = Button(self.root, text="✘", command=self.rejectRequestedAppointment)
        self.acceptButton.place(x=1110, y=250)
        self.deleteButton.place(x=1155, y=250)
        self.stopButton = Button(self.root, text="Stop", command=self.stopViewingRequests, width=24)
        self.stopButton.place(x=1200, y=250)
    
    def stopViewingRequests(self):
        self.requestsButton = Button(self.root, text="Requests", command=self.viewRequestedPatients)
        self.requestsButton.place(x=1110, y=250)
        
        self.treatedPatients = Button(self.root, text="See Treated Patients", command=self.viewTreatedPatients, width=15)
        self.treatedPatients.place(x=1200, y=250)
        
        self.acceptButton.destroy()
        self.deleteButton.destroy()
        self.stopButton.destroy()
        
        try:
            self.stopReviewing.destroy()
        except AttributeError:
            pass
        
    def acceptRequestedAppointment(self):
        item = self.appTable.selection()
        self.oldRequest = list(self.appTable.item(item, "values"))
        
        self.currentReqs = []
        with open("requests.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row != self.oldRequest:
                    self.currentReqs.append(row)

        with open("requests.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.currentReqs)
        
        self.currentApps = []
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.currentApps.append(row)
        
        self.currentApps.append(self.oldRequest)
        self.curentApps = sorted(self.currentApps, key=lambda item: datetime.strptime(f"{item[0]} {item[3]}", "%d/%m/%Y %H:%M"))
        
        self.appTable.delete(item)
        
        with open("appointments.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.currentApps)
            
    def rejectRequestedAppointment(self):
        item = self.appTable.selection()
        self.oldRequest = list(self.appTable.item(item, "values"))
        
        self.currentReqs = []
        with open("requests.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row != self.oldRequest:
                    self.currentReqs.append(row)

        with open("requests.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.currentReqs)
        
        self.appTable.delete(item)
        
    def editAdminDetails(self):
        self.root.destroy()
        self.root1 = Tk()
        settings(self.root1, self.email)
        self.root1.mainloop()
        
    def viewUpcomingAppointments(self):
        self.requestsButton = Button(self.root, text="Requests", command=self.viewRequestedPatients)
        self.requestsButton.place(x=1110, y=250)
        
        self.treatedPatients = Button(self.root, text="See Treated Patients", command=self.viewTreatedPatients, width=15)
        self.treatedPatients.place(x=1200, y=250)
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
        
        self.chosenDate = self.date.get()
        
        if self.chosenDate == "Any":
            self.allAppointments = displayAllApps()
        elif self.chosenDate != "Any":
            self.allAppointments = particularAppointments(self.chosenDate)

        for x in range(len(self.allAppointments)):
            self.appTable.insert("", "end", text=str(x+1), values=self.allAppointments[x])        
        
    def selectDateForAppointment(self):
        item = self.patientTable.selection()
        self.oldRecord = self.patientTable.item(item, "values")
        
        if self.oldRecord == "":
            selectPatient(self.root)
        else:
            self.root1 = Toplevel(self.root)
            self.root1.geometry("625x300")
            self.root1.transient(root)
            self.root1.grab_set()
            self.root1.title("")
            self.root1.update()
            
            self.label = Label(self.root1, text="Book appointment:", height=2)
            self.label.pack()
            
            self.label.config(font=("Arial", 40))
            self.root.title("")
            self.root.attributes('-fullscreen',True)
            
            self.dateLabel = Label(self.root1, text="Select appointment date:", font=("Arial", 20))
            self.dateLabel.place(x=25, y=150)
            
            self.dates = []
            for x in range(0, 31):
                currentDate = date.today() + timedelta(days=x)
                currentDate = currentDate.strftime("%d/%m/%Y")
                self.dates.append(currentDate)
                    
            self.appDate = StringVar()
            self.dateOption = ttk.Combobox(self.root1, textvariable=self.appDate, values=self.dates, height=20, width=10, state="readonly")
            self.dateOption.place(x=275, y=155)
            self.selectDate = ttk.Button(self.root1, text="Select date", command=self.selectTimeForAppointment, width=15)
            self.selectDate.place(x=425, y=152)
    
    def selectTimeForAppointment(self):
        self.chosenDate = self.appDate.get()
        appointmentDetails.append(self.chosenDate)
        self.availiable = findAppointments(self.chosenDate)
        
        self.times = []
        for x in range(len(self.availiable)):
            if self.availiable[x][0] not in self.times:
                self.times.append(self.availiable[x][0])
        
        self.timeLabel = Label(self.root1, text="Select time:", font=("Arial", 20))
        self.timeLabel.place(x=25, y=200)
        self.time = StringVar()
        self.timeOption = ttk.Combobox(self.root1, textvariable=self.time, values=self.times, width=10, state="readonly")
        self.timeOption.place(x=275, y=205)
        self.selectTime = ttk.Button(self.root1, text="Select time", command=self.selectDoctorForAppointment, width=15)
        self.selectTime.place(x=425, y=202)
    
    def selectDoctorForAppointment(self):
        self.chosenTime = self.time.get()
        appointmentDetails.append(self.chosenTime)
        self.doctors = []
        for x in range(len(self.availiable)):
            if self.availiable[x][0] == self.chosenTime:
                self.doctors.append(" ".join([self.availiable[x][1], self.availiable[x][2]]))
        
        self.doctorLabel = Label(self.root1, text="Select doctor:", font=("Arial", 20))
        self.doctorLabel.place(x=25, y=250)
        self.doctor = StringVar()
        self.chooseDoctor = ttk.Combobox(self.root1, textvariable=self.doctor, value=self.doctors, width=10, state="readonly")
        self.chooseDoctor.place(x=275, y=255)
        self.selectDoctor = ttk.Button(self.root1, text="Book appointment", width=15, command=self.bookingAppointmentValidity)
        self.selectDoctor.place(x=425, y=252)
    
    def bookingAppointmentValidity(self):
        item = self.patientTable.selection()
        patientsRecord = list(self.patientTable.item(item, "values"))
        
        self.forenameSelected = patientsRecord[0]
        self.surnameSelected = patientsRecord[1]
        
        valid = True
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                if self.chosenDate in row:
                    if self.appDate.get() in row:
                        if self.forenameSelected in row:
                            if self.surnameSelected in row:
                                alreadyBooked(self.root1)
                                valid = False
        
        if valid == True:
            self.writeBookedAppointment() 
    
    def writeBookedAppointment(self):
        self.recordToWrite = [self.appDate.get(), self.forenameSelected, self.surnameSelected, self.chosenTime, self.doctor.get().split(" ")[0], self.doctor.get().split(" ")[1]]
        with open("appointments.csv", "r", newline="") as file:
            self.newApps = list(reader(file))
        
        self.newApps.append(self.recordToWrite)
        self.newApps = sorted(self.newApps, key=lambda item: datetime.strptime(f"{item[0]} {item[3]}", "%d/%m/%Y %H:%M"))
        with open("appointments.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.newApps)
        
        self.root1.destroy()
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
    
        for x in range(len(self.newApps)):
            self.appTable.insert("", "end", text=str(x+1), values=self.newApps[x])
        
    def displayPatientRecordWindow(self):
        item = self.patientTable.selection()
        self.oldRecord = self.patientTable.item(item, "values")
        
        if self.oldRecord == "":
            selectPatient(self.root)
        else:
            self.root1 = Toplevel(self.root)
            self.root1.geometry("1400x150")
            self.root1.transient(root)
            self.root1.grab_set()
            self.root1.title("")
            self.root1.update()
            
            self.forenameText = Label(self.root1, text="*Forename:", font=("Arial", 20))
            self.forenameText.place(x=25, y=15)
            self.forenameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.forenameBox.place(x=25, y=50)
            self.forenameBox.insert(0, self.oldRecord[0])
            
            self.surnameText = Label(self.root1, text="*Surname:", font=("Arial", 20))
            self.surnameText.place(x=175, y=15)
            self.surnameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.surnameBox.place(x=175, y=50)
            self.surnameBox.insert(0, self.oldRecord[1])
            
            self.dobText = Label(self.root1, text="*DOB:", font=("Arial", 20))
            self.dobText.place(x=325, y=15)
            self.dobBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.dobBox.place(x=325, y=50)
            self.dobBox.insert(0, self.oldRecord[4])
            
            self.addressText = Label(self.root1, text="*Address:", font=("Arial", 20))
            self.addressText.place(x=475, y=15)
            self.addressBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.addressBox.place(x=475, y=50)
            self.addressBox.insert(0, self.oldRecord[5])
            
            self.postcodeText = Label(self.root1, text="*Postcode:", font=("Arial", 20))
            self.postcodeText.place(x=625, y=15)
            self.postcodeBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.postcodeBox.place(x=625, y=50)
            self.postcodeBox.insert(0, self.oldRecord[6])
            
            self.emailText = Label(self.root1, text="*Email:", font=("Arial", 20))
            self.emailText.place(x=775, y=15)
            self.emailBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.emailBox.place(x=775, y=50)
            self.emailBox.insert(0, self.oldRecord[7])
            
            self.phoneText = Label(self.root1, text="*Phone:", font=("Arial", 20))
            self.phoneText.place(x=925, y=15)
            self.phoneBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.phoneBox.place(x=925, y=50)
            self.phoneBox.insert(0, self.oldRecord[8])
            
            self.medicalBox = Label(self.root1, text="Medical:", font=("Arial", 20))
            self.medicalBox.place(x=1075, y=15)
            self.medicalBox = Text(self.root1, font=("Arial", 15), width=20)
            self.medicalBox.place(x=1075, y=50, height=85)
            self.medicalBox.insert(INSERT, self.oldRecord[9])
        
            self.editButton = Button(self.root1, text="Change", command=self.validateUpdatedPatient)
            self.editButton.place(x=1285, y=50)
    
    def validateUpdatedPatient(self):        
        validated = True
        self.usersDob = self.dobBox.get().split("/")
        
        if self.forenameBox.get() == "" or self.surnameBox.get() == "" or self.dobBox.get() == "" or self.addressBox.get() == "" or self.postcodeBox.get() == "" or self.emailBox.get() == "" or self.phoneBox.get() == "":
            emptyBoxes(self.root1)
            validated = False
            
        if len(self.usersDob) != 3 or int(self.usersDob[0]) < 1 or int(self.usersDob[0]) > 31 or int(self.usersDob[1]) < 1 or int(self.usersDob[1]) > 12 or int(self.usersDob[2]) < 1900 or int(self.usersDob[2]) > 2024:
            if validated == True:
                dobIncorrect(self.root1)
                validated = False
        
        if "@" not in self.emailBox.get():
            if validated == True:
                emailIncorrect(self.root1)
                validated = False
        
        if validated == True:    
            self.updatePatientRecord()
        
    def updatePatientRecord(self):
        if "+44" in self.phoneBox.get():
            self.phone = self.phoneBox.get()
        else:
            self.phone = "+44 " + self.phoneBox.get()
        
        self.usersDob = self.dobBox.get().split("/")
        self.usersAge = date.today().year - date(int(self.usersDob[2]), int(self.usersDob[1]), int(self.usersDob[0])).year
        self.newRecord = [self.forenameBox.get(), self.surnameBox.get(), self.oldRecord[2], self.usersAge, "/".join(self.usersDob), self.addressBox.get(), self.postcodeBox.get(), self.emailBox.get(), self.phone, self.medicalBox.get("1.0",'end-1c')]
        
        self.new = []
        self.old = []
        for x in range(len(self.newRecord)):
            self.new.append(self.newRecord[x])
            self.old.append(self.oldRecord[x])
        
        self.allPatients[self.allPatients.index(self.old)] = self.new
    
        csvFile = "patientRecords.csv"
        with open(csvFile, "w", newline="") as file:
            file = writer(file)
            file.writerows(self.allPatients)
        
        self.everyAppointment = []
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row[1] == self.oldRecord[0]:
                    if row[2] == self.oldRecord[1]:
                        row[1] = self.newRecord[0]
                        row[2] = self.newRecord[1]
                
                self.everyAppointment.append(row)
        
        with open("appointments.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.everyAppointment)
        
        self.everyRequest = []
        with open("requests.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row[1] == self.oldRecord[0]:
                    if row[2] == self.oldRecord[1]:
                        row[1] = self.newRecord[0]
                        row[2] = self.newRecord[1]
                
                self.everyRequest.append(row)
        
        with open("requests.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.everyRequest)
        
        for row in self.patientTable.get_children():
            self.patientTable.delete(row)
        
        for x in range(len(self.allPatients)):
            self.patientTable.insert("", "end", text=str(x+1), values=self.allPatients[x])
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
        
        for x in range(len(self.allAppointments)):
            self.appTable.insert("", "end", text=str(x+1), values=self.everyAppointment[x])
        
        
        self.root1.destroy()
    
    def generateReport(self):
        self.currentDoctors = []
        with open("doctorRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.currentDoctors.append([row[0], row[1]])
        
        self.totalDoctors = len(self.currentDoctors)
        
        self.everyAppointment = []
        self.currentAppointments = []
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.everyAppointment.append(row[4:6])
                if row[0] != ((date.today() + timedelta(days=-1)).strftime("%d/%m/%Y")):
                    self.currentAppointments.append(row[4:6])
        
        self.countAppointments = []
        for x in range(len(self.currentDoctors)):
            self.countAppointments.append(self.currentAppointments.count(self.currentDoctors[x]))
                
        self.totalConditions = []
        with open("patientRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.totalConditions.append(row[-1])
        
        self.conditions = list(set(self.totalConditions))
        
        self.conditionCount = []
        for x in range(len(self.conditions)):
            self.medicalCount = 0

            with open("patientRecords.csv", "r", newline="") as file:
                data = reader(file)
                self.medicalPatients = []
                for row in data:
                    if self.conditions[x] in row:
                        self.medicalPatients.append([row[0], row[1]])
            
            with open("appointments.csv", "r", newline="") as file:
                data = reader(file)
                self.appointmentPatients = []
                
                for row in data:
                    self.appointmentPatients.append(row)
            
            for y in range(len(self.medicalPatients)):
                for a in range(len(self.appointmentPatients)):
                    if self.medicalPatients[y][0] in self.appointmentPatients[a]:
                        if self.medicalPatients[y][1] in self.appointmentPatients[a]:
                            self.medicalCount = self.medicalCount + 1
                
            self.conditionCount.append(self.medicalCount)
        
        self.appointmentsTotal = []
        for x in range(len(self.currentDoctors)):
            self.appCounter = 0
            for y in range(len(self.currentAppointments)):
                if self.currentDoctors[x] == self.currentAppointments[y]:
                    self.appCounter = self.appCounter + 1
            
            self.appointmentsTotal.append(self.appCounter)
        
        self.patientNumbers = []
        for x in range(len(self.currentDoctors)):
            self.appCounter = 0
            for y in range(len(self.everyAppointment)):
                if self.currentDoctors[x] == self.everyAppointment[y]:
                    self.appCounter = self.appCounter + 1
            
            self.patientNumbers.append(self.appCounter)
        
        self.dateNow = datetime.now()
        self.dateNow = self.dateNow.strftime("%d-%m-%y_%H-%M-%S")
        self.txtFile = "Reports/report_%s" % self.dateNow
        with open(self.txtFile, "w") as file:
            self.todaysDate = datetime.now()
            self.todaysDate = self.todaysDate.strftime("%d/%m/%Y")
            self.nextMonth = date.today() + timedelta(days=31)
            self.nextMonth = self.nextMonth.strftime("%d/%m/%Y")
            file.write("Report for appointments from %s to %s" % (self.todaysDate, self.nextMonth))
            file.write("\nTotal Doctors - " + str(self.totalDoctors) + "\n\n")
            for x in range(len(self.conditions)):
                if self.conditions[x] == "" or self.conditions[x].isspace() == True:
                    file.write("Currently there are %s appointments with Patients that have no medical problems\n" % self.conditionCount[x])
                else:
                    file.write("Currently there are %s appointments with Patients that have the medical condition '%s'\n" % (self.conditionCount[x], self.conditions[x]))
        
            file.write("\n")
            for x in range(len(self.currentDoctors)):
                file.write("\nFor the next month Dr. %s has %s appointments" % (" ".join(self.currentDoctors[x]), self.appointmentsTotal[x]))
            
            file.write("\n")
            for x in range(len(self.currentDoctors)):
                file.write("\nCurrently Dr. %s has %s patients" % (" ".join(self.currentDoctors[x]), self.patientNumbers[x]))
            
            file.close()
    
    def createDoctorWindow(self):
        item = self.doctorTable.selection()
        self.oldRecord = self.doctorTable.item(item, "values")
        
        self.root1 = Toplevel(self.root)
        self.root1.geometry("1000x150")
        self.root1.transient(root)
        self.root1.grab_set()
        self.root1.title("")
        self.root1.update()
        
        self.forenameText = Label(self.root1, text="*Forename:", font=("Arial", 20))
        self.forenameText.place(x=25, y=15)
        self.forenameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
        self.forenameBox.place(x=25, y=50)
        
        self.surnameText = Label(self.root1, text="*Surname:", font=("Arial", 20))
        self.surnameText.place(x=175, y=15)
        self.surnameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
        self.surnameBox.place(x=175, y=50)
        
        self.gender = StringVar()
        self.genders = ["Male", "Female"]
        self.genderText = Label(self.root1, text="*Gender:", font=("Arial", 20))
        self.genderText.place(x=325, y=15)
        self.genderBox = ttk.Combobox(self.root1, textvariable=self.gender, values=self.genders, width=10, state="readonly")
        self.genderBox.place(x=325, y=52)
        
        self.dobText = Label(self.root1, text="*DOB:", font=("Arial", 20))
        self.dobText.place(x=475, y=15)
        self.dobBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
        self.dobBox.place(x=475, y=50)
        
        self.emailText = Label(self.root1, text="*Email:", font=("Arial", 20))
        self.emailText.place(x=625, y=15)
        self.emailBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
        self.emailBox.place(x=625, y=50)
        
        self.phoneText = Label(self.root1, text="*Phone:", font=("Arial", 20))
        self.phoneText.place(x=775, y=15)
        self.phoneBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
        self.phoneBox.place(x=775, y=50)
        
        self.addButton = Button(self.root1, text="Add", command=self.validateNewDoctor)
        self.addButton.place(x=910, y=48)
    
    def validateNewDoctor(self):
        validated = True
        self.doctorsDob = self.dobBox.get().split("/")
        
        if self.forenameBox.get() == "" or self.surnameBox.get() == "" or self.gender.get() == "" or self.dobBox.get() == "" or self.emailBox.get() == "" or self.phoneBox.get() == "":
            emptyBoxes(self.root1)
            validated = False
            
        if len(self.doctorsDob) != 3 or int(self.doctorsDob[0]) < 1 or int(self.doctorsDob[0]) > 31 or int(self.doctorsDob[1]) < 1 or int(self.doctorsDob[1]) > 12 or int(self.doctorsDob[2]) < 1900 or int(self.doctorsDob[2]) > 2024:
            if validated == True:
                dobIncorrect(self.root1)
                validated = False
        
        if "@" not in self.emailBox.get():
            if validated == True:
                emailIncorrect(self.root1)
                validated = False
        
        if validated == True:
            self.addNewDoctor()
    
    def addNewDoctor(self):
        self.doctorsDob = self.dobBox.get().split("/")
        self.doctorsAge = date.today().year - date(int(self.doctorsDob[2]), int(self.doctorsDob[1]), int(self.doctorsDob[0])).year
        
        if "+44" in self.phoneBox.get():
            self.phone = self.phoneBox.get()
        else:
            self.phone = "+44 " + self.phoneBox.get()
            
        self.newRecord = [self.forenameBox.get(), self.surnameBox.get(), self.gender.get(), self.doctorsAge, "/".join(self.doctorsDob), self.emailBox.get(), self.phone]
        
        self.allDoctors = []
        with open("doctorRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.allDoctors.append(row)
        
        self.allDoctors.append(self.newRecord)
        
        with open("doctorRecords.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.allDoctors)
        
        
        self.root1.destroy()
        
        for row in self.doctorTable.get_children():
            self.doctorTable.delete(row)
            
        for x in range(len(self.allDoctors)):
            self.doctorTable.insert("", "end", text=str(x+1), values=self.allDoctors[x])
        
    def updateDoctorWindow(self):
        item = self.doctorTable.selection()
        self.oldRecord = self.doctorTable.item(item, "values")
        
        if self.oldRecord == "":
            selectDoctor(self.root)
        else:   
            self.root1 = Toplevel(self.root)
            self.root1.geometry("850x150")
            self.root1.transient(root)
            self.root1.grab_set()
            self.root1.title("")
            self.root1.update()
            
            self.forenameText = Label(self.root1, text="*Forename:", font=("Arial", 20))
            self.forenameText.place(x=25, y=15)
            self.forenameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.forenameBox.place(x=25, y=50)
            self.forenameBox.insert(0, self.oldRecord[0])
            
            self.surnameText = Label(self.root1, text="*Surname:", font=("Arial", 20))
            self.surnameText.place(x=175, y=15)
            self.surnameBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.surnameBox.place(x=175, y=50)
            self.surnameBox.insert(0, self.oldRecord[1])
            
            self.dobText = Label(self.root1, text="*DOB:", font=("Arial", 20))
            self.dobText.place(x=325, y=15)
            self.dobBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.dobBox.place(x=325, y=50)
            self.dobBox.insert(0, self.oldRecord[4])
            
            self.emailText = Label(self.root1, text="*Email:", font=("Arial", 20))
            self.emailText.place(x=475, y=15)
            self.emailBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.emailBox.place(x=475, y=50)
            self.emailBox.insert(0, self.oldRecord[5])
            
            self.phoneText = Label(self.root1, text="*Phone:", font=("Arial", 20))
            self.phoneText.place(x=625, y=15)
            self.phoneBox = ttk.Entry(self.root1, font=("Arial", 15), width=10)
            self.phoneBox.place(x=625, y=50)
            self.phoneBox.insert(0, self.oldRecord[6])
            
            self.editButton = Button(self.root1, text="Change", command=self.validateUpdatedDoctor)
            self.editButton.place(x=750, y=48)
    
    def updateDoctorRecord(self):
        self.oldDoctors = []
        with open("doctorRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.oldDoctors.append(row)
        
        for x in range(len(self.oldDoctors)):
            if self.oldRecord[0] in self.oldDoctors[x]:
                if self.oldRecord[1] in self.oldDoctors[x]:
                    self.indexValue = x
        
        if "+44" in self.phoneBox.get():
            self.phone = self.phoneBox.get()
        else:
            self.phone = "+44 " + self.phoneBox.get()
        
        self.oldRecords = []
        self.doctorsDob = self.dobBox.get().split("/")
        self.doctorsAge = date.today().year - date(int(self.doctorsDob[2]), int(self.doctorsDob[1]), int(self.doctorsDob[0])).year
        self.newRecord = [self.forenameBox.get(), self.surnameBox.get(), self.oldRecord[2], self.doctorsAge, "/".join(self.doctorsDob), self.emailBox.get(), self.phoneBox.get()]
        self.newDoctors = self.oldDoctors
        self.newDoctors[self.indexValue] = self.newRecord
        
        with open("doctorRecords.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.newDoctors)
        
        self.root1.destroy()
        
        self.oldApps = []
        self.newApps = self.oldApps
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.oldApps.append(row)
        
        for x in range(len(self.oldApps)):
            if self.oldRecord[0] in self.oldApps[x] and self.oldRecord[1] in self.oldApps[x]:
                self.newApps[x][4] = self.newRecord[0]
                self.newApps[x][5] = self.newRecord[1]
        
        with open("appointments.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.newApps)
            
        for row in self.doctorTable.get_children():
            self.doctorTable.delete(row)
        
        for x in range(len(self.newDoctors)):
            self.doctorTable.insert("", "end", text=str(x+1), values=self.newDoctors[x])
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
        
        for x in range(len(self.newApps)):
            self.appTable.insert("", "end", text=str(x+1), values=self.newApps[x]) 
    
    def validateUpdatedDoctor(self):
        validated = True
        self.doctorsDob = self.dobBox.get().split("/")
        
        if self.forenameBox.get() == "" or self.surnameBox.get() == "" or self.dobBox.get() == "" or self.emailBox.get() == "" or self.phoneBox.get() == "":
            emptyBoxes(self.root1)
            validated = False
            
        if len(self.doctorsDob) != 3 or int(self.doctorsDob[0]) < 1 or int(self.doctorsDob[0]) > 31 or int(self.doctorsDob[1]) < 1 or int(self.doctorsDob[1]) > 12 or int(self.doctorsDob[2]) < 1900 or int(self.doctorsDob[2]) > 2024:
            if validated == True:
                dobIncorrect(self.root1)
                validated = False
        
        if "@" not in self.emailBox.get():
            if validated == True:
                emailIncorrect(self.root1)
                validated = False
        
        if validated == True:
            self.updateDoctorRecord()
            
    def deleteDoctor(self):
        item = self.doctorTable.selection()
        self.selectedDoctor = list(self.doctorTable.item(item, "values"))
        
        if self.selectedDoctor == "":
            selectDoctor(self.root)
        else:
            try:
                with open("appointments.csv", "r", newline="") as file:
                    data = reader(file)
                    self.hasApps = False
                    for row in data:
                        if self.selectedDoctor[0] in row and self.selectedDoctor[1] in row:
                            self.hasApps = True
                            break
                if self.hasApps == True:
                    self.doctorNotDeleted()
                
                else:
                    self.notSelected = []
                    with open("doctorRecords.csv", "r", newline="") as file:
                        data = reader(file)
                        for row in data:
                            if row != self.selectedDoctor:
                                self.notSelected.append(row)
                    
                    with open("doctorRecords.csv", "w", newline="") as file:
                        file = writer(file)
                        file.writerows(self.notSelected)
                    
                    for row in self.doctorTable.get_children():
                        self.doctorTable.delete(row)
                            
                    for x in range(len(self.notSelected)):
                        self.doctorTable.insert("", "end", text=str(x+1), values=self.notSelected[x])
            except IndexError:
                selectDoctor(self.root)
    
    def doctorNotDeleted(self):
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x250")
        self.root2.transient(self.root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.messageText = Label(self.root2, text="This doctor has\nappointments\nand can't be\ndeleted", font=("Arial", 25), height=6)
        self.messageText.pack()
        
        self.exitButton = Button(self.root2, text="Ok", command=self.exitDeleted)
        self.exitButton.pack()
    
    def exitDeleted(self):
        self.root2.destroy()
    
    def viewTreatedPatients(self):
        self.buttonText = "Discharge Patient"
        self.treatedPatients = Button(self.root, text=self.buttonText , command=self.dischargeTreatedPatient, width=15)
        self.treatedPatients.place(x=1200, y=250)
        
        self.stopReviewing = Button(self.root, text="Stop", command=self.stopDischarging, width=5)
        self.stopReviewing.place(x=1370, y=250)
        
        self.allTheDates = []
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.allTheDates.append(row[0])
        
        self.allTheDates = list(set(self.allTheDates))
        self.todaysDate = date.today()
        self.todaysDate = self.todaysDate.strftime("%d/%m/%Y")
        self.allTheDates = self.allTheDates[:self.allTheDates.index(self.todaysDate)]
        
        self.allPreviousAppointments = []
        for x in range(len(self.allTheDates)):
            self.previousAppointments = particularAppointments(self.allTheDates[x])
            for y in range(len(self.previousAppointments)):
                self.allPreviousAppointments.append(self.previousAppointments[y])
        
        for row in self.appTable.get_children():
            self.appTable.delete(row)
        
        for x in range(len(self.allPreviousAppointments)):
            self.appTable.insert("", "end", text=str(x+1), values=self.allPreviousAppointments[x])
    
    def dischargeTreatedPatient(self):
        item = self.appTable.selection()
        self.rowSelected = list(self.appTable.item(item, "values"))
        
        self.appTable.delete(item)
        
        self.patientName = self.rowSelected[1:3]
        
        self.treatedCounter = 0
        self.treatedIndex = 0
        self.yesterdayCounter = 0
        self.untreatedAppointments = []
        with open("appointments.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.untreatedAppointments.append(row)
                if self.patientName[0] == row[1]:
                    if self.patientName[1] == row[2]:
                        self.treatedIndex = self.treatedCounter
                
                self.treatedCounter = self.treatedCounter + 1
        del self.untreatedAppointments[self.treatedIndex]
    
        self.everyName = []
        self.everyPatient = []
        with open("patientRecords.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.everyName.append(row[0:2])
                self.everyPatient.append(row)
        
        with open("appointments.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.untreatedAppointments)
        
        self.patientIndex = self.everyName.index(self.patientName)
        del self.everyPatient[self.patientIndex]
        self.allPatients = self.everyPatient
        
        with open("patientRecords.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.allPatients)
                
        for row in self.patientTable.get_children():
            self.patientTable.delete(row)
        
        for x in range(len(self.allPatients)):
            self.patientTable.insert("", "end", text=str(x+1), values=self.allPatients[x])
    
    def stopDischarging(self):
        self.stopReviewing.destroy()
        
        self.buttonText = "See Treated Patient"
        self.treatedPatients = Button(self.root, text=self.buttonText , command=self.viewTreatedPatients, width=15)
        self.treatedPatients.place(x=1200, y=250)
    
    def logOut(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        resetDetails()
        self.root1.mainloop()
        
class doctorDashboard:
    def __init__(self, root, email):
        self.root = root
        self.email = email
        
        self.csvFile = "doctorRecords.csv"
        with open(self.csvFile, "r", newline="") as file:
            data = reader(file)
            for row in data:
                if row[5] == self.email:
                    self.doctorName = [row[0], row[1]]
        
        self.nameText = Label(self.root, text=("Welcome "+" ".join(self.doctorName)), font=("Arial", 15))
        self.nameText.place(x=1200, y=100)        
        
        self.label = Label(self.root, text="Appointments", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        self.root.title("")
        self.root.attributes('-fullscreen',True)
        
        self.logOut = Button(self.root, text="<< Log Out", command=self.logOut)
        self.logOut.place(x=150, y=100)
        
        self.allAppointments = displayAppointments(self.doctorName)
        self.allAppointments = self.allAppointments[:len(self.allAppointments)-2]
        
        self.table = ttk.Treeview(self.root, column=("c1", "c2", "c3", "c4"), show="headings", height=30)
        self.table.column("# 1", anchor=CENTER, width=250)
        self.table.heading("# 1", text="Date")
        self.table.column("# 2", anchor=CENTER, width=250)
        self.table.heading("# 2", text="Patient Forename")
        self.table.column("# 3", anchor=CENTER, width=250)
        self.table.heading("# 3", text="Patient Surname")
        self.table.column("# 4", anchor=CENTER, width=250)
        self.table.heading("# 4", text="Time")
        
        for x in range(len(self.allAppointments)):
            self.table.insert("", "end", text=str(x+1), values=self.allAppointments[x])
        
        self.table.pack()
        self.table.bind("<Double-1>", self.getRecord)
        
    def getRecord(self, event):
        item = self.table.selection()
        self.usersName = self.table.item(item, "values")
        
        self.csvFile = "patientRecords.csv"
        with open(self.csvFile, "r", newline="") as file:
            data = reader(file)
            for row in data:
                if self.usersName[1] == row[0]:
                    if self.usersName[2] == row[1]:
                        self.record = row
                        self.displayRecord()

    def displayRecord(self):
        self.root1 = Toplevel(self.root)
        self.root1.geometry("1300x100")
        self.root1.transient(root)
        self.root1.grab_set()
        self.root1.update()
        self.root1.title("")
        self.root1.attributes('-fullscreen',False)
        
        self.recordTable = ttk.Treeview(self.root1, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"), show="headings", height=2)
        self.headers = ["Name", "Surname", "Sex", "Age", "DOB", "Address", "Postcode", "Email", "Phone", "Medical condition"]
        
        for x in range(10):
            self.recordTable.column("#" + str(x), width=125)
            self.recordTable.heading(x, text=self.headers[x])
        
        self.recordTable.insert("", "end", text=str(x), values=self.record)
        self.recordTable.pack()
    
    def logOut(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        resetDetails()
        self.root1.mainloop()
        
class patientSelect:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.label = Label(self.root, text="Have you registered\nwith us?", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        self.root.title("")
        
        self.yes = Button(self.root, text="Yes, I have registered", font=("Arial", 20), command=self.launchExisting)
        self.yes.pack()
        self.no = Button(self.root, text="No, I am a new patient", font=("Arial", 20), command=self.launchRegister)
        self.no.pack()

    def launchExisting(self):
        self.root.destroy()
        self.root1 = Tk()
        existingPatient(self.root1)
        self.root1.mainloop()
        
    def launchRegister(self):
        self.root.destroy()
        self.root1 = Tk()
        patientRegister(self.root1)
        self.root1.mainloop()
        
class patientRegister:
    def __init__(self, root):
        self.root = root
        self.label = Label(self.root, text="Please register:", height=5)
        self.label.pack()
        
        self.label.config(font=("Arial", 40))
        self.root.title("")
        self.root.attributes('-fullscreen',True)
        
        self.back = Button(self.root, text="<< Back", command=self.goBack)
        self.back.place(x=125, y=100)
        
        self.forenameText = Label(self.root, text="*Forename:", font=("Arial", 20))
        self.forenameText.place(x=250, y=200)
        self.forenameBox = ttk.Entry(font=("Arial", 20), width=50)
        self.forenameBox.place(x=500, y=200)
        
        self.surnameText = Label(self.root, text="*Surname:", font=("Arial", 20))
        self.surnameText.place(x=250, y=250)
        self.surnameBox = ttk.Entry(font=("Arial", 20), width=50)
        self.surnameBox.place(x=500, y=250)
        
        self.gender = StringVar()
        self.genders = ["Male", "Female"]
        self.genderText = Label(self.root, text="*Gender:", font=("Arial", 20))
        self.genderText.place(x=250, y=325)
        self.genderBox = ttk.Combobox(self.root, textvariable=self.gender, values=self.genders, state="readonly")
        self.genderBox.place(x=500, y=325)
        
        self.dobText = Label(self.root, text="*DOB:", font=("Arial", 20))
        self.dobText.place(x=250, y=425)
        
        self.date = StringVar()
        self.dates = [str(x) for x in range(1, 32)]
        self.dateBox = ttk.Combobox(self.root, textvariable=self.date, values=self.dates, state="readonly")
        self.dateBox.place(x=500, y=425, width=100)
        self.dateText = Label(self.root, text="Date", font=("Arial", 20))
        self.dateText.place(x=525, y=375)
        self.dateButton = Button(self.root, text="Select date", command=self.addDob)
        self.dateButton.place(x=625, y=420)
        
        self.addressText = Label(self.root, text="*Address:", font=("Arial", 20))
        self.addressText.place(x=250, y=500)
        self.addressBox = ttk.Entry(font=("Arial", 20), width=50)
        self.addressBox.place(x=500, y=500)
        
        self.postcodeText = Label(self.root, text="*Postcode:", font=("Arial", 20))
        self.postcodeText.place(x=250, y=550)
        self.postcodeBox = ttk.Entry(font=("Arial", 20), width=50)
        self.postcodeBox.place(x=500, y=550)
        
        self.phoneText = Label(self.root, text="*Number:", font=("Arial", 20))
        self.phoneText.place(x=250, y=600)
        self.phoneBox = ttk.Entry(font=("Arial", 20), width=50)
        self.phoneBox.place(x=500, y=600)
        
        self.emailText = Label(self.root, text="*Email:", font=("Arial", 20))
        self.emailText.place(x=250, y=650)
        self.emailBox = ttk.Entry(font=("Arial", 20), width=50)
        self.emailBox.place(x=500, y=650)
            
        self.medicalText = Label(self.root, text="Medical Problems:", font=("Arial", 20))
        self.medicalText.place(x=250, y=725)
        self.medicalBox = Text(font=("Arial", 20), height=5, width=50)
        self.medicalBox.place(x=500, y=700)
        
        self.register = Button(self.root, text="Register", command=self.validateDetails)
        self.register.place(x=1250, y=750)
    
    def validateDetails(self):
        self.validDetails = True
        try:
            if self.forenameBox.get() == "" or self.surnameBox.get() == "" or self.gender.get() == "" or self.addressBox.get() == "" or self.postcodeBox.get() == "" or self.emailBox.get() == "" or self.phoneBox.get() == "":
                emptyBoxes(self.root)
                self.validDetails = False
            elif self.date == "" or self.month.get() == "" or self.year.get() == "":
                emptyBoxes(self.root)
                self.validDetails = False
            elif "@" not in self.emailBox.get():
                emailIncorrect(self.root)
                self.validDetails = False
        except ValueError:
            self.validDetails = False
            noDob(self.root)
        
        if self.validDetails == True:
            self.writeData()
    
    def addDob(self):
        self.date = int(self.date.get())
        self.dateBox.set(self.date)
        if self.date < 28:
            self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        elif self.date < 31:
            self.months = ["February", "April", "June", "September", "November"]
        else:
            self.months = ["January", "March", "May", "July", "August", "October", "December"]
        
        self.month = StringVar()
        self.monthBox = ttk.Combobox(self.root, textvariable=self.month, values=self.months, state="readonly")
        self.monthBox.place(x=625, y=425, width=100)
        self.monthText = Label(self.root, text="Month", font=("Arial", 20))
        self.monthText.place(x=640, y=375)
        
        self.year = StringVar()
        self.years = [str(x) for x in range(2024, 1900, -1)]
        self.yearBox = ttk.Combobox(self.root, textvariable=self.year, values=self.years, state="readonly")
        self.yearBox.place(x=750, y=425, width=100)
        self.yearText = Label(self.root, text="Year", font=("Arial", 20))
        self.yearText.place(x=775, y=375)
        del self.dateButton
        
    def writeData(self):
        usersName.append(self.forenameBox.get())
        usersName.append(self.surnameBox.get())
        
        self.y = self.year.get()
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.m = self.months.index(self.month.get()) + 1
        self.d = self.date
        self.age = date.today().year - date(int(self.y), int(self.m), int(self.d)).year
        
        if self.d < 10:
            self.d = "0" + str(self.m)
        else:
            self.d = str(self.d)
        
        if self.m < 10:
            self.m = "0" + str(self.m)
        else:
            self.m = str(self.m)
        
        if len(self.d) > 2:
            if self.d[2] == "0":
                self.d = self.d[0:2]
    
        self.dob = str("%s/%s/%s" % (self.d, self.m, self.y))
            
        self.record = [[self.forenameBox.get(), self.surnameBox.get(), self.gender.get(), self.age, self.dob, self.addressBox.get(), self.postcodeBox.get(), "+44 "+str(self.phoneBox.get()), self.emailBox.get(), self.medicalBox.get("1.0",'end-1c')]]
        self.csvFile = "patientRecords.csv"
        with open(self.csvFile, "a", newline="") as file:
            file = writer(file, quoting=QUOTE_ALL)
            file.writerows(self.record)
            
        self.next = Button(self.root, text="Next >>", command=self.nextWindow)
        self.next.place(x=1250, y=100)
        
    def goBack(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        self.root1.mainloop()
        
    def nextWindow(self):
        self.root.destroy()
        self.root1 = Tk()
        bookAppointment(self.root1)
        self.root1.mainloop()
        
class existingPatient:
    def __init__(self, root):
        self.root = root
        self.label = Label(self.root, text="Confirm your details:", height=5)
        self.label.pack()
        
        self.label.config(font=("Arial", 40))
        self.root.title("")
        self.root.attributes('-fullscreen',True)
        
        self.back = Button(self.root, text="<< Back", command=self.goBack)
        self.back.place(x=125, y=100)
        
        self.forenameText = Label(self.root, text="Forename:", font=("Arial", 20))
        self.forenameText.place(x=250, y=200)
        self.forenameBox = ttk.Entry(font=("Arial", 20), width=50)
        self.forenameBox.place(x=500, y=200)
        
        self.surnameText = Label(self.root, text="Surname:", font=("Arial", 20))
        self.surnameText.place(x=250, y=250)
        self.surnameBox = ttk.Entry(font=("Arial", 20), width=50)
        self.surnameBox.place(x=500, y=250)
        
        self.dobText = Label(self.root, text="DOB:", font=("Arial", 20))
        self.dobText.place(x=250, y=425)
        
        self.number = StringVar()
        self.dates = [str(x) for x in range(1, 32)]
        self.dateBox = ttk.Combobox(self.root, textvariable=self.number, values=self.dates, state="readonly")
        self.dateBox.place(x=500, y=425, width=100)
        self.dateText = Label(self.root, text="Date", font=("Arial", 20))
        self.dateText.place(x=525, y=375)
        self.dateButton = Button(self.root, text="Select date", command=self.addDob)
        self.dateButton.place(x=750, y=420)
    
    def addDob(self):
        self.date = int(self.number.get())
        self.dateBox.set(self.date)
        if self.date < 28:
            self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        elif self.date < 31:
            self.months = ["February", "April", "June", "September", "November"]
        else:
            self.months = ["January", "March", "May", "July", "August", "October", "December"]
        
        if self.date < 10:
            self.date = "0" + str(self.date)
        else:
            self.date = str(self.date)
            
        self.month = StringVar()
        self.monthBox = ttk.Combobox(self.root, textvariable=self.month, values=self.months, state="readonly")
        self.monthBox.place(x=750, y=425, width=100)
        self.monthText = Label(self.root, text="Month", font=("Arial", 20))
        self.monthText.place(x=765, y=375)
        
        self.year = StringVar()
        self.years = [str(x) for x in range(2024, 1900, -1)]
        self.yearBox = ttk.Combobox(self.root, textvariable=self.year, values=self.years, state="readonly")
        self.yearBox.place(x=1000, y=425, width=100)
        self.yearText = Label(self.root, text="Year", font=("Arial", 20))
        self.yearText.place(x=1025, y=375)
        
        self.next = Button(self.root, text="Next", command=self.validateDetails)
        self.next.place(x=1250, y=425)
        
    def goBack(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        self.root1.mainloop()
        
    def validateDetails(self):
        self.forename = self.forenameBox.get()
        self.surname = self.surnameBox.get()
        usersName.append(self.forename)
        usersName.append(self.surname)
        self.appointmentDetails = []
        
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.monthChosen = str(self.months.index(self.month.get()) + 1)
        
        if int(self.monthChosen) < 10:
            self.monthChosen = "0" + str(self.monthChosen)
        else:
            self.monthChosen = str(self.monthChosen)
            
        self.dob = self.date + "/" + self.monthChosen + "/" + str(self.year.get())
        
        self.valid = ""
        self.appointment = ""
        self.request = ""
        
        self.csvFile = "patientRecords.csv"
        with open(self.csvFile, "r", newline="") as file:
            data = reader(file)
            self.valid = False
            for row in data:
                if row[0] == self.forename:
                    if row[1] == self.surname:
                        if row[4] == self.dob:
                            self.valid = True
        
        if self.valid == True:
            self.appointment = False
            self.csvFile = "appointments.csv"
            with open(self.csvFile, "r", newline="") as file:
                data = reader(file)
                for row in data:
                    if row[1] == self.forename:
                        if row[2] == self.surname:
                            self.appointmentDetails.append(row)
                            self.appointment = True            
                            
        elif self.valid == False:
            self.detailsText = Label(self.root, text="Patient Details Incorrect")
            self.detailsText.place(x=575, y=625)
            self.detailsText.config(font=("Arial", 30))
            
            self.reset = Button(self.root, text="Reset", command=self.resetWindow)
            self.reset.place(x=250, y=725)
            
            self.register = Button(self.root, text="Register", command=self.launchRegister)
            self.register.place(x=1125, y=725)
        
        if self.appointment == False:
            self.request = False
            self.csvFile = "requests.csv"
            with open(self.csvFile, "r", newline="") as file:
                data = reader(file)
                for row in data:
                    if row[1] == self.forename:
                        if row[2] == self.surname:
                            self.appointmentDetails = row
                            self.request = True
                            
        elif self.appointment == True:
            self.root.destroy()
            self.root1 = Tk()
            confirmedAppointment(self.root1, self.appointmentDetails)
            self.root1.mainloop()
            
            resetDetails()
        
        if self.request == False:
            self.launchBooker()
            
        elif self.request == True:
            self.root.destroy()
            self.root1 = Tk()
            requestedAppointment(self.root1, self.appointmentDetails)
            self.root1.mainloop()
            resetDetails()        
                    
    def goRoleWindow(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        self.root1.mainloop()
    
    def launchBooker(self):
        self.root.destroy()
        self.root1 = Tk()
        bookAppointment(self.root1)
        self.root1.mainloop()
    
    def launchRegister(self):
        self.root.destroy()
        self.root1 = Tk()
        patientRegister(self.root1)
        self.root1.mainloop()
    
    def resetWindow(self):
        self.root.destroy()
        self.root1 = Tk()
        existingPatient(self.root1)
        self.root1.mainloop()

class bookAppointment:
    def __init__(self, root):
        self.root = root
        self.forename = usersName[0]
        self.surname = usersName[1]
        self.label = Label(self.root, text="Book appointment:", height=5)
        self.label.pack()
        
        self.label.config(font=("Arial", 40))
        self.root.title("")
        self.root.attributes('-fullscreen',True)
        
        self.dateLabel = Label(self.root, text="Choose your date:", font=("Arial", 20))
        self.dateLabel.place(x=300,y=300)
        
        self.dates = []
        for x in range(1, 32):
            currentDate = date.today() + timedelta(days=x)
            currentDate = currentDate.strftime("%d/%m/%Y")
            self.dates.append(currentDate)
                
        self.date = StringVar()
        self.dateOption = ttk.Combobox(self.root, textvariable=self.date, values=self.dates, height=20, width=10, state="readonly")
        self.dateOption.place(x=600, y=305)
        self.selectDate = ttk.Button(self.root, text="Select date", command=self.getDate, width=15)
        self.selectDate.place(x=900, y=300)
            
    def getDate(self):
        self.chosenDate = self.date.get()
        appointmentDetails.append(self.chosenDate)
        self.availiable = findAppointments(self.chosenDate)
        self.times = []
        for x in range(len(self.availiable)):
            if self.availiable[x][0] not in self.times:
                self.times.append(self.availiable[x][0])
        
        self.timeLabel = Label(self.root, text="Choose your time:", font=("Arial", 20))
        self.timeLabel.place(x=300, y=400)
        self.time = StringVar()
        self.timeOption = ttk.Combobox(self.root, textvariable=self.time, values=self.times, width=10, state="readonly")
        self.timeOption.place(x=600, y=405)
        self.selectTime = ttk.Button(self.root, text="Select time", command=self.getDoctor, width=15)
        self.selectTime.place(x=900, y=400)
    
    def getDoctor(self):
        self.chosenTime = self.time.get()
        appointmentDetails.append(self.chosenTime)
        self.doctors = []
        for x in range(len(self.availiable)):
            if self.availiable[x][0] == self.chosenTime:
                self.doctors.append(" ".join([self.availiable[x][1], self.availiable[x][2]]))
        
        self.doctorLabel = Label(self.root, text="Choose your doctor:", font=("Arial", 20))
        self.doctorLabel.place(x=300, y=500)
        self.doctor = StringVar()
        self.chooseDoctor = ttk.Combobox(self.root, textvariable=self.doctor, value=self.doctors, width=10, state="readonly")
        self.chooseDoctor.place(x=600, y=505)
        self.selectDoctor = Button(self.root, text="Book appointment", width=15, command=self.writeRecord)
        self.selectDoctor.place(x=900, y=500)
        
    def writeRecord(self):
        appointmentDetails.append((self.doctor.get()))
        self.record = [[self.date.get(), self.forename, self.surname, self.time.get(), self.doctor.get().split(" ")[0], self.doctor.get().split(" ")[1]]]
        requestAppointment(self.record)
        self.changeWindow()
        
    def changeWindow(self):
        self.root.destroy()
        self.root1 = Tk()
        requestedAppointment(self.root1, self.record)
        self.root1.mainloop()

class requestedAppointment:
    def __init__(self, root, appointmentDetails):
        self.root = root
        self.root.geometry("500x500")
        self.root.title("")

        
        self.label = Label(self.root, text="Appointment requested:", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        if len(appointmentDetails) == 1:
            appointmentDetails = appointmentDetails[0]
        
        self.string = "On %s at %s with Dr. %s %s" % (appointmentDetails[0], appointmentDetails[3], appointmentDetails[4], appointmentDetails[5])
        
        self.label2 = Label(self.root, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root, text="Ok", command=self.moveRoleWindow)
        self.button.place(x=235, y=300)
        
        resetDetails()
                
    def moveRoleWindow(self):
        self.root.destroy()
        self.root2 = Tk()
        roleWindow(self.root2)
        self.root2.mainloop()

class confirmedAppointment:
    def __init__(self, root, appointmentDetails):
        self.root = root
        self.root.geometry("500x500")
        self.root.title("")

        self.label = Label(self.root, text="Appointment confirmed:", height=5)
        self.label.pack()
        self.label.config(font=("Arial", 40))
        
        if len(appointmentDetails) == 1:
            appointmentDetails = appointmentDetails[0]
        
        self.string = "On %s at %s with Dr. %s %s" % (appointmentDetails[0], appointmentDetails[3], appointmentDetails[4], appointmentDetails[5])
        self.label2 = Label(self.root, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root, text="Ok", command=self.moveRoleWindow)
        self.button.place(x=235, y=300)
        
        resetDetails()
                
    def moveRoleWindow(self):
        self.root.destroy()
        self.root1 = Tk()
        roleWindow(self.root1)
        self.root1.mainloop()

class settings:
    def __init__(self, root, email):
        self.email = email
        self.root = root
        self.root.geometry("500x500")
        self.root.title("")
        
        self.userText1 = Label(self.root, text="*Current Email:", font=("Arial", 20))
        self.userText1.place(x=25, y=50)
        self.userBox1 = Entry(font=("Arial", 20))
        self.userBox1.place(x=210, y=50)    
    
        self.passText1 = Label(self.root, text="*Current Password:", font=("Arial", 20))
        self.passText1.place(x=25, y=100)
        self.passBox1 = ttk.Entry(font=("Arial", 20), show="•")
        self.passBox1.place(x=210, y=100)
        
        self.instructions = Label(self.root, text="Leave any box blank below if you\n don't want to change your details", font=("Arial", 20))
        self.instructions.place(x=90, y=190)
        
        self.userText2 = Label(self.root, text="New Email:", font=("Arial", 20))
        self.userText2.place(x=25, y=300)
        self.userBox2 = ttk.Entry(font=("Arial", 20))
        self.userBox2.place(x=210, y=300)
        
        self.passText2 = Label(self.root, text="New Password:", font=("Arial", 20))
        self.passText2.place(x=25, y=350)
        self.passBox2 = ttk.Entry(font=("Arial", 20), show="•")
        self.passBox2.place(x=210, y=350)

        self.changeDetails = Button(self.root, text="Change", command=self.validateLogins)
        self.changeDetails.place(x=215, y=425)
    
    def validateLogins(self):
        self.validated = True
        if self.userBox1.get() == "" and self.passBox1.get() == "":
            emptyBoxes(self.root)
            self.validated = False
        
        if self.validated == True:
            if "@" not in self.userBox1.get():
                emailIncorrect(self.root)
                self.validated = False
            elif "@" not in self.userBox2.get() and self.userBox2.get() != "":
                emailIncorrect(self.root)
                self.validated = False
        
        if self.validated == True:
            self.makeChanges()
        
    def makeChanges(self):
        self.details = []
        with open("adminLogins.csv", "r", newline="") as file:
            data = reader(file)
            for row in data:
                self.details.append(row)
        
        correctDetails = False
        self.detailsCounter = 0
        if self.userBox1.get() == self.email:
            for x in range(len(self.details)):
                if self.details[x][0] == self.userBox1.get():
                    if self.details[x][1] == sha256(self.passBox1.get().encode("utf-8")).hexdigest():
                        correctDetails = True
                        break
                
            self.detailsCounter = self.detailsCounter + 1
        
        if correctDetails == True:
            if self.userBox2.get() == "":
                self.details[self.detailsCounter][1] = sha256(self.passBox2.get().encode("utf-8")).hexdigest()
            elif self.passBox2.get() == "":
                self.details[self.detailsCounter][0] = self.userBox2.get()
            elif self.userBox2.get() != "" and self.userBox1.get() != "":
                self.details[self.detailsCounter][0] = self.userBox2.get()
                self.details[self.detailsCounter][1] = sha256(self.passBox2.get().encode("utf-8")).hexdigest()
        else:
            credentialsIncorrect(self.root)
            
        with open("adminLogins.csv", "w", newline="") as file:
            file = writer(file)
            file.writerows(self.details)
        
        self.email = self.userBox2.get()
        self.root.destroy()
        self.root1 = Tk()
        adminDashboard(self.root1, self.email)
        self.root1.mainloop()
        
def resetDetails():
    usersName = []
    appointmentDetails = []        
    
if __name__ == "__main__":
    root = Tk()
    roleWindow(root)
    root.mainloop()
        