#!/usr/bin/env python
# coding=utf-8

from astree import ASTLeaf, ASTList, NumberLiteral, StringLiteral, Name, NegativeExpr, BinaryExpr, BlockStmnt, IfStmnt, \
    WhileStmt, NullStmt

from exception import StoneException


class BasicEnv(object):
    def __init__(self):
        self.value = dict()

    def put(self, name, value):
        self.value[name] = value

    def get(self, name):
        return self.value.get(name)


class BasicEvaluator(object):
    TRUE = 1
    FALSE = 0


def category(ori_cls):
    def _(cls):
        for key, value in filter(lambda item: not item[0].startswith("_"), cls.__dict__.iteritems()):
            setattr(ori_cls, key, value)
        return cls
    return _


@category(ASTLeaf)
class ASTLeafEx:
    def eval(self, env):
        raise StoneException('不能执行:' + str(self), self)


@category(ASTList)
class ASTListEx:
    def eval(self, env):
        raise StoneException("不能执行:" + str(self), self)


@category(NumberLiteral)
class NumberLiteralEx:
    def eval(self, env):
        return self.value()


@category(StringLiteral)
class StringLiteralEx:
    def eval(self, env):
        return self.value()


@category(Name)
class NameEx:
    def eval(self, env):
        value = env.get(self.name())
        if value == None:
            raise StoneException('%s变量未定义' % repr(self.name()), self)
        return value


@category(NegativeExpr)
class NegativeExprEx:
    def eval(self, env):
        v = self.operand().eval(env)
        if isinstance(v, int):
            return -v
        else:
            raise StoneException("'-'类型错误", self)


@category(BinaryExpr)
class BinaryExprEx:
    def eval(self, env):
        op = self.operator()
        if op == "=":
            right = self.right().eval(env)
            return self.compute_assgin(env, right)
        else:
            left = self.left().eval(env)
            right = self.right().eval(env)

            return self.compute_op(left, op, right)

    def compute_assgin(self, env, value):
        l = self.left()
        if isinstance(l, Name):
            env.put(l.name(), value)
            return value
        else:
            raise StoneException('不能赋值给非变量', self)


    def compute_op(self, left, op, right):
        if isinstance(left, (int, float, long)) and isinstance(right, (int, float, long)):
            return self.compute_num(left, op, right)

        else:
            if op == '+':
                return str(left) + str(right)
            elif op == '==':
                return BasicEvaluator.TRUE if left == right else BasicEvaluator.FALSE

            else:
                raise StoneException("不支持%s运算符" % op, self)

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

            return BasicEvaluator.TRUE if left == right else BasicEvaluator.FALSE
        elif op == '>':
            return BasicEvaluator.TRUE if left > right else BasicEvaluator.FALSE
        elif op == '<':
            return BasicEvaluator.TRUE if left < right else BasicEvaluator.FALSE

        else:
            raise StoneException("不支持%s运算符" % op, self)


@category(BlockStmnt)
class BlockStmntEx:
    def eval(self, env):
        result = 0
        for t in self:
            if not isinstance(t, NullStmt):
                result = t.eval(env)
        return result


@category(IfStmnt)
class IfStmntEx:
    def eval(self, env):
        c = self.condition().eval(env)
        if c != BasicEvaluator.FALSE:
            return self.then_block().eval(env)
        else:
            b = self.else_block()
            if b != None:
                return b.eval(env)
            else:
                return 0


@category(WhileStmt)
class WhileStmtEx:
    def eval(self, env):
        result = 0
        while True:
            c = self.condition().eval(env)
            if c == BasicEvaluator.FALSE:
                return result
            else:
                result = self.body().eval(env)

