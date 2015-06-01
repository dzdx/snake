# -*- coding: utf8 -*-

import unittest
from snake.basicparser import BasicParser
from snake.interpreter import Interpreter
from snake.lexer import ReLexer, AutomatonLexer
from snake.token import Token


class InterpreterTest(unittest.TestCase):
    def test_relexer(self):
        '''
        正则词法分析器
        '''
        f = open('test.snake', 'r')
        l = ReLexer(f)
        token = l.read()
        while token != Token.EOF:
            token = l.read()

    def test_automaton(self):
        '''
        有限状态自动机词法分析器
        '''
        f = open('test.snake', 'r')
        l = AutomatonLexer(f)
        token = l.read()
        while token != Token.EOF:
            token = l.read()


    def test_basicparser(self):
        '''
        语法分析器
        '''
        f = open('test.snake', 'r')
        l = ReLexer(f)
        bp = BasicParser()
        while l.peek(0) != Token.EOF:
            ast = bp.parse(l)

    def test_basicInterpreter(self):
        '''
        基本解释器
        '''

        env = {
            'price': 10000.1,
            'stars': 4.5,
            'distance': 100.1
        }
        inter = Interpreter('test.snake', middle_code=True, lexer_class=AutomatonLexer)
        basic_env = inter.run(env)


if __name__ == '__main__':
    unittest.main()
