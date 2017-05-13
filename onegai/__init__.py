#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oneesama - a video playback server
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import plac

from imouto import *

import logging
import sys

from requests.auth import HTTPBasicAuth

default_oneesama_url = "http://localhost:5000/api"
default_auth = HTTPBasicAuth("admin", "admin")

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
log_formatter = logging.Formatter('[%(asctime)s] %(message)s')
stdout_handler.setFormatter(log_formatter)
logger.addHandler(stdout_handler)


class Onegai:
    commands = (
        'anime',
    )

    def __init__(self,
                 debug: ("enable debug output", "flag", "d"),
                 ):
        if debug:
            logger.setLevel(logging.DEBUG)
        logger.debug("debug output enabled")

    def anime(self, command, *args):
        arglist = [command]
        arglist.extend(args)
        plac.Interpreter.call(AnimeDispatcher, arglist=arglist)


class AnimeDispatcher:
    commands = (
        "add",
        "list",
    )

    def add(self, name, path):
        print("adding '{}' to database".format(name))
        f = File.create()
        logger.debug("new file: {}".format(f))
        f.upload(path)
        a = Anime.create(name, f.id)
        logger.debug("new anime: {}".format(a))

    def list(self):
        for anime in Anime.list():
            print("[{}] {}".format(anime.id, anime.name))


def main():
    plac.Interpreter.call(Onegai)

if __name__ == "__main__":
    main()
