#! -*- coding:utf-8 -*-
import re
from snake.exception import ParseException
from snake.token import Token, NumToken, StrToken, IdToken
from snake.reader import LineReader
from abc import ABCMeta, abstractmethod


class Lexer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def peek(self, i):
        pass


class ReLexer(Lexer):
    regex_pat = r'''
    \s*(                                        #空白
    (//.*)|                                     #注释
    (\d+)|                                      #数字类型
    ("[^"]*")|                                  #字符串类型
    [A-Z_a-z][A-z_a-z0-9]*|                     #标识符
    ==|<=|>=|&&|\|\||                           #符号
    [\+\-\*/\{\}\=\|\&\[\]\(\)\<\>\;\%]           #符号
    )
    '''


    def __init__(self, f):
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
        if not line:
            self.has_more = False
            return
        line = line[:-1]

        self.line_no = self.reader.line_no
        start = 0
        end = len(line)
        while start < end:
            matcher = self.pattern.search(line[start:end])
            start += matcher.end()
            if matcher:
                self.add_token(matcher)
        self.queue.append(IdToken(self.line_no, Token.EOL))

    def add_token(self, matcher):
        m = matcher.group(1)
        if m is not None:  # not a space line
            if matcher.group(2) == None:  # not a comment
                if matcher.group(3) != None:
                    token = NumToken(self.line_no, int(m))
                elif matcher.group(4) != None:
                    token = StrToken(self.line_no, m)
                else:
                    token = IdToken(self.line_no, m)
                self.queue.append(token)


class AutomatonLexer(Lexer):
    def __init__(self, f):
        self.reader = LineReader(f)
        self.state = 1
        self.queue = []
        self.word_buffer = ""
        self.last_char = ""

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
            token = self.add_token()
            if token != Token.EOF:
                self.queue.append(token)
            else:
                return False
        return True


    def add_token(self):
        if self.last_char == "":
            char = self.reader.read_char()
        else:
            char = self.last_char
        self.word_buffer = char
        while True:
            if char == "":
                return Token.EOF
            has_token = getattr(self, "state%s" % self.state)(char)
            if not 1 <= self.state <= 10:
                raise ParseException("%s行词法分析失败" % self.reader.line_no)

            if has_token:
                if self.state in (2,):
                    token = NumToken(self.reader.line_no, self.word_buffer)
                elif self.state in (12,):
                    token = StrToken(self.reader.line_no, self.word_buffer)
                elif self.state in (3, 4, 5, 6, 7, 8, 9, 10,):
                    token = IdToken(self.reader.line_no, self.word_buffer)
                self.state = 1
                return token

            char = self.reader.read_char()


    def state1(self, char):
        if char in [" ", "\t"]:
            self.state = 1
        elif re.match('\d', char):
            self.state = 2
            self.word_buffer = char
        elif re.match('[A-Za-z]', char):
            self.state = 3
            self.word_buffer = char
        elif char == "=":
            self.state = 4
            self.word_buffer = char
        elif char == "<":
            self.state = 6
            self.word_buffer = char
        elif char == ">":
            self.state = 7
            self.word_buffer = char
        elif char in list("+-*/{}|&[]()<>\n%"):
            self.state = 10
            self.word_buffer = char
            return True
        elif char == '"':
            self.state = 11
            self.word_buffer = char
        elif char == "&":
            self.state = 13
            self.word_buffer = char

        else:
            raise Exception("%s行词法分析失败" % self.reader.line_no)


    def state2(self, char):
        if re.match('\d', char):
            self.state = 2
            self.word_buffer += char
        else:
            self.last_char = char
            return True

    def state3(self, char):
        if re.match('\w', char):
            self.state = 3
            self.word_buffer += char
        else:
            self.last_char = char
            return True

    def state4(self, char):
        if char == '=':
            self.state = 5
            self.word_buffer += char
            return True
        else:
            self.last_char = char
            return True

    def state5(self, char):
        self.last_char = char
        return True

    def state6(self, char):
        if char == "=":
            self.state = 8
            self.word_buffer += char
            return True
        else:
            self.last_char = char
            return True

    def state7(self, char):
        if char == "=":
            self.state = 9
            self.word_buffer += char
            return True
        else:
            self.last_char = char
            return True

        pass

    def state8(self, char):
        self.last_char = char
        return True

    def state9(self, char):
        self.last_char = char
        return True


    def state10(self, char):
        self.last_char = char
        return True

    def state11(self, char):
        if char == '"':
            self.state = 12
            self.word_buffer + char
            return True
        else:
            self.state = 11
            self.word_buffer += char

    def state12(self, char):
        return True

    def state13(self, char):

        if char == "&":
            self.state = 14
            self.word_buffer += char
            return True
        else:
            self.last_char = char
            return True





