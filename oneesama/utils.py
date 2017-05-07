#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from flask import abort

from peewee import DoesNotExist

from .models import *

def get_or_404(model, primary_key):
    try:
        item = model.get(model.id == primary_key)
    except DoesNotExist:
        abort(404)
    return item


def create_admin_user(user="admin", password="admin"):
    admin = User.create(username=user, password="")
    admin.set_password(password)
    admin.save()


def urljoin(base, uri):
    return "/".join([base.rstrip("/"), uri.lstrip("/")])
