from token import Token
from parser import Parser, Operators
from snake.astree import PrimaryExpr, NumberLiteral, Name, StringLiteral, NegativeExpr, BinaryExpr, \
    BlockStmnt, IfStmnt, WhileStmt, NullStmt


class BasicParser(object):


    def __init__(self):

        self.reserved = set()

        self.operators = Operators()

        self.expr0 = Parser()
        self.primary = Parser(PrimaryExpr).between(
            Parser().sep("(").ast(self.expr0).sep(")"),
            Parser().number(NumberLiteral),
            Parser().identifier(self.reserved, Name),
            Parser().string(StringLiteral)
        )
        self.factor = Parser().between(
            Parser(NegativeExpr).sep("-").ast(self.primary),
            self.primary
        )

        self.expr = self.expr0.expression(self.factor, self.operators, BinaryExpr)

        self.statement0 = Parser()
        self.block = Parser(BlockStmnt).sep("{").option(self.statement0).repeat(
            Parser().sep(";", Token.EOL).option(self.statement0)).sep("}")

        self.simple = Parser(PrimaryExpr).ast(self.expr)
        self.statement = self.statement0.between(
            Parser(IfStmnt).sep("if").ast(self.expr).ast(self.block).option(
                Parser().sep("else").ast(self.block)),
            Parser(WhileStmt).sep("while").ast(self.expr).ast(self.block),
            self.simple)

        self.program = Parser().between(self.statement, Parser(NullStmt)).sep(";", Token.EOL)

        self.reserved.add(";")
        self.reserved.add("}")
        self.reserved.add(Token.EOL)

        self.operators.add("=", 1, Operators.RIGHT)
        self.operators.add("==", 2, Operators.LEFT)
        self.operators.add(">", 2, Operators.LEFT)
        self.operators.add("<", 2, Operators.LEFT)
        self.operators.add("+", 3, Operators.LEFT)
        self.operators.add("-", 3, Operators.LEFT)
        self.operators.add("*", 4, Operators.LEFT)
        self.operators.add("/", 4, Operators.LEFT)
        self.operators.add("%", 4, Operators.LEFT)

    def parse(self, lexer):
        return self.program.parse(lexer)
