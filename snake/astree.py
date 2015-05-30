#! -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod

from snake.exception import StoneException
from snake.basicenv import BasicEvaluator

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

    def eval(self, env):
        raise StoneException('can not eval:' + str(self), self)



class ASTList(ASTree):

    def __init__(self, l):
        self._children = l

    def child(self, i):
        return self._children[i]

    def num_child(self):
        return len(self._children)

    def children(self):
        return iter(self._children)


    def __iter__(self):
        return iter(self._children)

    def __str__(self):
        res = "("
        sep = ""
        for t in self._children:
            res += sep
            sep = " "
            res += str(t)
        res += ")"
        return res

    def location(self):
        for t in self._children:
            s = t.location()
            if s:
                return s
        return None

    def eval(self, env):
        raise StoneException("can not eval:" + str(self), self)



class NumberLiteral(ASTLeaf):

    def __init__(self, t):
        super(NumberLiteral, self).__init__(t)

    def value(self):
        return self.token.get_number()

    def eval(self, env):
        return self.value()





class StringLiteral(ASTLeaf):

    def value(self):
        return self.token.text()

    def eval(self, env):
        return self.value()



class Name(ASTLeaf):

    def __init__(self, t):
        super(Name, self).__init__(t)

    def name(self):
        return self.token.text()

    def eval(self, env):
        value = env.get(self.name())
        if value == None:
            raise StoneException('undefined name:' + self.name(), self)
        return value


class NegativeExpr(ASTList):

    def operand(self):
        return self.child(0)

    def __str__(self):
        return str("-" + self.operand())

    def eval(self, env):
        v = self.operand().eval(env)
        if isinstance(v, int):
            return -v
        else:
            raise StoneException("bad type for -", self)




class BinaryExpr(ASTList):

    def __init__(self, c):
        super(BinaryExpr, self).__init__(c)

    def left(self):
        return self.child(0)

    def operator(self):
        return self.child(1).token.text()


    def right(self):
        return self.child(2)

    def eval(self, env):
        op = self.operator()
        if op == "=":
            right = self.right().eval(env)
            return self.compute_assgin(env, right)
        else:
            left = self.left().eval(env)
            right = self.right().eval(env)
            return self.compute_op(left ,op ,right)

    def compute_assgin(self, env, value):
        l = self.left()
        if isinstance(l, Name):
            env.put(l.name(), value)
            return value
        else:
            raise StoneException('bad assignment', self)



    def compute_op(self, left, op, right):
        if isinstance(left, int) and isinstance(right, int):
            return self.compute_num(left, op, right)

        else:
            if op == '+':
                return str(left)+str(right)
            elif op == '==':
                return BasicEvaluator.TRUE if left==right else BasicEvaluator.FALSE

            else:
                raise StoneException("bad type ", self)

    def compute_num(self, left, op, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '==':
            return BasicEvaluator.TRUE if left==right else BasicEvaluator.FALSE
        elif op == '>':
            return BasicEvaluator.TRUE if left>right else BasicEvaluator.FALSE
        elif op == '<':
            return BasicEvaluator.TRUE if left<right else BasicEvaluator.FALSE

        else:
            raise StoneException("bad operator ", self)







class PrimaryExpr(ASTList):

    @classmethod
    def create(cls, c):
        return c[0] if len(c) else PrimaryExpr(c)



class BlockStmnt(ASTList):

    def eval(self, env):
        result = 0
        for t in self:
            if not isinstance(t, NullStmt):
                result = t.eval(env)
        return result



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

    def eval(self, env):
        c = self.condition().eval(env)
        if c == BasicEvaluator.FALSE:
            return self.then_block().eval(env)
        else:
            b = self.else_block()
            if b != None:
                return b.eval(env)
            else:
                return 0



class NullStmt(ASTList):
    pass


class WhileStmt(ASTList):

    def condition(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def __str__(self):
        return "(while %s {%s})" % (self.condition(), self.body())

    def eval(self, env):
        result = 0
        while True:
            c = self.condition().eval(env)
            if c == BasicEvaluator.FALSE:
                return result
            else:
                result = self.body().eval(env)
