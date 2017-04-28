#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from ..models import *

from flask_peewee.rest import RestResource

import sys

class FileResource(RestResource):
    exclude = (
        'path',
    )

    def prepare_data(self, obj, data):
        data["content_uri"] = "/file/{}/content".format(obj.id)
        return data


class AnimeResource(RestResource):
    include_resources = {
        'file': FileResource,
    }


class PlaylistResource(RestResource):
    pass


class PlaylistEntryResource(RestResource):
    include_resources = {
        'playlist': PlaylistResource,
        'anime': AnimeResource,
    }


class UserResource(RestResource):
    exclude = ('password')


resources = (
    FileResource,
    AnimeResource,
    PlaylistResource,
    PlaylistEntryResource,
    UserResource,
)

__all__ = [resource.__name__ for resource in resources]
