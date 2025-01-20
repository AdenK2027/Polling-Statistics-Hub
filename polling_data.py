import time
import datetime
from individual import Individual
#takes csv data from polls and reads it as individuals with characteristics seen in Individual.py
question = ''
def get_question():
    return question

def getDate(file_name):
    # creates a blank date that grabs only numbers and seperators from the filename
    date = ''  #
    for i in range(len(file_name)):
        char = file_name[i]
        try:  #
            if char != '-' and char != '_':  #
                date += str(int(char))  #
            else:  #
                date += '-'  #
        except:  #
            if char == 't':
                if file_name[i + 1] == 'o':
                    date += '-'
            continue  #
    ###############################################################################
    if file_name == 'Downloads/raw_pulse_data/Pulse Data 4_4 - 4_9 - Sports Betting - Thursday.csv':
        pass
    listDate = []
    for i in range(len(date)): #for every character in the date
        char = date[i]
        if char == '-': #if the character is a sep.
            if len(listDate) > 0: #if there is content in the date (doesn't start with a sep.)
                if listDate[-1] != '-': #if the last item wasn't also a sep.
                    listDate.append(char) #adds the seperator
        else: #if the character was a number
            listDate.append(char) #adds the number
    if listDate[-1] == '-':
        listDate.pop()
    date = ''.join(listDate)
    date = date.split('-')

    dateDict = {'month':-1, 'year':-1}

    if len(date) == 3:
        dateDict['month'] = date[0]
        dateDict['year'] = date[2]
    elif len(date) == 4:
        if date[0] == date[2]:
            dateDict['month'] = date[0]
            seconds_since_epoch = time.time()
            datetime_object = datetime.datetime.fromtimestamp(seconds_since_epoch)
            dateDict['year'] = str(datetime_object.year)
        elif int(date[0]) + 1 == int(date[2]) or int(date[0]) - 1 == int(date[2]):
            dateDict['month'] = date[0]
            seconds_since_epoch = time.time()
            datetime_object = datetime.datetime.fromtimestamp(seconds_since_epoch)
            dateDict['year'] = str(datetime_object.year)
    return (dateDict['month'], dateDict['year'])

def get_data(file_name):
    global question
    with open(file_name, 'rt') as fout:

        #all the lines of data read as a list of lines
        lines = fout.readlines()

        #data from app contains all polls so this is more or less just incase any previous
        #poll responses slip through the cracks

        question = ''
        i = len(lines)-1
        while question == '' and i >= 0:
            individual = lines[i].split(',')
            for characteristic in individual:
                if '?' in characteristic:
                    question = characteristic
                    break
                i -= 1



        #list of individuals that will be returned
        individuals = []

        #base parties
        parties = ['republican', 'democrat', 'independent', 'democratic']

        #fields
        fields = ['policy', 'administrative', 'communicators', 'communications', 'admin',
                  'administrator',]
        comms = ['communicators', 'communications']
        admin = ['administrative', 'administrator', 'admin']

        #for each response
        i = 0
        for line in lines:
            #splits the response by email, party, birthday, etc
            line = line.split(',')
            while '\n' in line:
                line.remove('\n')
            while '' in line:
                line.remove('')

            ind_question = ''
            for characteristic in line:
                if '?' in characteristic or 'agree or disagree' in characteristic.lower():
                    ind_question = characteristic
                    break

            if ind_question == question or ind_question == '':
                try:
                    response = line[-1].strip('\n')
                except IndexError as e:
                    break
                email = 'example@gmail.com'
                birthdate = '00/00/0000'
                party = ''
                affiliation = 'us example'
                gender = ''
                office = 'none'
                job_title = 'none'
                field = 'other'
                excess = []

                #for characteristic in line
                for characteristic in line:
                    if line.index(characteristic) == len(line) - 1 or characteristic == 'Email':
                        break
                    characteristic = characteristic.lower()
                    #for every part of each response
                    if '@' in characteristic and email == 'example@gmail.com':
                        email = characteristic
                    elif characteristic.count('/') > 1 and birthdate == '00/00/0000':
                        birthdate = characteristic
                    elif characteristic in parties and party == '':
                        if characteristic == 'democratic':
                            party = 'democrat'
                        else:
                            party = characteristic
                    elif ('house of representatives' in characteristic or characteristic == 'house') and affiliation == 'us example':
                        affiliation = 'house of rep'
                    elif ('senate' == characteristic or ('senate' in characteristic and 'u.s' in characteristic)) and affiliation == 'us example':
                        affiliation = 'u.s senate'
                    elif (characteristic == 'f' or characteristic == 'm') and gender == '':
                        gender = characteristic
                    elif ('rep.' in characteristic or 'representative' in characteristic or 'sen.' in characteristic
                    or 'senator' in characteristic) and office == 'none':
                        office = characteristic
                    else:
                        condition = False
                        if field == 'other':
                            for item in fields:
                                if item in characteristic:
                                    t_char = characteristic.split()
                                    try:
                                        if len(t_char) < 3:
                                            if not t_char.index(item) < len(t_char)-1:
                                                if item in comms:
                                                    field = 'communicators'
                                                elif item in admin:
                                                    field = 'administrative'
                                                else:
                                                    field = characteristic
                                                condition = True
                                                break
                                    except:
                                        pass
                        if not condition:
                            if '?' not in characteristic:
                                excess.append(characteristic)
                #only runs if a response was found (only stops empty individuals)
                if response != '' and response != 'Answer To Poll' and response != 'answer':

                    temp_individual = Individual(email=email,birthday=birthdate,party=party,affiliation=affiliation,
                                             office=office,title=job_title,gender=gender,field=field,
                                             response=response,excess=excess)
                    date = getDate(file_name)
                    temp_individual.setDate(date)
                    individuals.append(temp_individual)



    return individuals
