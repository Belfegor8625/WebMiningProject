import pyrebase

config = {"apiKey": "AIzaSyA167rqXj93fAxq-xDvrIGL0TuZC8_7arY ", "authDomain": "webmining-20102.firebaseapp.com",
          "databaseURL": "https://webmining-20102.firebaseio.com",
          "storageBucket": "webmining-20102.appspot.com",
          "serviceAccount": "WebMining-204af128f7f6.json"}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()  # authenticate a user user = auth.sign_in_with_email_and_password("william@hackbrightacademy.com", "mySuperStrongPassword")
user = auth.sign_in_with_email_and_password("bartekdudu@gmail.com", "baraschmulew")
db = firebase.database()


def add_graph_to_database(graph):
    for key, values in graph.items():
        site = {"subsites": values}
        new_key = prepare_key(key)
        db.child("graph").child(new_key).set(site, user['idToken'])


def add_page_rang_to_db(page_rank):
    db.child("pageRank").set(page_rank, user['idToken'])


def prepare_key(key):
    new_key = key.replace('/', '\\')
    new_key = new_key.replace('.', ' ')
    return new_key


# add data
# db.child("agents").child("Lana").set(lana, user['idToken'])

# TODO: utworzyć schemat danych
def remove_graph():
    db.child('graph').remove(user['idToken'])


# remove data
# db.child("agents").child("Lana").remove(user['idToken'])

def add_site_text_to_db(url, text):
    db.child("search_db").child(prepare_key(url)).child("text").set(text, user['idToken'])


def add_site_img_to_db(url, imgs):
    encoded = []
    for img in imgs:
        encoded.append(img.decode('utf-8'))
    db.child("search_db").child(prepare_key(url)).child("imgs").set(encoded, user['idToken'])


def add_site_links_to_db(url, links):
    encoded = []
    for link in links:
        encoded.append(link.decode('utf-8'))
    db.child("search_db").child(prepare_key(url)).child("links").set(encoded, user['idToken'])


def add_site_scripts_to_db(url, scripts):
    encoded = []
    for script in scripts:
        encoded.append(script.decode('utf-8'))
    db.child("search_db").child(prepare_key(url)).child("scripts").set(encoded, user['idToken'])
