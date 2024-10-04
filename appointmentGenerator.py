from csv import *
from random import *
from datetime import *
from time import *
from tabulate import *

def getPatients(): # returns list of patients
    patientNames = []
    with open("patientRecords.csv", "r", newline="") as file: # reads the record of patients
        data = reader(file)
        for row in data:
            fullName = [row[0], row[1]] 
            patientNames.append(fullName)
    return patientNames

def getDoctors(): # returns list of doctors
    doctorNames = []
    with open("doctorRecords.csv", "r", newline="") as file: # reads the record of doctors
        data = reader(file) 
        for row in data:
            fullName = [row[0], row[1]]
            doctorNames.append(fullName)
    return doctorNames
            
hoursOpen = 17 - 9 # hours the hospital is open for, I've said it's open from 9-5
minApp = hoursOpen * 2 # minimum Appointments for the day, given each appointment is half an hour long, should be double the hours the hopsital is open
maxApp = hoursOpen * 2 * len(getDoctors()) # maximum appointments per day, where the hospital is fully booked

appointments = [] # stores all the appointments

'''
The bottom bit of code generates random appointments between the patients and doctors. 
'''
currentPatients = getPatients() # gets the patients name and surname from the function, one patient can't have more than one appointment

for days in range(-1, 31): # represents the number of days that appointments will be generated for, currently set to the next 30 days, please adjust if you like.
    currentDate = date.today() + timedelta(days=days) # generates the days the appointments will be on
    currentDate = currentDate.strftime("%d/%m/%Y") # formatting the date
    for hours in range(9, 17): # represents the hours the hospital is open to, I've said it's open from 9-5, so appointments are generated from 9-5
        for minute in range(0, 2): # represents time intervals of the appointments, each appointment lasts for a quarter hour
            if minute == 0: # formatting the timestamp - if an appointment is on the hour, make the sure the time ends in "00"
                min = "00"
            else:
                min = "30"
            
            if hours < 10: # formatting the timestamp - if an appointment is before 10, make sure the time starts with a "0"
                hour = "09"
            else:
                hour = str(hours)
            
            time = hour + ":" + min # formats the time
            doctorRecords = getDoctors() # get the name of the doctors from the record
            for x in range(randint(7, len(doctorRecords))): # this loops represents the number of doctors that will be have appointments at a certain time
                doctor = doctorRecords[randint(0, len(doctorRecords)-1)] # randomly selects a doctor from the list
                del doctorRecords[doctorRecords.index(doctor)] # removes the doctor from the list of doctors as one doctor can't have two appointments at one time
                patient = currentPatients[randint(0, len(currentPatients)-1)] # randomly selects a patient from the list
                del currentPatients[currentPatients.index(patient)] # removes the patient from the list as one can't have more than one appointment
                appointment = [currentDate, patient[0], patient[1], time, doctor[0], doctor[1]] # creates a list storing a record of a scheduled appointment
                appointments.append(appointment) # add the list to the list of all appointmentns

appointments = sorted(appointments, key=lambda x: random())
appointments = appointments[:-100]
requests = appointments[-100:]
appointments = sorted(appointments, key=lambda item: datetime.strptime(f"{item[0]} {item[3]}", "%d/%m/%Y %H:%M"))
requests = sorted(requests, key=lambda item: datetime.strptime(f"{item[0]} {item[3]}", "%d/%m/%Y %H:%M"))

csvFile = "appointments.csv" # the file storing this information
with open(csvFile, "w", newline="") as file: 
    file = writer(file, quoting=QUOTE_ALL)
    file.writerows(appointments) # writes the information to the file

csvFile = "requests.csv"
with open(csvFile, "w", newline="") as file: 
    file = writer(file, quoting=QUOTE_ALL)
    file.writerows(requests) # writes the information to the file

'''
header = ["Date", "Patient First Name", "Patient Last Name",  "Time", "Doctor First Name", "Doctor Last Name"]
print(tabulate(appointments, headers=header)) # prints out the information into a table
'''