#! -*- utf-8 -*-
import unittest

from stone.lexer import Lexer
from stone.token import Token
class LexerTestCase(unittest.TestCase):
    def setUp(self):
        self.f = open('test.stone','r')

    def test_read(self):
        l = Lexer(self.f)
        token = l.read()
        while token != Token.EOF:
            print token
            token = l.read()
if __name__ == '__main__':
    unittest.main()
