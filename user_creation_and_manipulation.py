import uuid
import re
import names
from datetime import date
from random import randint


class User:
    def __init__(self, user_id, name, surname, birth_date):  # birth_date in format datetime.date(yyyy, mm, dd)
        self.user_id = user_id
        self.name = str(name).capitalize()
        self.surname = str(surname).capitalize()
        self.birth_date = birth_date
        self.email = None
        self.email_correct = False
        self.localization = (None, None)
        self.tags = []
        self.age = None

    def set_localization(self, localization):
        self.localization = localization

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

    # @staticmethod
    def check_email(self, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if re.search(regex, email):
            self.email = email
            self.email_correct = True

    def update_user(self, given_localization, given_email):
        self.set_localization(given_localization)
        self.calculate_age()
        self.check_email(given_email)

    def create_firebase_entry(self):
        data = {
            'User_ID': self.user_id,
            'Name': self.name,
            'Surname': self.surname,
            'Email': self.email,
            'Birth date': str(self.birth_date),
            'Age': self.age,
            'Current localization': self.localization,
            'Current used tags': self.tags
        }
        return data

    def print_user(self):
        print(f"Name & surname: {self.name} {self.surname}")
        print(f"Age: {self.age}")
        print(f"E-mail: {self.email}")


def create_users(num_of_users):
    list_of_users = []

    for _ in range(0, num_of_users):
        user = User(str(uuid.uuid4()).replace("-", ""), names.get_first_name(), names.get_last_name(),
                    date(2000 - randint(0, 10), randint(1, 12), randint(1, 28)))
        user.update_user((0, 0), f"{user.name.lower()}.{user.surname.lower()}@gmail.com")
        list_of_users.append(user)
    return list_of_users


for user in create_users(100):
    user.print_user()
    print()
