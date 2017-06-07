import re

# http://eu4parser.readthedocs.io/en/latest/format/


class Token(object):
    value = None
    pattern = None
    length = None

    string_format = "{0.name}: {0.value}"

    def __init__(self, value, length):
        self.value = value
        self.length = length

    @classmethod
    def match(cls, data):
        """
        :param `bytes` data: the data to match our pattern to
        # :rtype: tuple(Token, `bytes`)
        :rtype: tuple(`re.MatchObject`, `bytes`)
        """
        ret = re.match(cls.pattern, data)
        if ret:
            start, end = ret.span()
            rest = data[end:]
            return cls(ret.group(), end), rest

    @property
    def name(self):
        return self.__class__.__name__

    @staticmethod
    def _to_int(value):
        return int.from_bytes(value, byteorder='little', signed=True)

    def __repr__(self):
        return "<{0.name} length {0.length}: {0.value}>".format(self)

    def __str__(self):
        return self.string_format.format(self)


class MagicNumber(Token):
    value = "EU4bin"
    pattern = b'\x45\x55\x34\x62\x69\x6e'


class OpenGroup(Token):
    pattern = b'\x03\x00'
    string_format = "{0.name}"


class CloseGroup(Token):
    pattern = b'\x04\x00'
    string_format = "{0.name}"


class Equals(Token):
    pattern = b'\x01\x00'
    string_format = "{0.name}"


class Integer(Token):
    pattern = b'(\x0c\x00|\x14\x00)'

    @classmethod
    def match(cls, data):
        ret = re.match(cls.pattern, data)

        if ret:
            value = cls._to_int(data[2:6])
            length = 6
            rest = data[6:]
            return cls(value, length), rest


class Boolean(Token):
    pattern = b'\x0e\x00.'

    def __init__(self, value, length):
        super(Boolean, self).__init__(value, length)
        self.value = value[2:] != b'\x00'


class FixedBoolean(Boolean):
    pattern = b'(\x4b\x28|\x4c\x28)'

    def __init__(self, value, length):
        super(Boolean, self).__init__(value, length)
        self.value = True if value == b'\x4b\x28' else False


class Identifier(Token):
    pattern = b'..'

    def __init__(self, value, length):
        super(Identifier, self).__init__(value, length)
        self.value = self.value.hex().upper()


class String(Token):
    pattern = b'(\x0f\x00|\x17\x00)'

    @classmethod
    def match(cls, data):
        ret = re.match(cls.pattern, data)

        if ret:
            string_length = cls._to_int(data[2:4])
            string = data[4:string_length+4].decode('cp1252')
            length = string_length + 4
            rest = data[length:]
            return cls(string, length), rest


class Float(Integer):
    pattern = b'\x0d\x00'

    def __init__(self, value, length):
        super(Float, self).__init__(value, length)
        self.value /= 1000


class Q16Float(Token):
    pattern = b'\x67\x01'

    @classmethod
    def match(cls, data):
        ret = re.match(cls.pattern, data)

        if ret:
            length = 10
            rest = data[length:]
            value = data[2:6]  # final four have an unknown meaning
            value = cls._to_int(value) * (2 ** -16)
            return cls(value, length), rest