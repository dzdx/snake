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
        return 'at line %s' % self.token.get_line_number()

    def token(self):
        return self.token

    def __str__(self):
        return str(self.token)


class ASTList(ASTree):

    def __init__(self, l):
        self._children = l

    def child(self, i):
        return self._children[i]

    def num_child(self):
        return len(self._children)

    def children(self):
        return iter(self._children)


    def __str__(self):
        res = "("
        sep = ""
        for t in self._children:
            res += sep
            sep = " "
            res+=str(t)
        res+=")"
        return res



    def location(self):
        for t in self._children:
            s = t.location()
            if s:
                return s
        return None



class NumberLiteral(ASTLeaf):

    def __init__(self, t):
        super(NumberLiteral, self).__init__(t)

    def value(self):
        return self.token.get_number()


class Name(ASTLeaf):

    def __init__(self, t):
        super(Name, self).__init__(t)

    def name(self):
        return self.token.text()




class BinaryExpr(ASTList):

    def __init__(self, c):
        super(BinaryExpr, self).__init__(c)

    def left(self):
        return self.child(0)

    def operator(self):
        return self.child(1).token()

    def right(self):
        return self.child(2)


class PrimaryExpr(ASTList):

    @classmethod
    def create(cls, c):
        return c[0]if len(c) else PrimaryExpr(c)


class StringLiteral(ASTLeaf):

    def value(self):
        return self.token.text()


class NegativeExpr(ASTList):

    def operand(self):
        return self.child(0)

    def __str__(self):
        return str("-" + self.operand())


class BlockStmnt(ASTList):
    pass


class IfStmnt(ASTList):

    def condition(self):
        return self.child(0)

    def then_block(self):
        return self.child(1)

    def else_block(self):
        return self.child(2) if self.num_child() > 2 else None

    def __str__(self):
        return "(if %s %s else %s )" % (
            self.condition(), self.then_block(), self.else_block())


class NullStmt(ASTList):
    pass


class WhileStmt(ASTList):


    def condition(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def __str__(self):
        return "(while %s {%s})" % (self.condition(), self.body())
