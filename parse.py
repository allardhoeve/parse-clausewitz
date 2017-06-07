#!/usr/bin/env python
from zipfile import ZipFile

from tokenizer import tokenizer

with ZipFile('Tall.eu4', 'r') as myzip:
    data = myzip.read("meta")


print(" - Gamefile length is {} bytes".format(len(data)))


tokens = tokenizer(data)

for token in tokens:
    print(" - Found token {}".format(token))