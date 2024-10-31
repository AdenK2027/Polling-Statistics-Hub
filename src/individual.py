class Individual():
    def __init__(self,email='example@mail.com', birthday = '00/00/0000',
                 party='example party', affiliation='U.S Blank',
                 office='Rep. FName LName',title='example_title',
                 gender='NA',field='field',storage=[],
                 response='',excess=[]):
        if email == '':
            email = 'example@gmail.com'
        self.email=email
        if birthday == '':
            self.birthdate = [0, 0, 0]
        else:
            birthdate = birthday.split(' ')[0]
            birthdate = birthdate.split('/')
            birthday = []
            for i in range(len(birthdate)):
                try:
                    birthday.append(int(birthdate[i]))
                except ValueError as e:
                    birthday.append(0)
            self.birthdate = birthday

        if party == '':
            party = 'unknown'
        self.party = party
        self.affiliation = affiliation
        if office == '':
            office = "Rep/Sen. Fname Lname"
        self.office = office
        self.job_title = title
        self.gender = gender
        self.field = field
        self.response = response
        self.storage = storage
        self.excess = excess
        if self.birthdate[0] == 0 and len(self.excess) > 0:
            self.excess.pop()

    def __str__(self):
        return f'{self.email}({self.party}), {self.job_title} for {self.office} said {self.response}'

    def dump(self):
        print(f"Email:{self.email}, Birthday:{self.birthdate}, Party:{self.party}\n"
              f"Affil:{self.affiliation}, Office:{self.office}, Title:{self.job_title}\n"
              f"Gender:{self.gender}, Field:{self.field}, Response:{self.response}\n"
              f"Excess:{self.excess}")

    def get_storage(self):
        return self.storage

