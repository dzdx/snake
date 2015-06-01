#! -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod
from astree import ASTLeaf, ASTList
from token import Token
from exception import ParseException


class Factory:
    default_func = "create"

    @classmethod
    def get(cls, clazz):

        if not clazz:
            return None

        func = getattr(clazz, cls.default_func, None)

        factory = cls()
        if func:
            factory.make0 = lambda arg: func(arg)
        else:
            factory.make0 = lambda arg: clazz(arg)

        return factory

    @classmethod
    def get_for_astlist(cls, clazz):
        factory = Factory.get(clazz)
        if factory is None:
            def make0(arg):
                assert isinstance(arg, list)
                if len(arg) == 1:
                    return arg[0]
                else:
                    return ASTList(arg)

            factory = cls()
            factory.make0 = make0
        return factory

    def make(self, ast):
        return self.make0(ast)


class Parser(object):
    def __init__(self, arg=None):
        if isinstance(arg, Parser):
            self.elements = arg.elements
            self.factory = arg.factory
        else:
            self.reset(arg)

    def reset(self, clazz=None):
        self.elements = []
        self.factory = Factory.get_for_astlist(clazz)
        return self

    def parse(self, lexer):
        results = []
        for e in self.elements:
            e.parse(lexer, results)
        return self.factory.make(results)

    def match(self, lexer):
        if len(self.elements) == 0:
            return True
        else:
            return self.elements[0].match(lexer)

    def between(self, *parsers):
        self.elements.append(OrTree(parsers))

        return self

    def sep(self, *ts):
        self.elements.append(Skip(ts))
        return self

    def number(self, clazz=None):
        self.elements.append(NumToken(clazz))
        return self

    def ast(self, parser):
        self.elements.append(Tree(parser))
        return self

    def identifier(self, reserved, clazz=None):
        self.elements.append(IdToken(clazz, reserved))
        return self

    def string(self, clazz=None):
        self.elements.append(StrToken(clazz))
        return self

    def token(self, **ts):
        self.elements.append(Leaf(ts))
        return self

    def repeat(self, parser):
        self.elements.append(Repeat(parser, False))
        return self

    def option(self, parser):
        self.elements.append(Repeat(parser, True))
        return self

    def expression(self, subexp, operators, clazz=None):
        self.elements.append(Expr(clazz, subexp, operators))
        return self


class Element(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, lexer, res):
        pass

    @abstractmethod
    def match(self, lexer):
        pass


class Tree(Element):
    def __init__(self, p):
        self.parser = p

    def parse(self, lexer, res):
        res.append(self.parser.parse(lexer))

    def match(self, lexer):
        return self.parser.match(lexer)


class OrTree(Element):
    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, lexer, res):
        p = self.choose(lexer)
        if p is None:
            raise ParseException("语法解析出错")
        else:
            res.append(p.parse(lexer))

    def match(self, lexer):
        return self.choose(lexer) != None

    def choose(self, lexer):
        for p in self.parsers:
            if p.match(lexer):
                return p

        return None


class Repeat(Element):
    def __init__(self, p, once):
        self.parser = p
        self.onlyOnce = once

    def parse(self, lexer, res):
        while self.parser.match(lexer):
            t = self.parser.parse(lexer)
            if (not isinstance(t, ASTList)) or t.num_child() > 0:
                res.append(t)

            if self.onlyOnce:
                break

    def match(self, lexer):
        return self.match(lexer)


class AToken(Element):
    __metaclass__ = ABCMeta

    def __init__(self, clazz=None):
        if clazz is None:
            clazz = ASTLeaf
        self.factory = Factory.get(clazz)

    def parse(self, lexer, res):
        t = lexer.read()
        if self.test(t):
            leaf = self.factory.make(t)
            res.append(leaf)
        else:
            raise ParseException()

    def match(self, lexer):
        return self.test(lexer.peek(0))

    @abstractmethod
    def test(self, token):
        pass


class IdToken(AToken):
    def __init__(self, clazz=None, r=None):
        AToken.__init__(self, clazz)
        self.reserved = (r if r != None else set())


    def test(self, token):
        return token.type == Token.TOKEN_ID and not (
            token.text() in self.reserved)


class NumToken(AToken):
    def test(self, token):
        return token.type == Token.TOKEN_NUM


class StrToken(AToken):
    def test(self, token):
        return token.type == Token.TOKEN_STR


class Leaf(Element):
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self, lexer, res):
        t = lexer.read()
        if t.type == Token.TOKEN_ID:
            for token in self.tokens:
                if token == t.text():
                    self.find(res, t)
                    return

        if len(self.tokens) > 0:
            raise ParseException(token[0] + "语法分析失败. " ,t)
        else:
            raise ParseException()

    def find(self, res, token):
        res.append(ASTLeaf(token))

    def match(self, lexer):
        t = lexer.peek(0)
        if t.type == Token.TOKEN_ID:
            for token in self.tokens:
                if token == t.text():
                    return True

        return False


class Skip(Leaf):
    def find(self, res, t):
        pass


class Precedence:
    def __init__(self, v, a):
        self.value = v
        self.left_assoc = a


class Operators(dict):
    LEFT = True
    RIGHT = False

    def add(self, name, prec, left_assoc):
        self[name] = Precedence(prec, left_assoc)


class Expr(Element):
    def __init__(self, clazz, exp, operators):
        self.factory = Factory.get_for_astlist(clazz)
        self.operators = operators
        self.factor = exp

    def parse(self, lexer, res):
        right = self.factor.parse(lexer)
        prec = self.next_operator(lexer)
        while prec != None:
            right = self.do_shift(lexer, right, prec.value)
            prec = self.next_operator(lexer)
        res.append(right)

    def next_operator(self, lexer):
        t = lexer.peek(0)
        if t.type == Token.TOKEN_ID:
            return self.operators.get(t.text())
        else:
            return None

    def do_shift(self, lexer, left, prec):
        l = []
        l.append(left)
        l.append(ASTLeaf(lexer.read()))
        right = self.factor.parse(lexer)
        next_prec = self.next_operator(lexer)
        while next_prec and self.right_is_expr(prec, next_prec):
            right = self.do_shift(lexer, right, next_prec.value)
            next_prec = self.next_operator(lexer)
        l.append(right)
        return self.factory.make(l)

    def right_is_expr(self, prec, next_prec):
        if next_prec.left_assoc:
            return prec < next_prec.value
        else:
            return prec <= next_prec.value


    def match(self, lexer):
        return self.factor.match(lexer)
