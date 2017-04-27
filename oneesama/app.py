#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from flask import Flask

DATABASE = {
    'name': '/tmp/oneesama.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
FILE_DIR = "/tmp"

app = Flask(__name__)
app.config.from_object(__name__)
