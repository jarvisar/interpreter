from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp, Var
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP, FACTORIAL
import math

class Interpreter:
    def __init__(self, parser, symbol_table):
        self.parser = parser
        self.symbol_table = symbol_table

    def visit(self, node):
        if isinstance(node, UnaryOp):
            if node.op.type == FACTORIAL:
                return math.factorial(self.visit(node.expr))
            elif node.op.type == MINUS:
                return -self.visit(node.expr)
            else:
                raise ValueError(f"Invalid operator type: {node.op.type}")
        elif isinstance(node, Num):
            if isinstance(node.value, int):
                return node.value
            elif isinstance(node.value, float):
                return node.value
            else:
                raise TypeError(f"Invalid node value: {node.value}")
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(left, Var):
                left = self.symbol_table[left.name.value]
            if isinstance(right, Var):
                right = self.symbol_table[right.name.value]
            if node.op.type == PLUS:
                return left + right
            elif node.op.type == MINUS:
                return left - right
            elif node.op.type == MULTIPLY:
                return left * right
            elif node.op.type == DIVIDE:
                return left / right
            elif node.op.type == MODULO:
                return left % right
            elif node.op.type == EXPONENTIATION:
                return left ** right
            elif node.op.type == FLOOR_DIVIDE:
                return left // right
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
        elif isinstance(node, Var):
            if node.value is not None:
                # handle variable assignment
                var_name = node.name.value
                self.symbol_table[var_name] = self.visit(node.value)
                return self.symbol_table
            else:
                # return variable value
                var_name = node.name.value
                if var_name in self.symbol_table:
                    return self.symbol_table[var_name]
                else:
                    raise NameError(f"Name '{var_name}' is not defined")
        else:
            raise TypeError("Invalid node type")

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)