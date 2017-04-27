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

from werkzeug.utils import secure_filename

from flask import jsonify, request, Blueprint

api_views = Blueprint('', __name__)

@api_views.route('/api/file/<int:id>/content', methods=['PUT'])
def put_file(id):
    file_obj = get_or_404(File, id)
    filename = secure_filename(file_obj.path)
    with open("/tmp/{}".format(filename), mode="wb") as file:
        file.write(request.data)
    return jsonify({"success": True})


@api_views.route("/api/playlist/<int:id>/entries")
def show_entries(id):
    entries = PlaylistEntry.select().where(PlaylistEntry.playlist == id)
    return jsonify({
        "playlistentries": [entry.as_dict() for entry in entries],
    })

