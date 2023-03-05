# Token types
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
DECIMAL_POINT = 'DECIMAL_POINT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
MODULO = 'MODULO'
EXPONENTIATION = 'EXPONENTIATION'
FLOOR_DIVIDE = 'FLOOR_DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

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

            if self.current_char.isdigit() or self.current_char == '.':
                return self.integer()

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

            if self.current_char == '%':
                self.advance()
                return Token(MODULO, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)



class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == EXPONENTIATION:
            self.eat(EXPONENTIATION)
            node = self.factor()
            return BinOp(left=Num(Token(INTEGER, '2')), op=EXPONENTIATION, right=node)
        elif token.type == MODULO:
            self.eat(MODULO)
            node = BinOp(left=node, op=token, right=self.factor())
            return node
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE, FLOOR_DIVIDE, EXPONENTIATION, MODULO):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == FLOOR_DIVIDE:
                self.eat(FLOOR_DIVIDE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == EXPONENTIATION:
                self.eat(EXPONENTIATION)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == MODULO:
                self.eat(MODULO)
                node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node



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
        else:
            raise TypeError("Invalid node type")

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

print("Currently supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).")
print("Works with integers and decimals and supports parentheses, e.g. '(3 + 4) / 5' outputs 1.4 and '3 + 4 / 5' outputs 3.8.")
while True:
    text = input("Enter an arithmetic expression: ")
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)
