from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField, PasswordField, IntegerField, DateField

import firebase


class Replacement:
    def __init__(self, target="", location="1A1", day="01-01-1970", hour="1", replacer="", flags=""):
        self.target = target
        self.location = location
        self.day = day
        self.hour = hour
        self.replacer = replacer
        self.flags = flags


class PosterForm(Form):
    email = StringField("Email:", validators=[validators.required(), validators.email()])
    password = PasswordField("Password:", validators=[validators.required(), validators])

    target = StringField("Sostituto:", validators=[validators.required()])
    location = StringField("Classe:", validators=[validators.required(), validators.regexp("[1-5][a-f][1-5]?")])
    day = DateField("Giorno:", validators=[validators.required()])
    hour = IntegerField("Ora:", validators=[validators.required(), validators.regexp("[1-5]")])
    replacer = StringField("Sostituente:", validators=[validators.required()])
    flags = StringField("Annotazioni:", validators=[validators.regexp("[QLSRAUqlsrau]+")])


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '74d41f27d661f11567a4abf2b6176d'


@app.route("/postit", methods=["POST"])
def post():
    login_result = firebase.login(request.form["email"], request.form["password"])
    if login_result == 0:
        replacement = Replacement(
            request.form["target"],
            request.form["location"],
            request.form["day"],
            request.form["hour"],
            request.form["replacer"],
            request.form["flags"]
        )

        firebase.database_push(replacement)
        flash("Sostituzione pubblicata")
    else:
        flash("Errore: email o password errati")
    return render_template("index.html", form=PosterForm(request.form))


@app.route("/fetch", methods=["GET"])
def fetch():
    if 'date' in request.args:
        return firebase.download_database(request.args['date'])
    else:
        return '{}'


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", form=PosterForm(request.form))


if __name__ == "__main":
    app.run()
