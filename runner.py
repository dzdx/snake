#! -*- utf-8 -*-

from stone.lexer import ReLexer
from stone.token import Token
from stone.basicparser import BasicParser
# import sys
# import  crashonipy

def test_relexer():
    f = open('test.stone', 'r')
    l = ReLexer(f)
    token = l.read()
    while token != Token.EOF:
        print repr(token)
        token = l.read()






def test_basicparser():
    f = open('test.stone', 'r')
    l = ReLexer(f)
    bp = BasicParser()
    while l.peek(0) != Token.EOF:
        ast = bp.parse(l)
        print str(ast)



if __name__ == '__main__':
    test_relexer()
