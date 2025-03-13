import time
import datetime
from individual import Individual
#takes csv data from polls and reads it as individuals with characteristics seen in Individual.py
question = ''
def get_question():
    return question

def setDate(file_name, year):
    # creates a blank date that grabs only numbers and separators from the filename
    date = ''  #
    i = len(file_name)-1
    while i >= 0:
        if file_name[i] == '/':
            break
        i -= 1
    file_name = file_name[i:]
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
    listDate = []
    for i in range(len(date)): #for every character in the date
        char = date[i]
        if char == '-': #if the character is a sep.
            if len(listDate) > 0: #if there is content in the date (doesn't start with a sep.)
                if listDate[-1] != '-': #if the last item wasn't also a sep.
                    listDate.append(char) #adds the seperator
        elif char.isdigit(): #if the character was a number
            listDate.append(char) #adds the number

    #joins the list together and then splits it again to remove leading and following dashes
    date = ''.join(listDate)
    date = date.split('-')

    try:
        while not date[-1].isdigit():
            date.pop()
    except IndexError as e:
        return -1

    dateDict = {'month':-1, 'year':-1} #this will be used for the return

    if year in date:
        date.remove(year)
    # if there are three elements in the list (month, date, year) #
    if len(date) == 3:                                            #
                                                                  #
        #distributes the most probable dates                      #
        dateDict['month'] = date[0]                               #
        dateDict['year'] = date[2]                                #
    ###############################################################

    #else if there are four elements, then it is probably a range (month, day, month, day)
    elif len(date) == 4:                                                                #
                                                                                        #
        if year == '':
            #sets time standards to get current year                                        #
            seconds_since_epoch = time.time()                                               #
            datetime_object = datetime.datetime.fromtimestamp(seconds_since_epoch)          #
            dateDict['year'] = str(datetime_object.year - 1)                                #
        else:
            dateDict['year'] = year
                                                                                        #
        #if the two months are the same, just use the first month and assume the current year
        if date[0] == date[2]:                                                          #
            dateDict['month'] = date[0]                                                 #
                                                                                        #
        #if the two months aren't the same but are one away, use the first month        #
        elif int(date[0]) + 1 == int(date[2]) or int(date[0]) - 1 == int(date[2]):      #
            dateDict['month'] = date[0]                                                 #
                                                                                        #
        #otherwise, I have no idea what format this is in just assume the current year  #
        else:                                                                           #
            dateDict['month'] = '13' #sets to 13, will be read as N/A later             #
    #####################################################################################

    return (dateDict['month'], dateDict['year'])

def fixString(original): #removes and "'s as well as leading/following spaces
    result = ''
    for i in range(len(original)):
        if original[i] != '"' and original[i] != '\n':
            result += original[i]
    if len(result) > 0:
        origResult = result
        result = result.split()
        result = " ".join(result)
        if origResult[0] == ' ':
            result = ' ' + result
    return result

def fixLines(lines):
    fixedLines = []
    for line in lines: #line = 'email,name,date,etc'
        fixedLine = [] #['email', 'name', 'date']
        line = line.split(',')
        if len(line) > 0 and len(line) < 2:
            line = line[0]
            line = line.split('|')
        for characteristic in line: #line = ['email', 'name', 'date']
            if characteristic != "" and characteristic != "\n":
                fixedLine.append(fixString(characteristic)) #characteristic = 'email'
        if len(fixedLine) >= 1:
            fixedLines.append(fixedLine) #fixedLines = [['email', 'name'], ['email2', 'name2']]

    # removes all newlines and empty slots
    for line in fixedLines.copy():
        while '\n' in line:
            line.remove('\n')
        while '' in line:
            line.remove('')
    return fixedLines

def RemoveFloats(line):
    # creates a copy of the list to iterate through so the loop doesn't get messed up
    originalLine = line.copy()
    pass

    # for every element in a line (email, gender, response, etc)
    for item in originalLine:

        # creates an adjusted item that might meet removal criteria while preserving
        # the original item to be removed from the list
        adjustedItem = item

        # if there is a newline in the item, removes it
        if '\n' in item:
            adjustedItem = item[0:item.index('\n')] + item[item.index('\n'):]

        # checks if there is a percentage symbol in the item
        if '%' in adjustedItem:
            adjustedItem = item[0:item.index('%')] + item[item.index('%')+1:]

        # tries to convert the element into a float,
        try:
            isItemANumber = float(adjustedItem)

            # if the item can be converted into a float, then it is assumed to be a human
            # error and discounted from the data, there is a contigency at the bottom of
            # this function that reruns itself if there are no responses, due to the
            # accidental removal of genuine responses
            line.remove(item)

        except ValueError as e:  # if the element isn't a float then continue as normal
            continue
    return line

def setQuestion(lines):
    # data from app contains all polls so this is more or less just incase any previous
    # poll responses slip through the cracks

    question = ''
    i = len(lines) - 1 #starts at the bottom poll entry
    while question == '' and i >= 0: #until the question is determined or there are no more entries
        individual = lines[i] #each line is split into characteristics
        if len(individual) < 2 and len(individual) > 0:
            individual = individual[0].split('|')
        for characteristic in individual:

            #if the characteristic is a question
            if '?' in characteristic or 'agree or disagree' in characteristic.lower():

                #if the first character of the question is a space, then it was probably cut off
                if characteristic[0] != ' ':
                    question = characteristic
                else:
                    question = individual[individual.index(characteristic) - 1] + ',' + characteristic
                question = fixString(question)
                break
        i -= 1
    return question

def get_data(file_name, ignoreFloats = True, currentYear = ''):
    global question
    with open(file_name, 'rt') as fout:

        #all the lines of data read as a list of lines
        lines = fout.readlines()
        lines = fixLines(lines)

        question = setQuestion(lines)

        #list of individuals that will be returned
        individuals = []

        #base parties
        parties = ['republican', 'democrat', 'independent', 'democratic']

        #fields
        fields = ['policy', 'administrative', 'communicators', 'communications', 'admin',
                  'administrator',]
        comms = ['communicators', 'communications']
        admin = ['administrative', 'administrator', 'admin']

        lastResponse = -1
        #for each response
        for i in range(len(lines)):
            line = lines[i]

            #FLOAT REMOVAL
            if ignoreFloats:
                line = RemoveFloats(line)


            #Removes anything that isn't a character or number
            for item in line.copy():
                if len(item) < 2:
                    if not item.isalnum():
                        line.remove(item)


            #checks to see if the question for the results matches the question of the individual
            ind_question = ''
            for characteristic in line:

                #grabs the question from each individual
                if '?' in characteristic or 'agree or disagree' in characteristic.lower():

                    if ',' not in question:
                        ind_question = characteristic
                    else:
                        ind_question = line[line.index(characteristic)-1] + ',' + characteristic
                    ind_question = fixString(ind_question)
                    break

            if ind_question == question or (ind_question == '' and i - lastResponse < 20):
                try:
                    response = line[-1].strip('\n')
                    response = fixString(response)
                    response = response.lower()
                except IndexError as e:
                    break
                if response.lower() == 'answer':
                    continue
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
                    if line.index(characteristic) == len(line) - 1 or characteristic.lower() == 'email' or characteristic.lower() == 'emails':
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
                    date = setDate(file_name, currentYear)
                    if date != -1:
                        temp_individual.setDate(date)
                    else:
                        temp_individual.setDate()
                    individuals.append(temp_individual)
                    lastResponse = i

    # if there are no individuals (probably because the responses are supposed to be floats
    #and are subsequently removed because they are thought to be human error, run again but
    #without removing floats
    if len(individuals) < 1:
        individuals = get_data(file_name, False)
    return individuals
