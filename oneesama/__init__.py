#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from .app import app
from .api.views import api_views

#api = get_api(app)
from .api import register_all
from .api.resources import resources

app.register_blueprint(api_views)
register_all()

def main():
    app.run()
