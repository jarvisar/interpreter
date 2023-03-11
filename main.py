import argparse
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP
from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp
from myparser import Parser
from lexer import Lexer
from interpreter import Interpreter
from generator import CodeGenerator
from analyzer import SemanticAnalyzer

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="input file name")
args = parser.parse_args()

symbol_table = {}

if args.file:
    with open(args.file, "r") as f:
        for line in f:
            text = line.strip()
            if not text or text.isspace() or text.startswith("#"):
                continue
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
                    if text.endswith(";"):
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
else:
    while True:
        text = input("Enter an arithmetic expression: ")
        if not text or text.isspace() or text.startswith("#"):
                continue
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
