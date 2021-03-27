from firebase import Firebase
import user_creation_and_manipulation as ucam
import time
import uuid

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

# firebase_dblink connection establish
firebase = Firebase(config)
db = firebase.database()

db.child(USERS_DIR).shallow().remove()

list_of_created_users = ucam.create_users(100)

for user in list_of_created_users:
    db.child(USERS_DIR).child(str(user.user_id)).set(user.create_firebase_entry())


