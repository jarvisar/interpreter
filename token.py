# token.py

# Token types
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
FUNCTION = 'FUNCTION'
ID = 'ID'
DECIMAL_POINT = 'DECIMAL_POINT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
MODULO = 'MODULO'
EXPONENTIATION = 'EXPONENTIATION'
FLOOR_DIVIDE = 'FLOOR_DIVIDE'
LOG = 'LOG'
EXP = 'EXP'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
