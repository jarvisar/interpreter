import argparse
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP
from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp
from myparser import Parser
from lexer import Lexer
from interpreter import Interpreter
from generator import CodeGenerator
from analyzer import SemanticAnalyzer
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="input file name")
args = parser.parse_args()

symbol_table = {}

def runAssembly():
    # Use the modified Python code to assemble, link, and run the generated code
    if os.path.exists('assembly.s'):
        import platform
        import subprocess

        # Check if running on Windows
        if platform.system() == 'Windows':
            # Use WSL to run the commands
            command_prefix = ['wsl', 'bash', '-c']
            # Assemble the code
            print("Assembling code...")
            subprocess.run(command_prefix + ['as -o assembly.o assembly.s --64 -g'])
            # Link the code
            print("Linking...")
            subprocess.run(command_prefix + ['gcc -shared -o assembly assembly.o -lm -no-pie -g'])
            # Run the executable
            print("Executing...")
            subprocess.run(command_prefix + ['./assembly'])
        else:
            command_prefix = []
            # Assemble the code
            print("Assembling code...")
            subprocess.run(command_prefix + ['gcc', '-c', '-o', 'assembly.o', 'assembly.s', '--64'])
            # Link the code
            print("Linking code...")
            subprocess.run(command_prefix + ['gcc', '-o', 'assembly', 'assembly.o', '-lm', '-no-pie'])
            # Run the executable
            print("Executing...")
            subprocess.run(command_prefix + ['./assembly'])
    
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
                        with open("assembly.s", "w") as f:
                            f.write(".section .data\n")
                            f.write("result_fmt: .string \"Result: %ld\\n\"\n")
                            f.write("\n")
                            f.write(".section .text\n")
                            f.write(".globl main\n")
                            f.write(".type main, @function\n")
                            f.write("main:\n")
                            f.write("    subq $8, %rsp\n")
                            f.write("    # Calculate expression (paste generated assembly code here)\n")
                            f.write("\n".join(assembly_code) + "\n")
                            f.write("    # End of calculation\n")
                            f.write("\n")
                            f.write("    # Print the result\n")
                            f.write("    movq %rax, %rsi\n")
                            f.write("    movq $result_fmt, %rdi\n")
                            f.write("    movq $0, %rax\n")
                            f.write("    call printf\n")
                            f.write("\n")
                            f.write("    # Exit\n")
                            f.write("    addq $8, %rsp # restore stack\n")
                            f.write("    movq $0, %rax\n")
                            f.write("    retq\n")
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
                    with open("assembly.s", "w") as f:
                        f.write(".section .data\n")
                        f.write("result_fmt: .string \"Result: %ld\\n\"\n")
                        f.write("\n")
                        f.write(".section .text\n")
                        f.write(".globl main\n")
                        f.write(".type main, @function\n")
                        f.write("main:\n")
                        f.write("    subq $8, %rsp\n")
                        f.write("    # Calculate expression (paste generated assembly code here)\n")
                        f.write("\n".join(assembly_code) + "\n")
                        f.write("    # End of calculation\n")
                        f.write("\n")
                        f.write("    # Print the result\n")
                        f.write("    movq %rax, %rsi\n")
                        f.write("    movq $result_fmt, %rdi\n")
                        f.write("    movq $0, %rax\n")
                        f.write("    call printf\n")
                        f.write("\n")
                        f.write("    # Exit\n")
                        f.write("    addq $8, %rsp # restore stack\n")
                        f.write("    movq $0, %rax\n")
                        f.write("    retq\n")
                    runAssembly()
                else:
                    interpreter = Interpreter(parser, symbol_table)
                    result = interpreter.interpret()
                    if isinstance(result, dict):
                        symbol_table = result
                    else:
                        print(f'Result: {result}')
        except Exception as e:
            print(f"Error: {e}")

runAssembly()