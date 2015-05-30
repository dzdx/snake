#! -*- utf-8 -*-

from snake.lexer import ReLexer
from snake.token import Token
from snake.basicparser import BasicParser
from snake.basicenv import BasicEnv
from snake.astree import NullStmt

import unittest

class TestParser(unittest.TestCase):

    def test_relexer(self):
        f = open('test.snake', 'r')
        l = ReLexer(f)
        token = l.read()
        while token != Token.EOF:
            token = l.read()






    def test_basicparser(self):
        f = open('test.snake', 'r')
        l = ReLexer(f)
        bp = BasicParser()
        while l.peek(0) != Token.EOF:
            ast = bp.parse(l)

    def test_basicInterpreter(self):
        env = BasicEnv()
        bp = BasicParser()
        f = open('test.snake', 'r')
        l = ReLexer(f)
        r = 0
        while l.peek(0) != Token.EOF:
            ast = bp.parse(l)
            if not isinstance(ast, NullStmt):
                r = ast.eval(env)
        print 'result='+str(r)



if __name__ == '__main__':
    unittest.main()
