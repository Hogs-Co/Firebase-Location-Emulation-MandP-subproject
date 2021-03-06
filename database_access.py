from firebase import Firebase
import user_creation_and_manip as ucm
import tag_creation_and_manip as tcm
from names import get_first_name
from collections import OrderedDict
import time
import uuid

# User data:
# 'User_ID' string
# 'Name' string
# 'Surname' string
# 'Email' string which must be compliant with ucam.User.check_email()
# 'Birth_date' in a date format - passed to firebase as string
# 'Age': int - amount of years from birth date to today
# 'Current_localization': two argument list - [longitude, latitude]
# 'Current_used_tags': list of maximum 4 custom tags and 2 age tags


# consts
USERS_DIR = "users"
TAGS_DIR = "tags"

# firebase project identifier: fir-test-env-mandp
# firebase table identifier: fir-test-env-mandp-default-rtdb
# firebase link: https://fir-test-env-mandp-default-rtdb.firebaseio.com/

# Emulation tests Firebase
# config = {
#     "apiKey": "AAAA3KmrBPQ:APA91bFqfELPwbuc7gAS1FkgCland5wKUAEZpEaYUmLdjdjr-rUVF1zBp_5JKHY_TxbsT6ROtiRy28gCd2pEPmHk"
#               "awl2b-ow1H2rkOCknJ6b3npX09_flYlFZnQI1O5R0F-EC_PoJw1D",
#     "authDomain": "fir-test-env-mandp.firebaseapp.com",
#     "databaseURL": "https://fir-test-env-mandp-default-rtdb.firebaseio.com",
#     "storageBucket": "fir-test-env-mandp.appspot.com",
#     "serviceAccount": "fir-test-env-mandp-firebase-adminsdk-kswac-032b264225.json"
# }

# Party-Meat tests Firebase
config = {
    "apiKey": "AIzaSyBuqichuoC8ytlbDHzlw7dsiaRa10FxB4E",
    "authDomain": "party-and-meat.firebaseapp.com",
    "databaseURL": "https://party-and-meat-default-rtdb.firebaseio.com",
    "storageBucket": "party-and-meat.appspot.com",
    "serviceAccount": "party-and-meat-firebase-adminsdk-r1dse-9055245288.json"
}

tag_keys = ['Name', 'CreationDate', 'Author', 'Users']

user_keys = ['Id', 'Name', 'Surname', 'Email', 'BirthDate', 'Age',
             'CurrentLocation', 'CurrentUsedTags', 'UserGeneratedTags',
             'Info', 'ImageLink']


class DatabaseData:
    def __init__(self):
        self.users_list = get_all_users()
        self.tags_list = get_all_tags()

    def update_data(self):
        self.users_list.clear()
        self.tags_list.clear()

        self.users_list = get_all_users()
        self.tags_list = get_all_tags()


# tag centered functions
def create_tags(num_of_tags):
    firebase = Firebase(config)
    db = firebase.database()

    list_of_user_ids = get_all_user_ids()
    tags_dict, updated_users_dict = tcm.create_tags_dict(num_of_tags, list(list_of_user_ids))

    db.child(TAGS_DIR).set(tags_dict)
    for key in updated_users_dict:
        db.child(USERS_DIR).child(key).update(updated_users_dict[key])


def get_all_tags():
    firebase = Firebase(config)
    db = firebase.database()

    tags_ordered_dict = db.child(TAGS_DIR).get().val()
    tags_dict = dict(tags_ordered_dict)

    list_of_tags = []
    for value in tags_dict.values():
        name = value["Name"]
        try:
            author = value["Author"]
        except:
            author = None
        try:
            creation_date = value["Creation_date"]
        except:
            creation_date = None
        try:
            users = value["Users"]
        except:
            users = None

        list_of_tags.append(tcm.Tag(name, author, creation_date, users))

    return list_of_tags


def get_all_tag_names():
    firebase = Firebase(config)
    db = firebase.database()

    tags_ordered_dict = db.child(TAGS_DIR).get().val()
    tags_dict = dict(tags_ordered_dict)

    list_of_tags = []

    for value in tags_dict.values():
        name = value["Name"]
        list_of_tags.append(name)
    return list_of_tags


# noinspection DuplicatedCode
def delete_all_tags():
    firebase = Firebase(config)
    db = firebase.database()
    db.child(TAGS_DIR).shallow().remove()


def delete_tag(name):
    firebase = Firebase(config)
    db = firebase.database()
    db.child(TAGS_DIR + "/" + name).shallow().remove()


# def find_matching_users(user_id):
#     list_of_all_tags = get_all_tags()
#     # TODO add localization for users to show cross-matches on the map :3


# user centered functions
def delete_all_users():
    firebase = Firebase(config)
    db = firebase.database()
    db.child(USERS_DIR).shallow().remove()


def delete_user(user):
    firebase = Firebase(config)
    db = firebase.database()
    db.child(USERS_DIR + "/" + user).shallow().remove()


def create_users(number_of_users):
    firebase = Firebase(config)
    db = firebase.database()

    list_of_user_ids = []

    users_list = ucm.create_users(number_of_users)

    for user in users_list:
        list_of_user_ids.append(user.user_id)

    users_dict = {}
    for user in users_list:
        users_dict[user.user_id] = user.create_firebase_entry()

    db.child(USERS_DIR).update(users_dict)

    return list_of_user_ids


def check_if_exists(given_user_id):
    firebase = Firebase(config)
    db = firebase.database()

    list_of_existing_users = db.child(USERS_DIR).shallow().get().val()

    for id in list_of_existing_users:
        if id == given_user_id:
            return True
    return False


def update_user_data(given_user_id, data):
    if data is not None:
        if check_if_exists(given_user_id):
            firebase = Firebase(config)
            db = firebase.database()
            db.child(USERS_DIR).child(given_user_id).update(data)


def update_user_coords(given_user_id, data):
    if data is not None:
        if check_if_exists(given_user_id):
            firebase = Firebase(config)
            db = firebase.database()
            db.child(USERS_DIR).child(given_user_id).child('CurrentLocation').update({0: data[0], 1: data[1]})


def get_all_user_ids():
    firebase = Firebase(config)
    db = firebase.database()
    list_of_user_ids = db.child(USERS_DIR).shallow().get().val()
    return list_of_user_ids


def get_all_users(return_type="list"):
    firebase = Firebase(config)
    db = firebase.database()

    if return_type == "list":
        users_ordered_dict = db.child(USERS_DIR).get().val()
        users_list = []
        if users_ordered_dict is not None:
            users_dict = dict(users_ordered_dict)
            for value in users_dict.values():
                users_list.append(value)
        return users_list
    elif return_type == "json":
        return db.child(USERS_DIR).get().val()


def update_all_users(given_json):
    """Takes only json"""
    firebase = Firebase(config)
    db = firebase.database()
    db.child(USERS_DIR).update(given_json)


# print(tcm.mark_random_tags(get_all_tag_names()))

# delete_all_users()

# create_users(10)

# update_user_data("09f36741fc884f80aed60187b415f25c", {"Age": 26, "Name": "Brian", "Surname": "Poopiehead"})

# delete_user("01c6482546f64ebcb4f5271400a93526")

# print(check_if_exists(config, USERS_DIR, "01cd2f24549a4f6a8a2cc4ad553ca413"))

# get_all_users()

# create_tags(20)

# delete_all_tags()

# tags = get_all_tags()

# print(tags)
