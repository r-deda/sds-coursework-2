from faker import *
from csv import *
from random import *
from datetime import *
from tabulate import *
from hashlib import *

fake = Faker("en_GB")

logins = []

def generatePhone(): # function for generating random phone numbers
    number = ["+44 ", "0", "7"] # all patients will have new phone numbers
    for x in range(9): # generates the next numbers to be in the phone number
        number.append(str(randint(1, 9))) 
    number = "".join(number) # creates the number
    return number

def generateDoctor(): # generates random doctors
    if randint(1, 2) == 1: # randomly selects whether to generate a male of female
        forename = fake.first_name_male() # generates a random male name
        sex = "Male"
    else:
        forename = fake.first_name_female() # generates a random female name
        sex = "Female"
    
    surname = fake.last_name() # generates a random surname
    age = randint(25, 75) # randomly generates the age of the doctor, between 25 and 75
    dob = fake.date_of_birth(tzinfo=None, minimum_age=age, maximum_age=age).strftime("%d/%m/%Y") # using it's age, it will generate a random DOB
    email = str(forename[0]+"."+surname+"@hospital.com").lower() # generates a random email
    phone = generatePhone() # calls the function to generate a random phone number
    doctor = [forename, surname, sex, age, dob, email, phone] # list is created to store the record for the doctor
    password = str(forename[0]+surname).lower()
    hash = sha256(password.encode('utf-8')).hexdigest()
    logins.append([email, hash])
    return doctor 

doctors = [] # stores all the information about the doctors

while len(doctors) < 10: # will generate 20 doctors, you can change this
    doctors.append(generateDoctor())

'''
header = ["Doctor Forename", "Doctor Surname", "Sex", "Age", "DOB", "Email", "Number"] # tabulates this information
print(tabulate(doctors, headers=header)) 
'''

csvFile = "doctorRecords.csv"
with open(csvFile, "w", newline="") as file:
    file = writer(file, quoting=QUOTE_ALL)
    file.writerows(doctors)

csvFile = "doctorLogins.csv"
dummyRecord = ["rd123@hospital.com", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"]
logins.append(dummyRecord)
with open(csvFile, "w", newline="") as file:
    file = writer(file, quoting=QUOTE_ALL)
    file.writerows(logins)
    

