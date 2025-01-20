import analytics
def write_party_data(data, display):
    #dict of {total:#, DEM:{resp1:#,resp2:#}, REP:{resp1:#,resp2:#}}
    party_data = analytics.get_party_data(data)

    #grabs the parties (should always be Republican, Democrat, and '')
    parties = list(party_data.keys())

    #this is a tuple of (list of responses, counter for each response, total)
    responses = analytics.get_responses(data)

    for party in parties:
        #doesn't write data for total
        if party != 'total':

            #party name addition
            display += party[:1].upper() + party[1:]
            if party == '':
                display += ' Party'
            display += '|'

            #party total addition
            display += str(party_data[party]['total']) + '|'

            #party response value additions
            for response in responses[0]:
                display += str(party_data[party][response]) + '|'

            #party percentage addition (#reps/(#dems+#reps+#inds+#na)
            try:
                display += f"{party_data[party]['total']/party_data['total']*100:.2f}%|"
            except ZeroDivisionError as e:
                display += "0%|"

            #party response percentage within party (#repRes1/(#resRep1+#resRep2)
            for response in responses[0]:
                try:
                    display += f"{party_data[party][response]/party_data[party]['total']*100:.2f}%|"
                except ZeroDivisionError as e:
                    display += '0%|'

            #new line for next party
            display += '\n'


    return display

#writes affiliation data for the house, senate, and unknown
def write_house0senate_data(data, display):
    affil_data = analytics.get_affiliation_data(data)
    responses = analytics.get_responses(data)[0]
    affiliations = list(affil_data.keys())
    if '' not in affiliations:
        affiliations.append('')
    for affil in affiliations:
        if affil != 'total' and affil != '':
            if 'senate' in affil.lower():
                display += 'Senate|'
            elif 'house' in affil.lower():
                display += 'House|'
            else:
                display += 'Other Departments|'
            display += str(affil_data[affil]['total']) + '|'

            for response in responses:
                display += str(affil_data[affil][response]) + '|'
            try:
                display += f"{affil_data[affil]['total'] / affil_data['total'] * 100:.2f}%|"
            except ZeroDivisionError as e:
                display += f"0%|"

            for response in responses:
                try:
                    display += f"{affil_data[affil][response] / affil_data[affil]['total'] * 100:.2f}%|"
                except ZeroDivisionError as e:
                    display += f"0%|"

            display += '\n'
    return display

def write_age_data(data, data_display):
    responses = analytics.get_responses(data)
    age_stats = analytics.count_responses_by_age(data)
    ages = ['under', 'over', 'unknown']
    for age in ages:
        data_display += age[:1].upper() + age[1:]
        if age == 'unknown':
            data_display += ' age|'
        else:
            data_display += ' 30|'
        total = 0
        for stat in age_stats[age]:
            total += stat
        data_display += str(total) + '|'
        for stat in age_stats[age]:
            data_display += str(stat) + '|'
        try:
            data_display += f"{total / responses[2] * 100:.2f}%|"
        except ZeroDivisionError as e:
            data_display += f"0%|"
        for stat in age_stats[age]:
            try:
                data_display += f"{stat / total * 100:.2f}%|"
            except ZeroDivisionError as e:
                data_display += f"0%|"
        data_display += '\n'
    return data_display

def write_field_data(data, display):
    field_data = analytics.get_field_data(data)
    responses = analytics.get_responses(data)
    fields = list(field_data.keys())
    fields = analytics.field_sort(fields)
    for field in fields:
        if field != 'total':
            if 'admin' in field:
                display += 'Admin|'
            elif field == '':
                display += 'Unknown Field|'
            elif field == 'other':
                display += 'Other Fields|'
            else:
                display += field[0:1].upper() + field[1:] + '|'
            display += str(field_data[field]['total']) + '|'
            for response in responses[0]:
                display += str(field_data[field][response]) + '|'
            try:
                display += f"{field_data[field]['total']/field_data['total'] * 100:.2f}%|"
            except ZeroDivisionError as e:
                display += f"0%|"
            for response in responses[0]:
                try:
                    display += f"{field_data[field][response]/field_data[field]['total']*100:.2f}%|"
                except ZeroDivisionError as e:
                    display += f"0%|"

            display += '\n'


    return display

def write_gender_data(data, display):
    gender_data = analytics.get_gender_data(data)
    responses = analytics.get_responses(data)[0]
    genders = list(gender_data.keys())
    for gender in genders:
        if gender != 'total':
            if gender == 'm':
                display += 'Men|'
            elif gender == 'f':
                display += 'Women|'
            else:
                display += 'Unknown Gender|'
            display += str(gender_data[gender]['total']) + '|'

            for response in responses:
                display += str(gender_data[gender][response]) + '|'
            try:
                display += f"{gender_data[gender]['total'] / gender_data['total']*100:.2f}%|"
            except ZeroDivisionError as e:
                display += "0%|"

            for response in responses:
                try:
                    display += f"{gender_data[gender][response] / gender_data[gender]['total']*100:.2f}%|"
                except ZeroDivisionError as e:
                    display += f"0%|"

            display += '\n'
    return display

def write_gender_party_data(data,display):
    parties = ['rep','dem']
    split_gender_data = analytics.get_gender_party_data(data)
    responses = analytics.get_responses(data)[0]
    genders = list(split_gender_data.keys())
    for gender in genders:
        for party in parties:
            if gender != 'total' and gender != '':
                string = ''
                if party == 'rep':
                    string += 'GOP '
                else:
                    string += 'DEM '
                if gender == 'm':
                    string += 'Men|'
                elif gender == 'f':
                    string += 'Women|'
                else:
                    continue
                display += string
                display += str(split_gender_data[gender][party]['total']) + '|'

                for response in responses:
                    display += str(split_gender_data[gender][party][response]) + '|'
                try:
                    display += f"{split_gender_data[gender][party]['total'] / split_gender_data['total'] * 100:.2f}%|"
                except ZeroDivisionError as e:
                    display += '0%|'

                for response in responses:
                    try:
                        display += f"{split_gender_data[gender][party][response] / split_gender_data[gender][party]['total'] * 100:.2f}%|"
                    except ZeroDivisionError as e:
                        display += f"0%|"

                display += '\n'
    return display

def write_field_party_data(data, display):
    listed_fields = analytics.get_fields(data)
    listed_fields = analytics.field_sort(listed_fields)
    #listed_fields = ['Policy', 'Communicators']
    field_data = analytics.get_field_party_data(data)
    responses = analytics.get_responses(data)
    for field in listed_fields:
        if field != 'total':
            for party in list(field_data[field].keys()):
                if field in listed_fields:
                    if party == 'rep':
                        display += 'GOP '
                    else:
                        display += 'DEM '
                    if field == 'Communicators':
                        display += 'Comms|'
                    elif field == "Administrative":
                        display += 'Admin|'
                    elif field == '':
                        display += 'Unknown Fields|'
                    else:
                        display += field[0:1].upper() + field[1:] + '|'

                    display += str(field_data[field][party]['total']) + '|'

                    for response in responses[0]:
                        display += str(field_data[field][party][response]) + '|'

                    display += f"{field_data[field][party]['total'] / responses[2] * 100:.2f}%|"
                    for response in responses[0]:
                        try:
                            display += f"{field_data[field][party][response]/field_data[field][party]['total']*100:.2f}%|"
                        except ZeroDivisionError as e:
                            display += '0%|'

                    display += '\n'
    return display

def write_house0senate_party_data(data,display):
    affil_data = analytics.get_house0senate_party_data(data)
    responses = analytics.get_responses(data)
    # print(affil_data)
    for affil in list(affil_data.keys()):
        if affil != 'total' and affil != '':
            for party in list(affil_data[affil].keys()):
                if party == 'rep':
                    display += 'GOP '
                else:
                    display += 'DEM '
                if 'house' in affil.lower():
                    display += 'House|'
                elif 'senate' in affil.lower():
                    display += 'Senate|'
                else:
                    display += 'Other Departments|'

                display += str(affil_data[affil][party]['total']) + '|'

                for response in responses[0]:
                    display += str(affil_data[affil][party][response]) + '|'

                display += f"{affil_data[affil][party]['total'] / responses[2] * 100:.2f}%|"
                for response in responses[0]:
                    try:
                        display += f"{affil_data[affil][party][response] / affil_data[affil][party]['total'] * 100:.2f}%|"
                    except ZeroDivisionError as e:
                        display += "0%|"

                display += '\n'
    return display

def write_age_party_data(data,display):
    age_data = analytics.get_age_party_data(data)
    responses = analytics.get_responses(data)
    for age in list(age_data.keys()):
        if age != 'total' and age != 'unknown':
            for party in list(age_data[age].keys()):
                if party == 'rep':
                    display += 'GOP '
                else:
                    display += 'DEM '
                display += age[0:1].upper() + age[1:] + ' 30|'

                display += str(age_data[age][party]['total']) + '|'

                for response in responses[0]:
                    display += str(age_data[age][party][response]) + '|'

                try:
                    display += f"{age_data[age][party]['total'] / responses[2] * 100:.2f}%|"
                except ZeroDivisionError as e:
                    display += "0%|"

                for response in responses[0]:
                    try:
                        display += f"{age_data[age][party][response] / age_data[age][party]['total'] * 100:.2f}%|"
                    except ZeroDivisionError as e:
                        display += "0%|"

                display += '\n'
    return display

# FUNCTION RUNNERS

def write_all_reg_data(data,display):
    # adds all of the party specific data
    display = write_party_data(data, display)

    # adds all of the house/senate specific data INCOMPLETE
    display = write_house0senate_data(data, display)

    # adds all of the age specific data
    display = write_age_data(data, display)

    # adds all of the field specific data
    display = write_field_data(data, display)

    # adds all of the gender specific data
    display = write_gender_data(data, display)

    return display

def write_all_party_data(data,display):
    # adds all of the party specific gender data
    display = write_gender_party_data(data, display)

    # adds all of the party specific field data
    display = write_field_party_data(data, display)

    # adds all of the party specific house/senate data
    display = write_house0senate_party_data(data, display)

    display = write_age_party_data(data, display)

    return display

