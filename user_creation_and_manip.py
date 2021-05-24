import uuid
import re
import names
from datetime import date
from random import randint


class User:
    def __init__(self, user_id, name, surname, birth_date):  # birth_date in format datetime.date(yyyy-mm-dd)
        self.user_id = user_id
        self.name = str(name).capitalize()
        self.surname = str(surname).capitalize()
        self.birth_date = birth_date
        self.age = None
        self.email = None
        self.imageLink = "https://i.imgur.com/FtGIXlN.png"
        self.email_correct = False
        self.location = [51.735172, 19.492445]
        # self.phone = ""
        self.info = "Created using EmulationApp"
        self.tags = []
        self.user_generated_tags = []

    def set_location(self, location):
        self.location = location

    def calculate_age(self):
        today = date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, month=self.birth_date.month + 1, day=1)
        if birthday > today:
            self.age = today.year - self.birth_date.year - 1
        else:
            self.age = today.year - self.birth_date.year

    def check_email(self, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if re.search(regex, email):
            self.email = email
            self.email_correct = True

    def update_user(self, given_localization, given_email):
        self.set_location(given_localization)
        self.calculate_age()
        self.check_email(given_email)

    def create_firebase_entry(self):
        data = {
            'Id': self.user_id,
            'Name': self.name,
            'Surname': self.surname,
            'Email': self.email,
            'Birthdate': str(self.birth_date),
            'ImageLink': str(self.imageLink),
            'Age': self.age,
            'CurrentLocation': self.location,
            'CurrentUsedTags': self.tags,
            'UserGeneratedTags': self.user_generated_tags,
            'Info': self.info
        }
        return data

    def print_user(self):
        for key, value in self.create_firebase_entry().keys():
            print(f"{str(key):{' '}{'<'}{25}}: {value}")


def create_users(num_of_users):
    list_of_users = []

    # TODO is uuid4 to str change really necessary?
    # possible fix is this:
    # |-------------------------------------------------------------------------|
    # | import json                                                             |
    # | from uuid import UUID                                                   |
    # |                                                                         |
    # | class UUIDEncoder(json.JSONEncoder):                                    |
    # |     def default(self, obj):                                             |
    # |         if isinstance(obj, UUID):                                       |
    # |             # if the obj is uuid, we simply return the value of uuid    |
    # |             return obj.hex                                              |
    # |         return json.JSONEncoder.default(self, obj)                      |
    # |-------------------------------------------------------------------------|
    for _ in range(0, num_of_users):
        user = User(str(uuid.uuid4()).replace("-", "-"), names.get_first_name(), names.get_last_name(),
                    date(2000 - randint(0, 10), randint(1, 12), randint(1, 28)))
        user.update_user((0, 0), f"{user.name.lower()}.{user.surname.lower()}@gmail.com")
        list_of_users.append(user)
    return list_of_users


def check_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False
