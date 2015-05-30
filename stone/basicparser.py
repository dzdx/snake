from token import Token
from parser import Parser, Operators
from stone.astree import PrimaryExpr, NumberLiteral, Name, StringLiteral, NegativeExpr, BinaryExpr, \
    BlockStmnt, IfStmnt, WhileStmt, NullStmt


class BasicParser(object):
    reserved = set()

    operators = Operators()

    expr0 = Parser()
    primary = Parser(PrimaryExpr).between(
        Parser().sep("(").ast(expr0).sep(")"),
        Parser().number(NumberLiteral),
        Parser().identifier(reserved, Name),
        Parser().string(StringLiteral)
    )
    factor = Parser().between(
        Parser(NegativeExpr).sep("-").ast(primary),
        primary
    )

    expr = expr0.expression(factor, operators, BinaryExpr)

    statement0 = Parser()
    block = Parser(BlockStmnt).sep("{").option(statement0).repeat(
        Parser().sep(";", Token.EOL).option(statement0)).sep("}")

    simple = Parser(PrimaryExpr).ast(expr)
    statement = statement0.between(
        Parser(IfStmnt).sep("if").ast(expr).ast(block).option(
            Parser().sep("else").ast(block)),
        Parser(WhileStmt).sep("while").ast(expr).ast(block),
        simple)

    program = Parser().between(statement, Parser(NullStmt)).sep(";", Token.EOL)

    def __init__(self):
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
