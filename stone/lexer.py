#! -*- coding:utf-8 -*-
import re
from stone.token import Token, NumToken, StrToken, IdToken
from stone.reader import LineReader


class Lexer(object):
    regex_pat = r'''
    \s*(                        #空白
    (//.*)|                     #注释
    (\d+)|                      #数字类型
    ("[^"]*")|                  #字符串类型
    [A-Z_a-z][A-z_a-z0-9]*|     #标识符
    ==|<=|>=|&&|\|\||           #符号
    [\+\-\*/\{\}\=\|\&\[\]\(\)\<\>\;]            #符号
    )
    '''
    def __init__(self,f):
        self.has_more = True
        self.reader = LineReader(f)
        self.line_no = 0
        self.queue = []
        self.pattern = re.compile(self.regex_pat, re.X)

    def read(self):
        if self.fill_queue(0):
            return self.queue.pop(0)
        return Token.EOF

    def peek(self, i):
        if self.fill_queue(i):
            return self.queue[i]
        return Token.EOF

    def fill_queue(self, i):
        while i >= len(self.queue):
            if self.has_more:
                self.read_line()
            else:
                return False
        return True

    def read_line(self):
        line = self.reader.read()
        line = line[:-1]
        if not line :
            self.has_more = False
            return
        self.line_no = self.reader.line_no
        start = 0
        end = len(line)
        while start < end:
            matcher = self.pattern.search(line[start:end])
            start += matcher.end()
            if matcher:
                self.add_token(matcher)
        self.queue.append(IdToken(self.line_no,Token.EOL))

    def add_token(self, matcher):
        m = matcher.group(1)
        if m != None:        #not a space line
            if matcher.group(2) == None:    #not a comment
                if matcher.group(3) != None:
                    token = NumToken(self.line_no, int(m))
                elif matcher.group(4) != None:
                    token = StrToken(self.line_no, m)
                else:
                    token = IdToken(self.line_no, m)
                self.queue.append(token)
