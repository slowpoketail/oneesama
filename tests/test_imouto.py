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

def check_status(url):
    return requests.get(url).status_code


class TestFile(LiveServerTestCase):

    create_app = create_app

    def test_create(self):
        f = File.create()
        assert hasattr(f, "id")
        assert hasattr(f, "content_uri")
        assert check_status(f.uri) == 200
        assert f.content_uri == "/file/{}/content".format(f.id)

    def test_unique(self):
        f1 = File.create()
        f2 = File.create()
        assert f1.id != f2.id

    def test_delete(self):
        f = File.create()
        f.delete()
        assert check_status(f.uri) == 404

    def test_upload(self):
        f = File.create()
        f.upload("test.mkv")

class TestAnime(LiveServerTestCase):

    create_app = create_app

    def test_create(self):
        f = File.create()
        a = Anime.create(name="foo", file_id=f.id)
        assert hasattr(a, "id")
        assert hasattr(a, "name")
        assert hasattr(a, "file")
        assert check_status(a.uri) == 200
        assert a.name == "foo"
        assert a.file == f.id

    def test_unique(self):
        f = File.create()
        a1 = Anime.create(name="foo", file_id=f.id)
        a2 = Anime.create(name="bar", file_id=f.id)
        assert a1.id != a2.id

    def test_update(self):
        f1 = File.create()
        a = Anime.create(name="foo", file_id=f1.id)
        a.name = "bar"
        assert a.name == "bar"
        f2 = File.create()
        a.file = f2.id
        assert a.file == f2.id

    def test_delete(self):
        f = File.create()
        a = Anime.create(name="foo", file_id=f.id)
        a.delete()
        assert check_status(a.uri) == 404
