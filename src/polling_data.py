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

        question = lines[-1].split(',')[-2]
        i = len(lines)-2
        while '?' not in question:
            question = lines[i].split(',')[-2]
            i -= 1

        #list of individuals that will be returned
        individuals = []

        #for each response
        for line in lines:
            #splits the response by email, party, birthday, etc
            line = line.split(',')

            #again just verifying that the response is for the relevant question
            if line[-2] == question:
                #for every part of each response
                email = line[0].lower()
                birthdate = line[1]
                party = line[2].lower()
                affiliation = line[3].lower()
                office = line[4].lower()
                job_title = line[5].lower()
                field = line[-4].lower()
                gender = line[-3].lower()
                response = line[-1].strip('\n')

                #only runs if a response was found (only stops empty individuals)
                if response != '':
                    temp_individual = Individual(email=email,birthday=birthdate,party=party,affiliation=affiliation,
                                             office=office,title=job_title,gender=gender,field=field,
                                             response=response)
                    individuals.append(temp_individual)
    # for person in individuals:
    #     print(analytics.check_age(person))
    #     person.dump()
    for i in range(len(individuals)):
        if individuals[i].response == None:
            individuals.remove(individuals[i])
    return individuals
