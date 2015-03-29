#! -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod
class ASTree:
    __metaclass__ = ABCMeta

    @abstractmethod
    def child(self, i):
        pass

    @abstractmethod
    def num_child(self):
        pass

    @abstractmethod
    def children(self):
        pass

    @abstractmethod
    def location(self):
        pass

    def __iter__(self):
        return self.children()

class ASTLeaf(ASTree):
    def __init__(self, t):
        self.token = t
        self._children = []

    def child(self, i):
        raise IndexError()

    def num_child(self):
        return 0

    def children(self):
        return self._children

    def location(self):
        return 'at line %s'%self.token.get_line_number()

class ASTList(ASTree):
    def __init__(self, l):
        self._children = l

    def child(self, i):
        return self.children[i]

    def num_child(self):
        return len(self._children)

    def children(self):
        return iter(self._children)


class NumberLiteral(ASTree):
    def __init__(self, t):
        super(NumberLiteral, self).__init__(t)

    def value(self):
        return self.token()

class Name(ASTree):
    def __init__(self, t):
        super(Name, self).__init__(t)

    def name(self):
        return self.token()


class BinaryExpr(ASTList):
    def __init__(self, c):
        super(BinaryExpr, self).__init__(c)

    def left(self):
        return self.child(0)

    def operator(self):
        return self.child(1).token()

    def right(self):
        return self.child(2)


