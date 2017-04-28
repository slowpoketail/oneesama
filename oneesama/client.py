#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import requests
import json

from urllib.request import quote

json_headers = {"Content-Type": "application/json"}
json_empty = json.dumps({})

class Client:
    '''A client for the oneesama server.

    Applications can use this to control oneesama.
    '''
    def __init__(self, base_url, auth):
        self._base_url = base_url
        self._auth = auth

    def _create_resource(self, name, data=json_empty):
        r = requests.post(self.full_url(name), auth=self._auth,
                          headers=json_headers, data=data)
        r.raise_for_status()
        if not r.json:
            raise ValueError("no JSON in reply")
        return r.json()

    def _get(self, uri):
        url = self.full_url(uri)
        r = requests.get(url, auth=self._auth)
        r.raise_for_status()
        if not r.json:
            raise ValueError('no JSON in reply')
        return r.json()

    def query(self, uri, column, value):
        value = quote(value)
        query_uri = "{}?{}={}".format(uri, column, value)
        return self._get(query_uri)

    def full_url(self, resource=""):
        '''Return the the full URL of a resource.

        A resource URI should always start with a /.
        '''
        return "".join((self._base_url, resource))

    def create_file_resource(self):
        '''Create a file resource on the server.

        Returns the file object as a dictionary.
        '''
        return self._create_resource('/file/')

    def create_anime_resource(self, name, file_id):
        '''Create an anime resource on the server.

        Returns the anime object as a dictionary.
        '''
        data = json.dumps({
            "name": name,
            "file": file_id,
        })
        return self._create_resource('/anime/', data)

    def get_anime_by_id(self, id):
        return self._get("/anime/{}/".format(id))

    def get_anime_by_name(self, name):
        name = quote(name)
        objects = self._get("/anime/?name={}".format(name))['objects']
        assert len(objects) == 1
        return objects[0]

    def put_file(self, path, uri):
        with open(path, mode="rb") as file:
            r = requests.put(self.full_url(uri),
                             auth=self._auth, data=file)
            r.raise_for_status()
            if not r.json:
                raise ValueError("no JSON in reply")
            return r.json()
