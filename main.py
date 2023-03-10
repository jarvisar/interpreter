from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP
from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp
from myparser import Parser
from lexer import Lexer
from interpreter import Interpreter
from generator import CodeGenerator
from analyzer import SemanticAnalyzer


# print("Currently supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).")
# print("Works with integers and decimals and supports parentheses, e.g. '(3 + 4) / 5' outputs 1.4 and '3 + 4 / 5' outputs 3.8.")
symbol_table = {}

while True:
    text = input("Enter an arithmetic expression: ")
    try:
        if '=' in text:
            # If the input contains an equal sign, skip code generation
            interpreter = Interpreter(Parser(Lexer(text)), symbol_table)
            result = interpreter.interpret()
            if isinstance(result, dict):
                symbol_table = result
            else:
                print(f'Result: {result}')
        else:
            # Otherwise, proceed with code generation as before
            lexer = Lexer(text)
            parser = Parser(lexer)
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.analyze(parser)
            action = input("Press 2 to show assembly code, or any other key to interpret result:")
            if action == "2":
                generator = CodeGenerator(parser, symbol_table)
                assembly_code = generator.generate_code()
                print("== Begin Assembly Code ==")
                print("\n".join(assembly_code))
                print("== End Assembly Code ==")
            else:
                interpreter = Interpreter(parser, symbol_table)
                result = interpreter.interpret()
                if isinstance(result, dict):
                    symbol_table = result
                else:
                    print(f'Result: {result}')
    except Exception as e:
        print(f"Error: {e}")




