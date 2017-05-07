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
import os.path

from tempfile import mkdtemp

def create_app(self):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["TESTING"] = True
    app.config["TEST_DIR"] = mkdtemp(prefix="oneesama-test:")
    app.config["DATABASE"] = {
        "name": os.path.join(app.config["TEST_DIR"], "oneesama.db"),
        "engine": "peewee.SqliteDatabase",
    }
    #app.config["LIVESERVER_PORT"] = 0
    return app

class TestAPI(LiveServerTestCase):

    create_app = create_app


    def test_create(self):
        #File.base_url = urljoin(self.get_server_url(), "/api/")
        f = File.create()
        assert hasattr(f, "id")
        assert hasattr(f, "content_uri")
        a = Anime.create(name="foo", file_id=f.id)
        assert hasattr(a, "id")
        assert hasattr(a, "name")
        assert hasattr(a, "file")

