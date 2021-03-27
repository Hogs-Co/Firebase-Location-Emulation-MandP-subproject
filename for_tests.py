import time
import re
import names
from datetime import date
from firebase import Firebase
from random import randint

# firebase project identifier: fir-test-env-mandp
# firebase table identifier: fir-test-env-mandp-default-rtdb
# firebase link: https://fir-test-env-mandp-default-rtdb.firebaseio.com/

config = {
  "apiKey": "AAAA3KmrBPQ:APA91bFqfELPwbuc7gAS1FkgCland5wKUAEZpEaYUmLdjdjr-rUVF1zBp_5JKHY_TxbsT6ROtiRy28gCd2pEPmHkawl2b-ow1H2rkOCknJ6b3npX09_flYlFZnQI1O5R0F-EC_PoJw1D",
  "authDomain": "fir-test-env-mandp.firebaseapp.com",
  "databaseURL": "https://fir-test-env-mandp-default-rtdb.firebaseio.com",
  "storageBucket": "fir-test-env-mandp.appspot.com"
  # optional - overrides security rules
  # "serviceAccount": "fir-test-env-mandp-firebase-adminsdk-kswac-032b264225.json"
}

# firebase_dblink connection establish
firebase = Firebase(config)

# in classes:
# thing     - is public
# _thing    - is protected
# __thing   - is private


class User:
    def __init__(self, name, surname, birth_date):  # birth_date in format datetime.date(yyyy, mm, dd)
        self.user_id = None
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

    def print_user(self):
        print(f"Name & surname: {self.name}, {self.surname}")
        print(f"Age: {self.age}")
        print(f"E-mail: {self.email}")


def update_user(given_user, given_localization, given_email):
    given_user.set_localization(given_localization)
    given_user.calculate_age()
    given_user.check_email(given_email)


user1 = User(names.get_first_name(), names.get_last_name(), date(2000 - randint(0, 10), randint(1, 12), randint(1, 28)))
update_user(user1, (0, 0), f"{user1.name.lower()}.{user1.surname.lower()}@google.com")
# user1.print_user()

data1 = {
    'Name': user1.name + ' ' + user1.surname,
    'Email': user1.email,
    'Birth date': user1.birth_date,
    'Age': user1.age,
    'Current localization': user1.localization,
    'Current used tags': user1.tags
}

# user2 = User("maciej", "luciński", date(1998, 4, 18))
# update_user(user2, (0, 0), "maciej.lucinski@edu.lodz.pl")
# user2.print_user()

# data2 = {
#     'Name': user2.name + ' ' + user2.surname,
#     'Email': user2.email,
#     'Birth date': user2.birth_date,
#     'Age': user2.age,
#     'Current localization': user2.localization,
#     'Current used tags': user2.tags
# }

# pushing data and data2 to firebase_dblink
# TODO read about .put() and .patch() how to update already existing data entries?
# user_data_id = firebase_dblink.post('/fir-test-env-mandp-default-rtdb/Users', data1)
# print(user_data_id)
# print("-MWiyGcWO5t39J3zn34q")

# pulling data from firebase_dblink

# pull_result = firebase_dblink.get('/fir-test-env-mandp-default-rtdb/Users/', )

db = firebase.database()
all_user_ids = db.child("/fir-test-env-mandp-default-rtdb/Users").shallow().get()
user_ids = []

for user_id in all_user_ids.val():
    user_ids.append(user_id)

# for key, value in pull_result.items():
#     print(f"User ID token: {key}")
#     for sub_key, sub_value in value.items():
#         print(f"\t{sub_key:{' '}{'<'}{20}}: {sub_value}")
