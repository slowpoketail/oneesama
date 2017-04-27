#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from flask import Flask, jsonify, request, abort

from flask_peewee.auth import Auth, BaseUser
from flask_peewee.db import Database
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication

from peewee import (
    TextField, BooleanField, CharField, ForeignKeyField, DoesNotExist
)

from werkzeug.utils import secure_filename

import os.path

import json

# CONFIGURATION

DATABASE = {
    'name': '/tmp/oneesama.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
FILE_DIR = "/tmp"

# APP

app = Flask(__name__)
app.config.from_object(__name__)

# DATABASE

db = Database(app)

# MODELS

def get_or_404(model, id):
    try:
        item = model.get(model.id == id)
    except DoesNotExist:
        abort(404)
    return item


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    admin = BooleanField(default=False)
    active = BooleanField(default=True)


class UserResource(RestResource):
    exclude = ('password')


class File(db.Model):
    path = CharField(default="")

    def prepared(self):
        self.path = os.path.join(
            app.config["FILE_DIR"], "oneesama:file:{}:content".format(self.id))
        self.save()


class FileResource(RestResource):
    exclude = (
        'path',
    )

    def check_put(self, obj):
        """Disallow updates to this resource."""
        return False

    def prepare_data(self, obj, data):
        data['content_uri'] = "/file/{}/content".format(obj.id)
        return data


@app.route('/api/file/<int:id>/content', methods=['PUT'])
def put_file(id):
    file_obj = get_or_404(File, id)
    filename = secure_filename(file_obj.path)
    with open("/tmp/{}".format(filename), mode="wb") as file:
        file.write(request.data)
    return jsonify({"success": True})

class Anime(db.Model):
    name = CharField()
    file = ForeignKeyField(File, related_name='anime')
    watched = BooleanField(default=False)

class AnimeResource(RestResource):
    include_resources = {
        'file': FileResource,
    }


class Playlist(db.Model):
    name = CharField()


class PlaylistResource(RestResource):
    pass


@app.route("/api/playlist/<int:id>/entries")
def show_entries(id):
    entries = PlaylistEntry.select().where(PlaylistEntry.playlist == id)
    return jsonify({
        "playlistentries": [entry.as_dict() for entry in entries],
    })


class PlaylistEntry(db.Model):
    playlist = ForeignKeyField(Playlist, related_name='entries')
    anime = ForeignKeyField(Anime, related_name='playlists')

    def as_dict(self):
        return {
            "playlist": self.playlist.id,
            "anime": self.anime.id,
        }

class PlaylistEntryResource(RestResource):
    include_resources = {
        'playlist': PlaylistResource,
        'anime': AnimeResource,
    }

def create_tables():
    File.create_table()
    Anime.create_table()
    User.create_table()
    Playlist.create_table()
    PlaylistEntry.create_table()


def create_admin_user():
    admin = User.create(username="admin", password="")
    admin.set_password("admin")
    admin.save()


# AUTH


auth = Auth(app, db, user_model=User)
user_auth = UserAuthentication(auth)

# API

api = RestAPI(app, default_auth=user_auth)

api.register(File, FileResource)
api.register(Anime, AnimeResource)
api.register(Playlist)
api.register(PlaylistEntry)
api.register(User, UserResource)

api.setup()

# MAIN


def main():
    app.run()
