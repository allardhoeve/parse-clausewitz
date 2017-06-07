#!/usr/bin/env python
import argparse
from zipfile import ZipFile
from tokenizer import tokenizer

parser = argparse.ArgumentParser(description="Parse Clausewitz save file (EU4)")
parser.add_argument("--file", "-f", dest="file", type=str, default="Sample.eu4")
parser.add_argument("--meta", "-m", dest="meta", action="store_true")

args = parser.parse_args()


with ZipFile(args.file, 'r') as myzip:
    if args.meta:
        data = myzip.read("meta")
        print(" - Meta data length is {} bytes".format(len(data)))
    else:
        data = myzip.read("game.eu4")
        print(" - Game file length is {} bytes".format(len(data)))


tokens = tokenizer(data)


for token in tokens:
    print(" - Found token {}".format(token))