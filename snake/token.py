#! -*- utf-8 -*-

import re

class Token(object):

    TOKEN_NUM = 0
    TOKEN_ID = 1
    TOKEN_STR = 2

    def __init__(self, line):
        self.line_number = line

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.text())

    def text(self):
        return str(self.value)

    def get_line_number(self):
        return self.line_number

    def __str__(self):
        return str(self.value)

Token.EOF = Token(-1)
Token.EOL = "\n"


class NumToken(Token):

    def __init__(self, line, v):
        super(NumToken, self).__init__(line)
        self.value = v
        self.type = Token.TOKEN_NUM

    def get_number(self):
        if re.match('\d+', str(self.value)):
            return int(self.value)
        elif re.match('^\d+\.\d+$', str(self.value)):
            return float(self.value)


class IdToken(Token):

    def __init__(self, line, i):
        super(IdToken, self).__init__(line)
        self.value = i
        self.type = Token.TOKEN_ID


class StrToken(Token):

    def __init__(self, line, i):
        super(StrToken, self).__init__(line)
        self.value = i
        self.type = Token.TOKEN_STR
