#!/usr/bin/python

import argparse
from argparse import ArgumentParser
import json
from urllib import parse

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import (
    SpotifyClientCredentials,
    SpotifyOAuth,
)

from readers import Reader, SpotifyReader, FileReader
from writers import Writer, SpotifyWriter, FileWriter
from objects import *

load_dotenv()

scope = "user-library-modify user-read-private"

from sys import stdin, stdout, stderr


def init_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", dest="src", default="stdin", type=str)
    parser.add_argument("-d", "--dest", dest="dest", default="stdout", type=str)
    parser.add_argument(
        "--tracks", dest="type", action="store_const", const="tracks", default=None
    )
    parser.add_argument(
        "--albums", dest="type", action="store_const", const="albums", default=None
    )
    return parser


if __name__ == "__main__":
    argparser = init_parser()
    args = argparser.parse_args()

    reader: Reader = Reader.get_reader(args.src)
    objects = reader.read_objects(args.type)
    writer: Writer = Writer.get_writer(args.dest)
    writer.write_objects(args.type, objects)

    exit(0)
