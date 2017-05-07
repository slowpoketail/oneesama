#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from oneesama.utils import urljoin

import requests
from requests import get, post, put, delete
from requests.auth import HTTPBasicAuth

import json

from abc import ABC, abstractmethod

from functools import reduce

default_auth = HTTPBasicAuth("admin", "admin")

json_headers = {"Content-Type": "application/json"}
json_empty = json.dumps({})

BASE_URL = "http://localhost:5000/api/"


class BaseResource(ABC):

    base_url = BASE_URL

    uri = property(lambda self: urljoin(self.resource_url, str(self._id)))

    id = property(lambda self: self._id)

    @abstractmethod
    def __init__(self):
        return NotImplemented

    @classmethod
    def _request(cls, method, uri="", data=json_empty):
        uri = "/{}/".format(str(uri))
        url = urljoin(cls.resource_url, uri)
        r = method(url, auth=default_auth, headers=json_headers, data=data)
        r.raise_for_status()
        if not r.json:
            raise AttributeError("no JSON in reply")
        return r.json()

    @classmethod
    def list(cls):
        return cls._request(get)

    @classmethod
    @abstractmethod
    def create(cls):
        data = cls._request(post)
        return cls(data)

    def delete(self):
        return self._request(delete, uri=self.id)


class File(BaseResource):

    resource_name = "/file/"
    resource_url = urljoin(BASE_URL, resource_name)

    content_uri = property(lambda self: self._content_uri)

    def __init__(self, id, content_uri):
        self._id = id
        self._content_uri = content_uri

    @classmethod
    def create(cls):
        data = cls._request(post)
        id = data["id"]
        return cls(data["id"], data["content_uri"])

    def upload(self, path):
        url = urljoin(self.base_url, self.content_uri)
        f = open(path, 'rb')
        r = put(url, data=f, auth=default_auth)
        r.raise_for_status()
