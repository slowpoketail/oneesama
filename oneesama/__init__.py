#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from flask import Flask, jsonify, request

from flask_peewee.auth import Auth, BaseUser
from flask_peewee.db import Database
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication

from peewee import TextField, BooleanField, CharField

from flask_uploads import UploadSet

from werkzeug.utils import secure_filename

# CONFIGURATION

DATABASE = {
    'name': '/tmp/oneesama.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True

# APP

app = Flask(__name__)
app.config.from_object(__name__)

# DATABASE

db = Database(app)

# FILES
anime = UploadSet('anime', extensions=["mkv"])

@app.route('/api/upload/<filename>', methods=['POST'])
def upload(filename):
    filename = secure_filename(filename)
    with open("/tmp/{}".format(filename), mode="wb") as file:
        file.write(request.data)
    return jsonify({"success": True, "filename": filename})

# MODELS

class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    admin = BooleanField(default=False)
    active = BooleanField(default=True)

class UserResource(RestResource):
    exclude = ('password')

class Anime(db.Model):
    name = TextField()
    path = TextField()
    watched = BooleanField(default=False)

def create_tables():
    Anime.create_table()
    User.create_table()

# AUTH

auth = Auth(app, db, user_model = User)
user_auth = UserAuthentication(auth)

# API

api = RestAPI(app, default_auth=user_auth)

api.register(Anime)
api.register(User, UserResource)

api.setup()

# MAIN

def main():
    app.run()
