#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from imouto import *
from flask_testing import LiveServerTestCase
from flask import Flask
from oneesama import config
from oneesama.utils import urljoin

import pytest
import requests


def create_app(self):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["TESTING"] = True
    app.config["DATABASE"] = {
        "name": "/tmp/oneesama.db",
        "engine": "peewee.SqliteDatabase",
    }
    #app.config["LIVESERVER_PORT"] = 0
    return app


class TestFile(LiveServerTestCase):

    create_app = create_app

    def test_create(self):
        f = File.create()
        assert hasattr(f, "id")
        assert hasattr(f, "content_uri")
        assert requests.get(f.uri).status_code == 200
        assert f.content_uri == "/file/{}/content".format(f.id)

    def test_unique(self):
        f1 = File.create()
        f2 = File.create()
        assert f1.id != f2.id

    def test_delete(self):
        f = File.create()
        f.delete()
        assert requests.get(f.uri).status_code == 404
