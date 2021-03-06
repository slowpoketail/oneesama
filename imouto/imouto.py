#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from oneesama.utils import urljoin

from requests import get, post, put, delete
from requests.auth import HTTPBasicAuth

import json

from abc import ABC, abstractmethod

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
        pass

    @abstractmethod
    def update(self):
        return NotImplemented

    @classmethod
    def _request(cls, method, uri="", data=None, query=""):
        json_data = json.dumps(data) if data else json_empty
        uri = "/{}/".format(str(uri))
        url = urljoin(cls.resource_url, uri)
        url = urljoin(url, query)
        r = method(url, auth=default_auth, headers=json_headers, data=json_data)
        r.raise_for_status()
        if not r.json:
            raise AttributeError("no JSON in reply")
        return r.json()

    @classmethod
    def list(cls):
        reply = cls._request(get)
        meta = reply["meta"]
        objects = reply["objects"]
        while meta["next"]:
            next_page_query = meta["next"].split("/")[-1]
            next_page_reply = cls._request(get, query=next_page_query)
            objects.extend(next_page_reply["objects"])
            meta = next_page_reply["meta"]
        return [cls.from_dict(obj) for obj in objects]

    @classmethod
    @abstractmethod
    def create(cls):
        data = cls._request(post)
        return cls(data)

    def delete(self):
        return self._request(delete, uri=self.id)

    def _get(self):
        return self._request(get, uri=self.id)

    def _put(self, data):
        return self._request(put, uri=self.id, data=data)

    @classmethod
    def get(cls, id):
        return cls._request(get, uri=id)

    @classmethod
    def from_dict(cls, d):
        return NotImplemented


class File(BaseResource):

    resource_name = "/file/"
    resource_url = urljoin(BASE_URL, resource_name)

    content_uri = property(lambda self: self._content_uri)

    def __init__(self, id, content_uri):
        self._id = id
        self._content_uri = content_uri

    def update(self):
        data = self._get()
        self._content_uri = data["content_uri"]

    @classmethod
    def create(cls):
        data = cls._request(post)
        return cls(data["id"], data["content_uri"])

    def upload(self, path):
        url = urljoin(self.base_url, self.content_uri)
        f = open(path, 'rb')
        r = put(url, data=f, auth=default_auth)
        r.raise_for_status()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, str({
            "id": self.id,
            "content_uri": self.content_uri,
        }))


class Anime(BaseResource):

    resource_name = "/anime/"
    resource_url = urljoin(BASE_URL, resource_name)

    def __init__(self, id, name, file_id):
        self._id = id
        self._name = name
        self._file_id = file_id

    def update(self):
        data = self._get()
        self._name = data["name"]
        self._file_id = data["file"]["id"]

    @classmethod
    def create(cls, name, file_id):
        data = {"name": name, "file": file_id}
        reply = cls._request(post, data=data)
        return cls(reply["id"], reply["name"], reply["file"])

    @classmethod
    def from_dict(cls, d):
        id = d.get("id")
        assert id
        name = d.get("name")
        assert name
        file_id = d.get("file")
        assert file_id
        return cls(id, name, file_id)

    @property
    def name(self):
        self.update()
        return self._name

    @name.setter
    def name(self, name):
        data = {"name": name}
        self._put(data)
        self._name = name

    @property
    def file(self):
        self.update()
        return self._file_id

    @file.setter
    def file(self, file_id):
        data = {"file": file_id}
        self._put(data)
        self._file_id = file_id

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, str({
            "id": self.id,
            "name": self.name,
            "file": self.file,
        }))
