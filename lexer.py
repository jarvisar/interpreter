from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF
from ast import Num, BinOp, FuncCall, AST, Node

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Check for decimal point
        if self.current_char == '.':
            result += self.current_char
            self.advance()

            # Continue reading digits after decimal point
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def floor_divide(self):
        self.advance()
        self.advance()
        return Token(FLOOR_DIVIDE, '//')

    def exponentiation(self):
        self.advance()
        self.advance()
        return Token(EXPONENTIATION, '**')

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char == '.':
                return self.float()

            if self.current_char == '/' and self.peek() == '/':
                return self.floor_divide()

            if self.current_char == '*' and self.peek() == '*':
                return self.exponentiation()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            if self.current_char == '//':
                self.advance()
                return Token(FLOOR_DIVIDE, '//')

            if self.current_char == '%':
                self.advance()
                return Token(MODULO, '%')

            if self.current_char == '^':
                self.advance()
                return Token(EXPONENTIATION, '^')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == 's' and self.text[self.pos:self.pos+3] == 'sin':
                self.advance()
                self.advance()
                self.advance()
                self.skip_whitespace()
                return Token(ID, 'sin')

            if self.current_char == 'c' and self.text[self.pos:self.pos+3] == 'cos':
                self.advance()
                self.advance()
                self.advance()
                self.skip_whitespace()
                return Token(ID, 'cos')

            if self.current_char == 't' and self.text[self.pos:self.pos+3] == 'tan':
                self.advance()
                self.advance()
                self.advance()
                self.skip_whitespace()
                return Token(ID, 'tan')

            if self.current_char == 's' and self.text[self.pos:self.pos+4] == 'sqrt':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.skip_whitespace()
                return Token(ID, 'sqrt')

            self.error()

        return Token(EOF, None)

