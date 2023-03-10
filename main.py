from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP
from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp
from myparser import Parser
from lexer import Lexer
from interpreter import Interpreter
from generator import CodeGenerator
from analyzer import SemanticAnalyzer


# print("Currently supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).")
# print("Works with integers and decimals and supports parentheses, e.g. '(3 + 4) / 5' outputs 1.4 and '3 + 4 / 5' outputs 3.8.")
vars = {}
while True:
    text = input("Enter an arithmetic expression: ")
    lexer = Lexer(text)
    parser = Parser(lexer)
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(parser)
    action = input("Press 2 to show assembly code, or any other key to interpret result:")
    if action == "2":
        generator = CodeGenerator(parser)
        assembly_code = generator.generate_code()
        print("== Begin Assembly Code ==")
        print("\n".join(assembly_code))
        print("== End Assembly Code ==")
    else:
        intepreter = Interpreter(parser, vars)
        result = intepreter.interpret()
        if isinstance(result, dict):
            vars = result
        else:
            print(f'Result: {result}')

