from datetime import *

def default_constructor(data):
    base_percentages = get_answer_percentages(data)
    data_display = 'Category|Overall|'
    for response in base_percentages:
        response = response[:response.index(':')]
        data_display += (response + '|')
    data_display += 'Overall Percentage|'
    for response in base_percentages:
        response = response[:response.index(':')]
        data_display += (response + ' Percentage|')
    data_display += '\n'
    data_display += 'Overall|'
    total0counts = get_overall_response_count(data)
    data_display += str(total0counts[0]) + '|'
    for item in total0counts[1]:
        data_display += str(item) + '|'
    total_percentage = 0
    for response in base_percentages:
        total_percentage += float(response[response.index(':')+1:len(response)-1])
    data_display += str(total_percentage) + '%|'
    for response in base_percentages:
        response = response[response.index(':')+1:]
        data_display += response + '|'
    data_display += '\n'
    return data_display

def get_responses(data):
    answers = []
    counter = []
    total = 0
    for person in data:
        response = person.response
        if response not in answers:
            # print(f"'{response}'")
            answers.append(response)
            counter.append(1)
            total += 1
        else:
            counter[answers.index(response)] += 1
            total += 1
    return answers, counter, total

def get_answer_percentages(data):
    answers, counter, total = get_responses(data)

    return_list = []
    for response in answers:
        index = answers.index(response)
        response = response.strip('\n')
        try:
            percentage = float(f"{counter[index]/total*100:.2f}")
        except ZeroDivisionError as e:
            percentage = 0
        return_list.append(f"{response}:{percentage}%")

    return return_list

def party_sort(list):
    new_list = []
    if 'republican' in list:
        new_list.append('republican')
    if 'democrat' in list:
        new_list.append('democrat')
    list.sort()
    for item in list:
        if item not in new_list:
            new_list.append(item)
    if 'unknown' in new_list:
        new_list.pop(new_list.index('unknown'))
        new_list.append('unknown')
    return new_list

def get_parties(data):
    parties = []
    for person in data:
        if person.party not in parties:
            if person.party == '':
                parties.append('')
            else:
                parties.append(person.party)
    for i in range(len(parties)):
        if parties[i] == '':
            parties[i] = 'Unknown'
    return party_sort(parties)

def get_party_data(data):
    parties = get_parties(data)
    responses = get_responses(data)[0]
    result = {'total':0}
    for party in parties:
        result[party] = {'total':0}
        for response in responses:
            result[party][response] = 0

    for person in data:
        party = person.party
        if party == '':
            party = 'Unknown'
        result[party][person.response] += 1
        result[party]['total'] += 1
        result['total'] += 1
    return result

def get_overall_response_count(data):
    #total number of responses
    total_count = 0

    #specifics is a list of the response values in the order that they appear in get_responses
    specifics = []
    responses = get_responses(data)[0]
    for i in range(len(responses)):
        specifics.append(0)
    for person in data:
        specifics[responses.index(person.response)] += 1
        total_count += 1
    return total_count, specifics


#Returns a list of all the different affiliations (house, senate)
def get_affiliations(data):
    affiliations = []
    for person in data:
        if person.affiliation not in affiliations:
            affiliations.append(person.affiliation)

    #if there are no unknowns it adds one just because in my write affiliations code
    #i have it write unknown data even if there is none
    if '' not in affiliations:
        affiliations.append('')
    return affiliations

def get_affiliation_data(data):
    total = get_responses(data)[2]
    responses = get_responses(data)[0]
    result = {'total': total}
    affiliations = get_affiliations(data)
    # adds affiliation entries to the results
    for affiliation in get_affiliations(data):
        result[affiliation] = {}

    # sets the baseline of each response within each affiliation
    # result = {'total':TOTAL, AFF:{res1:0,res2:1}, AFF2:{res1:1,res2:0}}, AFF3:{}}, etc.
    for affiliation in affiliations:  #
        result[affiliation] = {'total': 0}  #
        for response in responses:  #
            result[affiliation][response] = 0  #
    # sets the baseline of each response for each party within each affiliation

    for person in data:
        result[person.affiliation][person.response] += 1
        result[person.affiliation]['total'] += 1

    return result

def format_time(today):
    result = []
    result.append(int(today[5:7]))
    result.append(int(today[-2:]))
    result.append(int(today[:4]))
    return result
def assume_age(data):
    #sets a current date so this doesn't need to be updated
    today = str(date.today())

    #for every response
    for person in data:

        #if the person didn't put a birthday
        if person.birthdate[0] == 0:

            #if an intern, assumes they were born today
            if 'intern' in person.job_title:
                #splits title so [comp, sci, intern] or [intern, overseer]
                title = person.job_title.split(' ')

                index = -1
                #gets the index of the intern word
                for i in range(len(title)):
                    if 'intern' in title[i]:
                        index = i
                        break
                # if intern is the last word in the title then it's probably SOMETHING intern
                if index == len(title)-1:
                    person.birthdate = [today[5:7], {today[-2:]}, today[:4]]
                #if not then its probably intern manager/overseer/etc
                else:
                    pass

            #if a senior position assumes they were born 31 years ago
            if 'senior' in person.job_title:
                person.birthdate = [today[5:7],today[-2:],int(today[:4])-31]

def check_age(person):
    # current date in [M,D,YYYY] format
    today = format_time(str(date.today()))

    cat = 'unknown'
    # grabs birthday in [M,D,YYYY] format
    birthday = person.birthdate

    try:
        # if no birthday was found
        if birthday[0] == 0:
            cat = 'unknown'

        # if the year is more than 30 years ago
        elif today[2] - birthday[2] > 30:
            cat = 'over'

        # else if the year is exactly 30 years ago
        elif today[2] - birthday[2] == 30:
            # if the month is before today
            if today[0] - birthday[0] > 0:
                cat = 'over'
            # if the month is exactly today
            elif today[0] - birthday[0] == 0:
                # if the day is today or before
                if today[1] - birthday[1] >= 0:
                    cat = 'over'
                # if the day is in the future
                elif today[1] - birthday[1] < 0:
                    cat = 'under'
            # if the month is in the future
            elif today[0] - birthday[0] < 0:
                cat = 'under'

        # if the year is less than 30 years ago
        elif today[2] - birthday[2] < 30:
            cat = 'under'
    except TypeError as e:
        person.dump()
    return cat

def count_responses_by_age(data):

    #if job data is in the file, assumes some ages (TURNED OFF)
    #assume_age(data)

    #gets all responses (always in the same order)
    responses = get_responses(data)[0]

    #over or under 30 responses
    results = {'under':[],'over':[],'unknown':[]}

    #sets default values for age sets
    for i in range(len(responses)):
        results['under'].append(0)
        results['over'].append(0)
        results['unknown'].append(0)

    #current date in [M,D,YYYY] format
    today = format_time(str(date.today()))

    #for every person
    for person in data:
        cat = check_age(person)
        results[cat][responses.index(person.response)] += 1
    return results

def field_sort(list):
    new_list = []
    if 'senior policy' in list:
        new_list.append('senior policy')
    if 'junior policy' in list:
        new_list.append('junior policy')
    if 'policy' in list:
        new_list.append('policy')
    list.sort()
    for item in list:
        if item not in new_list:
            new_list.append(item)
    if 'unknown' in new_list:
        new_list.pop(new_list.index('unknown'))
        new_list.append('unknown')
    return new_list


#gets responses based on field (admin, policy, etc)
def get_field_data(data):

    #responses and fields
    responses = get_responses(data)[0]
    fields = get_fields(data)

    #total number of responses
    result = {'total':0}

    #sets the base dict to have every field and every field dict to have every response
    for field in fields:
        result[field] = {'total':0}
        for response in responses:
            result[field][response] = 0

    #if there is no policy field (instead there is sen. policy and jun. policy)
    try:
        result['policy'][responses[0]] += 1
    except KeyError as e:
        result['policy'] = {}
        for response in responses:
            result['policy'][response] = 0
        result['policy']['total'] = 0

    for person in data:
        result[person.field][person.response] += 1
        result[person.field]['total'] += 1
        result['total'] += 1
        if 'policy' in person.field and person.field != 'policy':
            result['policy'][person.response] += 1
            result['policy']['total'] += 1

    return result

def get_fields(data):
    fields = []
    for person in data:
        if person.field not in fields:
            fields.append(person.field)
    if '' in fields:
        fields.pop(fields.index(''))
        fields.append('')
    if 'policy' in fields:
        fields.pop(fields.index('policy'))
        fields.insert(0,'policy')
    return fields

def get_gender_data(data):
    result = {'total':0,'m':{'total':0},'f':{'total':0},'':{'total':0}}
    responses = get_responses(data)[0]
    genders = list(result.keys())
    for gender in genders:
        if gender != 'total':
            for response in responses:
                result[gender][response] = 0
    for person in data:
        if person.gender == 'm':
            gen = 'm'
        elif person.gender == 'f':
            gen = 'f'
        else:
            gen = ''
        result[gen][person.response] += 1
        result[gen]['total'] += 1
        result['total'] += 1
    return result

#===========================================================================================
#PARTY SPECIFIC DATA STARTS HERE
#===========================================================================================

def get_gender_party_data(data):
    total = get_responses(data)[2]
    responses = get_responses(data)[0]
    result = {'total': total}
    genders = ['m', 'f', '']
    parties = ['dem', 'rep']

    # adds field entries to the results
    for gender in genders:
        result[gender] = {}

    # sets the baseline of each response for each party within each field
    # result = {'total':TOTAL, FIELD:{DEM:{res1:0,res2:1}, REP:{res1:1,res2:0}}, FIELD2:{}, etc.
    for gender in genders:  #
        for party in parties:  #
            result[gender][party] = {'total': 0}  #
            for response in responses:  #
                result[gender][party][response] = 0  #
    # sets the baseline of each response for each party within each field

    for person in data:
        party = person.party.lower()[:3]
        if party in parties:
            if person.gender == 'm':
                gen = 'm'
            elif person.gender == 'f':
                gen = 'f'
            else:
                gen = ''
            result[gen][party][person.response] += 1
            result[gen][party]['total'] += 1

    # print(result)
    return result

def get_field_party_data(data):
    total = get_responses(data)[2]
    responses = get_responses(data)[0]
    result = {'total': total}
    fields = get_fields(data)
    parties = ['dem', 'rep']

    #adds field entries to the results
    for field in fields:
        result[field] = {}

    #sets the baseline of each response for each party within each field
    #result = {'total':TOTAL, FIELD:{DEM:{res1:0,res2:1}, REP:{res1:1,res2:0}}, FIELD2:{}, etc.
    for field in fields:                                               #
        for party in parties:                                          #
            result[field][party] = {'total':0}                         #
            for response in responses:                                 #
                result[field][party][response] = 0                     #
    #sets the baseline of each response for each party within each field



    for person in data:
        party = person.party.lower()[:3]
        if party in parties:
            result[person.field][party][person.response] += 1
            result[person.field][party]['total'] += 1

    #print(result)
    return result

def get_house0senate_party_data(data):
    total = get_responses(data)[2]
    responses = get_responses(data)[0]
    result = {'total': total}
    affiliations = get_affiliations(data)
    parties = ['dem', 'rep']

    # adds affiliation entries to the results
    for affiliation in get_affiliations(data):
        result[affiliation] = {}

    # sets the baseline of each response for each party within each affiliation
    # result = {'total':TOTAL, AFF:{DEM:{res1:0,res2:1}, REP:{res1:1,res2:0}}, AFF2:{}, etc.
    for affiliation in affiliations:  #
        for party in parties:  #
            result[affiliation][party] = {'total': 0}  #
            for response in responses:  #
                result[affiliation][party][response] = 0  #
    # sets the baseline of each response for each party within each affiliation

    for person in data:
        party = person.party.lower()[:3]
        if party in parties:
            result[person.affiliation][party][person.response] += 1
            result[person.affiliation][party]['total'] += 1

    #print(result)
    return result

def get_age_party_data(data):
    total = get_responses(data)[2]
    responses = get_responses(data)[0]
    result = {'total': total}
    ages = list(count_responses_by_age(data).keys())
    parties = ['dem', 'rep']

    # adds age entries to the results
    for age in ages:
        result[age] = {}

    # sets the baseline of each response for each party within each age
    # result = {'total':TOTAL, AGE:{DEM:{res1:0,res2:1}, REP:{res1:1,res2:0}}, AGE2:{}, etc.
    for age in ages:  #
        for party in parties:  #
            result[age][party] = {'total': 0}  #
            for response in responses:  #
                result[age][party][response] = 0  #
    # sets the baseline of each response for each party within each age

    for person in data:
        party = person.party.lower()[:3]
        if party in parties:
            result[check_age(person)][party][person.response] += 1
            result[check_age(person)][party]['total'] += 1

    #print(result)
    return result
