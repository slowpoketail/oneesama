#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from .models import User
from .app import app
from .db import db

from flask_peewee.auth import Auth
from flask_peewee.rest import UserAuthentication

auth = Auth(app, db, user_model=User)
user_auth = UserAuthentication(auth)
