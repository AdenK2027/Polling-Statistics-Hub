from src.individual import Individual
#takes csv data from polls and reads it as individuals with characteristics seen in Individual.py
question = ''
def get_question():
    return question
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
                                        if len(t_char) < 2:
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
                if response != '' and response != 'Answer To Poll':
                    temp_individual = Individual(email=email,birthday=birthdate,party=party,affiliation=affiliation,
                                             office=office,title=job_title,gender=gender,field=field,
                                             response=response,excess=excess)
                    individuals.append(temp_individual)
    return individuals
