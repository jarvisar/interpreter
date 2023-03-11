from myast import Num, BinOp, FuncCall, AST, Node, UnaryOp
from tokens import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP, FACTORIAL
import math

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)
            if node.left.type != node.right.type:
                raise Exception(f"Type mismatch between {node.left.type} and {node.right.type}")

            node.type = node.left.type
            
        elif isinstance(node, Num):
            node.type = "int"

        elif isinstance(node, FuncCall):
            self.analyze(node.arg)

            if node.func not in self.symbol_table:
                raise Exception(f"Function {node.func} is not defined")

            func_return_type = self.symbol_table[node.func]
            arg_type = node.arg.type

            if arg_type != func_return_type.arg_type:
                raise Exception(f"Type mismatch between argument {arg_type} and function {func_return_type.arg_type}")

            node.type = func_return_type.return_type

        elif isinstance(node, UnaryOp):
            self.analyze(node.expr)
            node.type = node.expr.type