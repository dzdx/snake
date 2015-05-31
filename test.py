#! -*- coding:utf-8 -*-

from snake.lexer import ReLexer, AutomatonLexer
from snake.token import Token
from snake.basicparser import BasicParser
from snake.basicenv import BasicEnv
from snake.astree import NullStmt

import unittest


class TestParser(unittest.TestCase):
    # def test_relexer(self):
    #     '''
    #     正则词法分析器
    #     '''
    #     f = open('test.snake', 'r')
    #     l = ReLexer(f)
    #     token = l.read()
    #     while token != Token.EOF:
    #         print '*',repr(token)
    #         token = l.read()

    # def test_automaton(self):
    #     '''
    #     有限状态自动机词法分析器
    #     '''
    #     f = open('test.snake', 'r')
    #     l = AutomatonLexer(f)
    #     i = 0
    #     token = l.read()
    #     while token != Token.EOF:
    #         i+=1
    #         print '-', repr(token)
    #         token = l.read()
    #         assert i < 50


    # def test_basicparser(self):
    #     '''
    #     语法分析器
    #     '''
    #     f = open('test.snake', 'r')
    #     l = ReLexer(f)
    #     bp = BasicParser()
    #     while l.peek(0) != Token.EOF:
    #         ast = bp.parse(l)

    def test_basicInterpreter(self):
        '''
        基本解释器
        '''
        env = BasicEnv()
        bp = BasicParser()
        f = open('test.snake', 'r')
        l = ReLexer(f)
        r = 0
        while l.peek(0) != Token.EOF:
            ast = bp.parse(l)
            if not isinstance(ast, NullStmt):
                r = ast.eval(env)
        print 'result=' + str(r)


if __name__ == '__main__':
    unittest.main()
