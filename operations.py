from csv import *
from tabulate import *
from datetime import *
from time import *
from tkinter import *
from tkinter import ttk
from hashlib import *
from mcms import *

class findAppointments:    
    def __new__(self, date):
        self.date = date
        
        self.times = []
        for x in range(9, 17): 
            for y in range(0, 2): 
                if y == 0: 
                    min = "00"
                else:
                    min = "30"
                
                if x < 10: 
                    hour = "09"
                elif x > 9:
                    hour = str(x)
                
                time = hour + ":" + min 
                self.times.append(time)
        
        self.appointments = []
        with open("appointments.csv", "r", newline="") as file: 
            data = reader(file) 
            for row in data:
                if self.date in row:
                    self.doctors = " ".join([row[4], row[5]])
                    self.appointments.append([row[3], self.doctors])
        
        self.requests = []
        with open("requests.csv", "r", newline="") as file: 
            data = reader(file) 
            for row in data:
                if self.date in row:
                    self.doctors = " ".join([row[4], row[5]])
                    self.appointments.append([row[3], self.doctors])
        
        self.appointments = self.appointments + self.requests
        
        self.doctors = []
        with open("doctorRecords.csv", "r", newline="") as file: 
            data = reader(file) 
            for row in data:
                self.doctors.append(" ".join([row[0], row[1]]))
        
        self.availiable = []
        for x in range(len(self.times)):
            self.occupied = []
            for y in range(len(self.appointments)):
                if self.times[x] == self.appointments[y][0]:
                    self.occupied.append(self.appointments[y][1])
            for y in range(len(self.doctors)):
                if self.doctors[y] not in self.occupied:
                    self.doctorName = self.doctors[y].split(" ")
                    self.availiable.append([self.times[x], self.doctorName[0], self.doctorName[1]])
            
        """
        self.header = ["Time", "Doctor Forename", "Doctor Second Name"]
        print(tabulate(self.availiable, headers=self.header)) # tabulates the data about the patients
        """
        
        return self.availiable

class requestAppointment:
    def __new__(self, record):
        with open("requests.csv", "a", newline="") as file:
            file = writer(file, quoting=QUOTE_ALL)
            file.writerows(record)

class confirmAppointment:
    def __new__(self, record):
        with open("appointments.csv", "a", newline="") as file:
            file = writer(file, quoting=QUOTE_ALL)
            file.writerows(record)
            
class displayAppointments:
    def __new__(self, doctorName):
        self.doctorName = doctorName
        csvFile = "appointments.csv"
        with open(csvFile, "r", newline="") as file:
            data = reader(file)
            self.allAppointments = []
            for row in data:
                if row[4] == self.doctorName[0]:
                    if row[5] == self.doctorName[1]:
                        self.yesterday = date.today() - timedelta(days=1)
                        self.yesterday = self.yesterday.strftime("%d/%m/%Y")
                        if row[0] != self.yesterday:
                            if row[0] == date.today().strftime("%d/%m/%Y"):
                                self.currentTime = datetime.now().strftime("%H:%M")
                                if row[3] > self.currentTime:
                                    self.valid = True
                                elif row[3] < self.currentTime:
                                    self.valid = False
                            else:
                                self.valid = True
                        else:
                            self.valid = False
                    else:
                        self.valid = False
                else:
                    self.valid = False
                
                if self.valid == True:
                    self.allAppointments.append(row)
        
        return self.allAppointments

class displayAllApps:
    def __new__(self):
        csvFile = "appointments.csv"
        
        self.today = date.today() + timedelta(days=0)
        self.today = self.today.strftime("%d/%m/%Y")
        self.today = strptime(self.today, "%d/%m/%Y")
        
        with open(csvFile, "r", newline="") as file:
            data = reader(file)
            self.allAppointments = []
            for row in data:
                dateRow = row[0]
                dateRow = strptime(dateRow, "%d/%m/%Y")
                if dateRow >= self.today:
                    self.allAppointments.append(row)        

        return self.allAppointments

class particularAppointments:
    def __new__(self, chosenDate):
        self.chosenDate = chosenDate
        csvFile = "appointments.csv"
        
        with open(csvFile, "r", newline="") as file:
            data = reader(file)
            self.allAppointments = []
            for row in data:
                if row[0] == self.chosenDate:
                    self.allAppointments.append(row)        

        return self.allAppointments

class credentialsIncorrect:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
        self.label = Label(self.root2, text="Incorrect Login Details:", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Incorrect details.\nPlease try again." 
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()

class emailIncorrect:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
                
        self.label = Label(self.root2, text="Email is in incorrect format:", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Email in wrong format.\nPlease re-enter."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()

class dobIncorrect:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("300x250")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
        
        self.label = Label(self.root2, text="DOB entered incorrectly", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "DOB entered incorrectly.\n Use format DD/MM/YYYY when entering.\nBirth year must be at least 2024.\nMonth must be between '1' and '12'.\nBirthmonth must be between '1' and '31'."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
        
        
    def changeWindow(self):
        self.root2.destroy()

class noDob:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
        
        self.label = Label(self.root2, text="Please add your DOB", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "You haven't added your DOB.\nPlease add this."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
        
    def changeWindow(self):
        self.root2.destroy()

class emptyBoxes:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
                
        self.label = Label(self.root2, text="Important Boxes Empty:", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Please fill in all boxes asterisked"
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()
        
class alreadyBooked:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
                
        self.label = Label(self.root2, text="Patient already booked in:", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Patient already booked in at this time.\nSelect a different time."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()

class selectPatient:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
                
        self.label = Label(self.root2, text="Please select a patient", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Patient not selected.\nPlease click on a patient in the table."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()

class selectDoctor:
    def __init__(self, root):
        self.root = root
        self.root2 = Toplevel(self.root)
        self.root2.geometry("250x125")
        self.root2.transient(root)
        self.root2.grab_set()
        self.root2.title("")
        self.root2.update()
        
        self.root.attributes('-topmost',True)
                
        self.label = Label(self.root2, text="Please select a doctor", height=2)
        self.label.pack()
        self.label.config(font=("Arial", 20))
        
        self.string = "Doctor not selected.\nPlease click on a doctor in the table."
        self.label2 = Label(self.root2, text=self.string)
        self.label2.pack()
        
        self.button = Button(self.root2, text="Ok", command=self.changeWindow)
        self.button.pack()
                
    def changeWindow(self):
        self.root2.destroy()