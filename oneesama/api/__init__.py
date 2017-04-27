#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from ..app import app
from ..auth import user_auth
from ..models import models
from .resources import resources

from . import resources, views

from flask_peewee.rest import RestAPI, RestResource

api = RestAPI(app, default_auth=user_auth)

def register_all():
    resource_table = {}
    for resource in resources:
        resource_table[resource.__name__] = resource
    for model in models:
        resource = resource_table.get("{}Resource".format(model.__name__),
                                      RestResource)
        api.register(model, resource)
    api.setup()
