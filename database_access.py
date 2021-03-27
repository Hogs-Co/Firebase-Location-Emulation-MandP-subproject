from firebase import Firebase
import user_creation_and_manipulation as ucam
import time
import uuid

# User data:
# 'User_ID' string
# 'Name' string
# 'Surname' string
# 'Email' string which must be compliant with ucam.User.check_email()
# 'Birth date' in a date format - passed to firebase as string
# 'Age': int - amount of years from birth date to today
# 'Current localization': two argument list - [longitude, latitude]
# 'Current used tags': list of maximum 4 custom tags and 2 age tags


# consts
USERS_DIR = "users"


# firebase project identifier: fir-test-env-mandp
# firebase table identifier: fir-test-env-mandp-default-rtdb
# firebase link: https://fir-test-env-mandp-default-rtdb.firebaseio.com/

config = {
  "apiKey": "AAAA3KmrBPQ:APA91bFqfELPwbuc7gAS1FkgCland5wKUAEZpEaYUmLdjdjr-rUVF1zBp_5JKHY_TxbsT6ROtiRy28gCd2pEPmHkawl2b"
            "-ow1H2rkOCknJ6b3npX09_flYlFZnQI1O5R0F-EC_PoJw1D",
  "authDomain": "fir-test-env-mandp.firebaseapp.com",
  "databaseURL": "https://fir-test-env-mandp-default-rtdb.firebaseio.com",
  "storageBucket": "fir-test-env-mandp.appspot.com"
  # optional - overrides security rules
  # "serviceAccount": "fir-test-env-mandp-firebase-adminsdk-kswac-032b264225.json"
}


def delete_all_users(given_config, users_directory):
    firebase = Firebase(given_config)
    db = firebase.database()
    db.child(users_directory).shallow().remove()


def create_users(given_config, users_directory, number_of_users):
    firebase = Firebase(given_config)
    db = firebase.database()

    list_of_user_ids = []

    for user in ucam.create_users(number_of_users):
        db.child(users_directory).child(user.user_id).set(user.create_firebase_entry())
        list_of_user_ids.append(user.user_id)
    return list_of_user_ids


def update_user_data(given_config, users_directory, user_id, **data):
    firebase = Firebase(given_config)
    db = firebase.database()
    db.child(users_directory).child(user_id).update(data)


update_user_data(config, USERS_DIR, "01c6482546f64ebcb4f5271400a93526", Name="Richard", Surname="Vagina")
