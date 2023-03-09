from ast import Num, BinOp, FuncCall, AST, Node
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP
import math

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        if isinstance(node, Num):
            if isinstance(node.value, int):
                return node.value
            elif isinstance(node.value, float):
                return node.value
            else:
                raise TypeError(f"Invalid node value: {node.value}")
        elif isinstance(node, BinOp):
            if node.op.type == PLUS:
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == MINUS:
                return self.visit(node.left) - self.visit(node.right)
            elif node.op.type == MULTIPLY:
                return self.visit(node.left) * self.visit(node.right)
            elif node.op.type == DIVIDE:
                return self.visit(node.left) / self.visit(node.right)
            elif node.op.type == MODULO:
                return self.visit(node.left) % self.visit(node.right)
            elif node.op.type == EXPONENTIATION:
                return self.visit(node.left) ** self.visit(node.right)
            elif node.op.type == FLOOR_DIVIDE:
                return self.visit(node.left) // self.visit(node.right)
            else:
                raise ValueError(f"Invalid operator type: {node.op.type}")
        elif isinstance(node, FuncCall):
            if node.func == 'sin':
                return math.sin(self.visit(node.arg))
            elif node.func == 'cos':
                return math.cos(self.visit(node.arg))
            elif node.func == 'tan':
                return math.tan(self.visit(node.arg))
            elif node.func == 'sqrt':
                return math.sqrt(self.visit(node.arg))
            elif node.func == 'log':
                return math.log(self.visit(node.arg))
            elif node.func == 'exp':
                return math.exp(self.visit(node.arg))
            else:
                raise ValueError(f"Invalid function name: {node.func}")
        else:
            raise TypeError("Invalid node type")

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)