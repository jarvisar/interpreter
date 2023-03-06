from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF
from ast import Num, BinOp, FuncCall, AST, Node
from myparser import Parser
from lexer import Lexer
from interpreter import Interpreter
from generator import CodeGenerator


# print("Currently supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).")
# print("Works with integers and decimals and supports parentheses, e.g. '(3 + 4) / 5' outputs 1.4 and '3 + 4 / 5' outputs 3.8.")
while True:
    text = input("Enter an arithmetic expression: ")
    lexer = Lexer(text)
    parser = Parser(lexer)
    generator = CodeGenerator(parser)
    result = generator.generate_code()
    print(result)
