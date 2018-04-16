import pyrebase

config = {"apiKey": "AIzaSyA167rqXj93fAxq-xDvrIGL0TuZC8_7arY ", "authDomain": "webmining-20102.firebaseapp.com",
          "databaseURL": "https://webmining-20102.firebaseio.com", "storageBucket": "webmining-20102.appspot.com",
          "serviceAccount": "WebMining-204af128f7f6.json"}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()  # authenticate a user user = auth.sign_in_with_email_and_password("william@hackbrightacademy.com", "mySuperStrongPassword")
user = auth.sign_in_with_email_and_password("bartekdudu@gmail.com", "baraschmulew")

db = firebase.database()
lana = {"name": "Lana Kane", "agency": "Figgis Agency"}
db.child("agents").child("Lana").set(lana, user['idToken'])

#TODO: utworzyć schemat danych
