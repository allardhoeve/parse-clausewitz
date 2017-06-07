from tokens import *

TOKENS = (MagicNumber, OpenGroup, CloseGroup, Equals, Integer, Boolean, String, Identifier)


def tokenizer(data):
    while data:
        ret = None

        for Token in TOKENS:
            ret = Token.match(data)
            if ret:
                break

        if ret:
            token, rest = ret
            # reset data to be the rest data from previous token
            data = rest
            yield token

        if not ret:
            raise RuntimeError("Could not find token in {} bytes starting with {}".format(len(data), data[0:24]))
