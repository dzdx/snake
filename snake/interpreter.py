# -*- coding: utf8 -*-


import os

try:
    import cPickle as pickle
except ImportError, e:
    import pickle
import StringIO

from astree import NullStmt
from basicenv import BasicEnv
from basicparser import BasicParser
from lexer import ReLexer
from token import Token


class Interpreter(object):
    def __init__(self, file_path="", middle_code=False,lexer_class=ReLexer):
        self.middle_code = middle_code
        self.file_path = file_path
        self.middle_file_path = file_path + 'o'
        self.lexer_class = lexer_class


    def run_script(self, code, env={}):
        code += '\n'
        basic_env = BasicEnv()
        for key, value in env.iteritems():
            basic_env.put(key, value)
        f = StringIO.StringIO(code)

        bp = BasicParser()
        l = self.lexer_class(f)
        while l.peek(0) != Token.EOF:
            ast = bp.parse(l)
            if not isinstance(ast, NullStmt):
                ast.eval(basic_env)
        return basic_env


    def run(self, env={}):

        basic_env = BasicEnv()
        for key, value in env.iteritems():
            basic_env.put(key, value)

        with open(self.file_path, 'r') as f:
            if self.middle_code:
                if (not os.path.exists(self.middle_file_path)) or os.stat(self.file_path).st_mtime > os.stat(
                        self.middle_file_path).st_mtime:
                    with open(self.middle_file_path, 'wb') as middle_file:
                        bp = BasicParser()
                        l = self.lexer_class(f)
                        while l.peek(0) != Token.EOF:
                            ast = bp.parse(l)
                            if not isinstance(ast, NullStmt):
                                pickle.dump(ast, middle_file)
                with open(self.middle_file_path, 'rb') as middle_file:
                    while True:
                        try:
                            ast = pickle.load(middle_file)
                            ast.eval(basic_env)
                        except EOFError:
                            break
            else:
                bp = BasicParser()
                l = ReLexer(f)
                while l.peek(0) != Token.EOF:
                    ast = bp.parse(l)
                    if not isinstance(ast, NullStmt):
                        ast.eval(basic_env)
        return basic_env


