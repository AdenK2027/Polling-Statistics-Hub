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

        #fields
        fields = ['policy', 'administrative', 'communicators', 'administrative', 'other']

        #for each response
        i = 0
        for line in lines:
            #splits the response by email, party, birthday, etc
            line = line.split(',')
            if '\n' in line:
                line.remove('\n')

            response = line[-1].strip('\n')
            email = 'example@gmail.com'
            birthdate = '00/00/0000'
            party = ''
            affiliation = 'us example'
            gender = ''
            office = 'none'
            job_title = 'none'
            field = 'other'
            excess = []

            if line[-2] == question:
                #for characteristic in line
                for characteristic in line:
                    if line.index(characteristic) == len(line) - 2:
                        break
                    characteristic = characteristic.lower()
                    #for every part of each response
                    if '@' in characteristic:
                        email = characteristic
                        if email == "test9@gmail.com":
                            pass
                    elif characteristic.count('/') > 1:
                        birthdate = characteristic
                    elif characteristic in parties:
                        party = characteristic
                    elif 'house of representatives' in characteristic or 'senate' in characteristic:
                        affiliation = characteristic
                    elif characteristic == 'f' or characteristic == 'm':
                        gender = characteristic
                    else:
                        condition = False
                        for item in fields:
                            if item in characteristic:
                                t_char = characteristic.split()
                                if not t_char.index(item) < len(t_char)-1:
                                    field = characteristic
                                    condition = True
                                    break
                        if not condition:
                            excess.append(characteristic)
                #only runs if a response was found (only stops empty individuals)
                if response != '':
                    temp_individual = Individual(email=email,birthday=birthdate,party=party,affiliation=affiliation,
                                             office=office,title=job_title,gender=gender,field=field,
                                             response=response,excess=excess)
                    individuals.append(temp_individual)
    return individuals

file_path = os.path.join("files","Testing-Data.csv")

individuals = get_data(file_path)

for item in individuals:
    item.dump()
    print()