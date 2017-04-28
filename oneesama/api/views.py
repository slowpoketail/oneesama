#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from ..utils import *

from ..models import *

from .. import config

from flask import jsonify, request, Blueprint
import os.path

api_views = Blueprint('', __name__)

@api_views.route('/api/file/<int:id>/content', methods=['PUT'])
def put_file(id):
    filename = os.path.join(config.FILE_DIR,
                            "oneesama:file:{}:content".format(id))
    with open(filename, mode="wb") as file:
        file.write(request.data)
    return jsonify({"success": True})


@api_views.route("/api/playlist/<int:id>/entries")
def show_entries(id):
    entries = PlaylistEntry.select().where(PlaylistEntry.playlist == id)
    return jsonify({
        "playlistentries": [entry.as_dict() for entry in entries],
    })

