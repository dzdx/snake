#! -*- coding:utf-8 -*-
from token import Token


class StoneException(Exception):

    def __init__(self, m, t):
        Exception.__init__(self, m+" "+t.location())
    pass


class ParseException(Exception):
    def __init__(self, m, t):
        Exception.__init__(self, "%s处有语法错误"%self.location(t))

    def location(self, t):
        if t==Token.EOF:
            return "最后一行"
        else:
            return r'在第%s行的%s'%(t.get_line_number(),repr(t.text()))

