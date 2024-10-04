from faker import *
from csv import *
from random import *
from datetime import *
from tabulate import *

fake = Faker("en_GB")
addresses = []
postcodes = []

def generateMale(): # generates a random male adult patient
    forename = fake.first_name_male() # generates a random first name
    surname = fake.last_name() # generates a random last name
    
    sex = "Male"
    age = randint(18, 100) # generates it's age
    dob = fake.date_of_birth(tzinfo=None, minimum_age=age, maximum_age=age).strftime("%d/%m/%Y") # generates DOB
    
    address = fake.address().split(" ") # gives it a fake address
    address = " ".join(address[:len(address)-2]) # does generate a weird postcode, so I removed it from the address
    while address in addresses:
        address = fake.address().split(" ") # gives it a fake address
        address = " ".join(address[:len(address)-2]) # does generate a weird postcode, so I removed it from the address
    addresses.append(address)
    
    postcode = fake.postcode() # random postcode generated
    while postcode in postcodes:
        postcode = fake.postcode() # random postcode generated
    postcodes.append(postcode)
    
    email = str(forename[0]+"."+surname+"@email.com").lower() # random email generated
    number = generatePhone() # random phone number generated
    condition = generateCondition() # random condition
    
    record = [forename, surname, sex, age, dob, address, postcode, email, number, condition] # stores a record of the patient generated
    return record

def generateFemale(): # generates a random female adult patient
    forename = fake.first_name_female() # generates a random first name
    surname = fake.last_name() # generates a random last name
    sex = "Female"
    age = randint(18, 100) # generates it's age
    dob = fake.date_of_birth(tzinfo=None, minimum_age=age, maximum_age=age).strftime("%d/%m/%Y") # generates DOB
    
    address = fake.address().split(" ") # gives it a fake address
    address = " ".join(address[:len(address)-2]) # does generate a weird postcode, so I removed it from the address
    while address in addresses:
        address = fake.address().split(" ") # gives it a fake address
        address = " ".join(address[:len(address)-2]) # does generate a weird postcode, so I removed it from the address
    addresses.append(address)
    
    postcode = fake.postcode() # random postcode generated
    while postcode in postcodes:
        postcode = fake.postcode() # random postcode generated
    postcodes.append(postcode)
    
    email = str(forename[0]+"."+surname+"@email.com").lower() # random email generated
    number = generatePhone() # random phone number generated
    condition = generateCondition() # random condition
    
    record = [forename, surname, sex, age, dob, address, postcode, email, number, condition] # stores a record of the patient generated
    return record

def generatePartner(record1): # will generate a partner for the first patient generated, some of the personal details will be the same like the surname, email, address
    if "Male" in record1: # checks the sex of the first patient generated, if it's a male
        forename = fake.first_name_female()
        sex = "Female"
        age = randint(record1[3]-10, record1[3]) # assumed partners are around the same age
    if "Female" in record1: # checks the sex of the first patient generated, if it's a female
        forename = fake.first_name_male()
        sex = "Male"
        age = randint(record1[3], record1[3]+10) # assumed partners are around the same age
   
    surname = record1[1] # partner will have same surname
    dob = fake.date_of_birth(tzinfo=None, minimum_age=age, maximum_age=age).strftime("%d/%m/%Y") # generates DOB
    address = record1[5] # partner has the same address
    postcode = record1[6] # and same postcode
    email = str(forename[0]+"."+surname+"@email.com").lower() # random email generated
    number = generatePhone() # but different phone number
    condition = generateCondition() # generates random condition
    
    record2 = [forename, surname, sex, age, dob, address, postcode, email, number, condition] # record will store the data about the partner
    return record2

        
def generatePhone(): # phone number is generated
    number = ["+44 ", "0", "7"]
    for x in range(9):
        number.append(str(randint(1, 9)))
    number = "".join(number)
    return number

def generateCondition(): # random condition for the patient will be generated
    if randint(1, 4) == 1: # randomly selects whether or not a patient will have a medical condition, 1 of every 4 patients wil;
        condition = conditions[randint(0, len(conditions)-1)]
    else:
        condition = ""
    return condition

length = 0
conditions = ["Haemophilia", "Nut Allergy", "Dairy Allergy", "Tourettes", "Dyspraxia", "Autistic"] # random medical conditions
records = []


while length < 10000: # 10000 patients will be generated
    if randint(1, 2) == 1: # randomly chooses whether or not the patient will be a male of female
        record1 = generateMale() # generates a male
    else:
        record1 = generateFemale() # generates a female
    
    length = length + 1 # counter to check the size of the record
    records.append(record1)
    
    if randint(1, 3) == 1: # randomly selects to generate a family - 1 of every 3 patients will have a partner and family
        record2 = generatePartner(record1) # partner is generated
        length = length + 1 # size of record increased
        records.append(record2)
        
        if 25 < record1[3] < 50 and 25 < record2[3] < 50: # if the partners are between the ages of 25 and 50, then a child in the family is generated
            children = [] # stores the total number of children a family will have
            for x in range(1, randint(1, 4)): # this loop represents the number of children a family could have, between 1 child to 4 children
                if randint(1, 2) == 1: # randomly selects whether or not to make the child a male or female
                    forename = fake.first_name_male()
                    sex = "Male"
                else:
                    forename = fake.first_name_female()
                    sex = "Female"
                
                surname = record1[1] # inherits surname from the parent
                age = randint(1, record1[3]-20) # makes sure that the child is less than 20 years younger than the parent
                dob = fake.date_of_birth(tzinfo=None, minimum_age=age, maximum_age=age).strftime("%d/%m/%Y") # fake dob generated
                address = record1[5] # address inherited
                postcode = record1[6] # postcode inherted
                email = record1[7] # email inherited
                number = record1[8] # number inherited
                condition = generateCondition() # random condition might be generated
                    
                childRecord = [forename, surname, sex, age, dob, address, postcode, email, number, condition] # record for child stored in a list
                children.append(childRecord) # record for children added to the list
            
            length = length + len(children) # length counter incremented by the number of children generated by the algorithm
            
            for x in range(len(children)):
                records.append(children[x])

'''
header = ["Patient Forename", "Patient Surname", "Sex", "Age", "DOB", "Address", "Postcode", "Email", "Number", "Medical condition"]
print(tabulate(records, headers=header)) # tabulates the data about the patients
'''

csvFile = "patientRecords.csv"
with open(csvFile, "w", newline="") as file:
    file = writer(file, quoting=QUOTE_ALL)
    file.writerows(records)