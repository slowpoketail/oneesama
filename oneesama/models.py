#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import sys
import os.path

from .app import app
from .db import db

from peewee import (
    TextField,
    BooleanField,
    CharField,
    ForeignKeyField,
)
from flask_peewee.auth import BaseUser

class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    admin = BooleanField(default=False)
    active = BooleanField(default=True)


class File(db.Model):
    path = CharField(default="")

    def prepared(self):
        self.path = os.path.join(
            app.config["FILE_DIR"], "oneesama:file:{}:content".format(self.id))
        self.save()


class Anime(db.Model):
    name = CharField()
    file = ForeignKeyField(File, related_name='anime')
    watched = BooleanField(default=False)


class Playlist(db.Model):
    name = CharField()


class PlaylistEntry(db.Model):
    playlist = ForeignKeyField(Playlist, related_name='entries')
    anime = ForeignKeyField(Anime, related_name='playlists')

    def as_dict(self):
        return {
            "playlist": self.playlist.id,
            "anime": self.anime.id,
        }


models = (
    User,
    File,
    Anime,
    Playlist,
    PlaylistEntry,
)

__all__ = [model.__name__ for model in models]

def create_tables():
    for model in models:
        model.create_tables()


