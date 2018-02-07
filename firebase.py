import json
import os

import pyrebase
from requests import HTTPError

API_KEY = os.environ['SNAKE_API_KEY']

"""
  Database structure
  
  poster
   |- lun
   |  |- target
   |  |  |- 1
   |  |  |  |- location
   |  |  |  |- replacer
   |  |  |  \- flags
   |  |  |- 2
   |  |     |- location
   |  |     |- replacer
   |  |     \- flags
   |  |  |- 3 [...]
   |  |  |- 4 [...]
   |  |  \- 5 [...]
   |  |- target 2 [...]
   |  |- [...]
   |  \- target X [...]
   |- mar [...]
   |- mer [...]
   |- gio [...]
   |- ven [...]
   \- sab [...]  

"""


def get_child(db, day_path: []):
    return db.child("poster") \
        .child(day_path[0]) \
        .child(day_path[1]) \
        .child(day_path[2])


def exists(child):
    return child.get().val() is not None


def database_push(item):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return

    config = {
        "apiKey": API_KEY,
        "authDomain": "liceobold.firebaseapp.com",
        "databaseURL": "https://liceobold.firebaseio.com/",
        "storageBucket": "liceobold.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    data = {
        "flags": item.flags,
        "hour": item.hour,
        "location": item.location,
        "replacer": item.replacer,
    }

    if item.target is "" or item.day is "":
        return

    day_path = item.day.split("-")

    # Push
    print("Creating /poster/{}/{}/{}...".format(item.day.replace("-", "/"), item.target, "ora-" + str(item.hour)))
    get_child(db, day_path) \
        .child(item.target) \
        .child("ora-" + str(item.hour)) \
        .set(data)


def download_database(day: str):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return "1"

    config = {
        "apiKey": API_KEY,
        "authDomain": "liceobold.firebaseapp.com",
        "databaseURL": "https://liceobold.firebaseio.com/",
        "storageBucket": "liceobold.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    day_path = day.split("-")
    shallow_child = get_child(db, day_path).shallow()

    if not exists(shallow_child):
        return "{}"

    result = json.dumps(get_child(db, day_path).get().val(), indent=2)
    return str(result)


def login(email: str, password: str):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return 2

    config = {
        "apiKey": API_KEY,
        "authDomain": "liceobold.firebaseapp.com",
        "databaseURL": "https://liceobold.firebaseio.com/",
        "storageBucket": "liceobold.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except HTTPError:
        return 1
    else:
        token = user["idToken"]
        registered = user["registered"]
        if registered is False or token is None or token is "":
            return 3
        else:
            return 0
