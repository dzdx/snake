#! -*- utf-8 -*-
class Token(object):

    TOKEN_NUM = 0
    TOKEN_ID  = 1
    TOKEN_STR = 2

    def __init__(self,line):
        self.lineNumber = line

    def __repr__(self):
        return '<%s %s>'%(self.__class__.__name__, self.text())

    def text(self):
        return ''

Token.EOF = Token(-1)
Token.EOL = "\n"

class NumToken(Token):
    def __init__(self, line, v):
        super(NumToken, self).__init__(line)
        self.value = v
        self.type = Token.TOKEN_NUM

    def text(self):
        return str(self.value)

class IdToken(Token):
    def __init__(self, line, i):
        super(IdToken, self).__init__(line)
        self.value = i
        self.type = Token.TOKEN_ID

    def text(self):
        return self.value

class StrToken(Token):
    def __init__(self, line, i):
        super(StrToken, self).__init__(line)
        self.value = i
        self.type = Token.TOKEN_STR

    def text(self):
        return self.value

