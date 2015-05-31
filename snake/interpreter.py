# -*- coding: utf8 -*-


import os
import pickle
import time

from snake.astree import NullStmt
from snake.basicenv import BasicEnv
from snake.basicparser import BasicParser
from snake.lexer import ReLexer
from snake.token import Token


def speed(func):
    def _(*args, **kwargs):
        before = time.time()
        ret = func(*args, **kwargs)
        after = time.time()
        print after-before
        return ret
    return _




class Interpreter(object):
    def __init__(self, file_path, middle_code=False):
        self.middle_code = middle_code
        self.file_path = file_path
        self.middle_file_path = file_path+'o'

    def run(self, env={}):

        basic_env = BasicEnv()
        for key, value in env.iteritems():
            basic_env.put(key, value)

        with open(self.file_path, 'r') as f:
            if self.middle_code:
                if os.stat(self.file_path).st_mtime > os.stat(self.middle_file_path).st_mtime:
                    print('m')
                    with open(self.middle_file_path,'wb') as middle_file:
                        bp = BasicParser()
                        l = ReLexer(f)
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





if __name__ == '__main__':
    inter = Interpreter('../test.snake', True)
    env = {'price': 10000, 'distance': 1000, 'stars': 4}
    res = inter.run(env)
    print(res.get('score'))
