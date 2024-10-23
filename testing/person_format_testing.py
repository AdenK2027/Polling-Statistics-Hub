import os
from src.individual import Individual

def get_data(file_name):
    global question
    with open(file_name, 'rt') as fout:

        #all the lines of data read as a list of lines
        lines = fout.readlines()

        #data from app contains all polls so this is more or less just incase any previous
        #poll responses slip through the cracks

        question = lines[-1].split(',')[-2]
        i = len(lines)-2
        while '?' not in question:
            question = lines[i].split(',')[-2]
            i -= 1

        #list of individuals that will be returned
        individuals = []

        #base parties
        parties = ['republican', 'democrat']

        #for each response
        for line in lines:
            #splits the response by email, party, birthday, etc
            line = line.split(',')

            response = line[-1].strip('\n')
            email = 'example@gmail.com'
            birthdate = '00/00/0000'
            party = 'example party'
            affiliation = 'us example'
            gender = ''

            if line[-2] == question:
                #for characteristic in line
                for characteristic in line:
                    if line.index(characteristic) == len(line) - 2:
                        break
                    characteristic = characteristic.lower()
                    #for every part of each response
                    if '@' in characteristic:
                        email = characteristic
                    elif characteristic.count('/') > 1:
                        birthdate = characteristic
                    elif characteristic in parties:
                        party = characteristic
                    elif 'house' in characteristic or 'senate' in characteristic:
                        affiliation = characteristic
                    office = line[4].lower()
                    job_title = line[5].lower()
                    field = line[-4].lower()
                    if characteristic == 'f' or characteristic == 'm':
                        gender = characteristic
                #only runs if a response was found (only stops empty individuals)
                if response != '':
                    temp_individual = Individual(email=email,birthday=birthdate,party=party,affiliation=affiliation,
                                             office=office,title=job_title,gender=gender,field=field,
                                             response=response)
                    individuals.append(temp_individual)
    return individuals

file_path = os.path.join("files","complete_09_12_24_data.csv")

individuals = get_data(file_path)

for item in individuals:
    item.dump()