#! -*- coding:utf-8 -*-
import re
from exception import ParseException
from token import Token, NumToken, StrToken, IdToken
from reader import FileReader
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
        self.reader = FileReader(f)
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
        line = self.reader.read_line()
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
        self.reader = FileReader(f)
        self.state = 1
        self.queue = []
        self.word_buffer = ""
        self.tmp_char = ""


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

    def get_char(self):
        if not self.tmp_char:
            char = self.reader.read_char()
            return char
        else:
            char = self.tmp_char
            self.tmp_char = ""
            return char

    def unget_char(self, char):
        self.tmp_char = char

    def ret_token(self, word):

        if self.state in (2,):
            token = NumToken(self.reader.line_no, word)
        elif self.state in (12,):
            token = StrToken(self.reader.line_no, word)
        elif self.state in (3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16,):
            token = IdToken(self.reader.line_no, word)
        self.state = 1
        return token


    def add_token(self):
        self.word_buffer = ""
        while True:
            char = self.get_char()
            if char == "":
                if self.word_buffer:
                    word = self.word_buffer.strip(" ").strip("\t")
                    return self.ret_token(word)
                return Token.EOF
            ret = getattr(self, "state%s" % self.state)(char)
            if ret:
                token = None
                word = self.word_buffer.strip(" ").strip("\t")
                if word:
                    self.unget_char(char)
                    return self.ret_token(word)


    def state1(self, char):
        if char in [" ", "\t"]:
            self.state = 1
        elif re.match('\d', char):
            self.state = 2
        elif re.match('[A-Za-z]', char):
            self.state = 3
        elif char == "=":
            self.state = 4
        elif char == "<":
            self.state = 6
        elif char == ">":
            self.state = 7
        elif char in list("+-*/{}|&[]()<>\n%"):
            self.state = 10
        elif char == '"':
            self.state = 11
        elif char == "&":
            self.state = 13
        else:
            raise Exception("%s行词法分析失败" % self.reader.line_no)

        self.word_buffer += char


    def state2(self, char):
        if re.match('\d', char):
            self.state = 2
            self.word_buffer += char
        else:
            return True

    def state3(self, char):
        if re.match('\w', char):
            self.state = 3
            self.word_buffer += char
        else:
            return True

    def state4(self, char):
        if char == '=':
            self.state = 5
            self.word_buffer += char
        else:
            return True

    def state5(self, char):
        return True

    def state6(self, char):
        if char == "=":
            self.state = 8
            self.word_buffer += char
        else:
            return True

    def state7(self, char):
        if char == "=":
            self.state = 9
            self.word_buffer += char
        else:
            return True


    def state8(self, char):
        return True

    def state9(self, char):
        return True


    def state10(self, char):
        return True

    def state11(self, char):
        if char == '"':
            self.state = 12
            self.word_buffer += char
        else:
            self.state = 11
            self.word_buffer += char

    def state12(self, char):
        return True

    def state13(self, char):

        if char == "&":
            self.state = 14
            self.word_buffer += char
        else:
            return True

    def state14(self, char):
        return True

    def state15(self, char):
        if char == "|":
            self.state = 16
            self.word_buffer += char

    def state16(self, char):
        return True





