from tokens import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP, FACTORIAL, VAR, ASSIGN, KEYWORDS, LE, GE, LT, GT, EQ, NE, AND, OR, NOT
from myast import Num, BinOp, FuncCall, AST, Node, UnaryOp, Var

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type, token_value=None):
        if self.current_token.type == token_type:
            if token_value is None or self.current_token.value == token_value:
                self.current_token = self.lexer.get_next_token()
            else:
                self.error()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        
        if token.type == INTEGER:
            self.eat(INTEGER)
            if self.current_token.type == FACTORIAL:
                op = self.current_token
                self.eat(FACTORIAL)
                # apply factorial operator repeatedly 
                node = UnaryOp(op, Num(token))
                while self.current_token.type == FACTORIAL:
                    op = self.current_token
                    self.eat(FACTORIAL)
                    node = UnaryOp(op, node)
                return node
            return Num(token)
        elif self.current_token.type == VAR:
            var_node = Var(self.current_token, None)
            self.eat(VAR)
            if self.current_token.type == FACTORIAL:
                op = self.current_token
                self.eat(FACTORIAL)
                return UnaryOp(op, var_node)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                var_node.value = self.expr()
            return var_node
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            # check if there is a factorial operator
            if self.current_token.type == FACTORIAL:
                op = self.current_token
                self.eat(FACTORIAL)
                # apply factorial operator repeatedly
                node = UnaryOp(op, node)
                while self.current_token.type == FACTORIAL:
                    op = self.current_token
                    self.eat(FACTORIAL)
                    node = UnaryOp(op, node)
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(Token(MINUS, '-'), self.factor())
            return node
        elif token.type == EXPONENTIATION:
            self.eat(EXPONENTIATION)
            node = self.factor()
            return BinOp(left=Num(Token(INTEGER, '2')), op=EXPONENTIATION, right=node)
        elif token.type == MODULO:
            self.eat(MODULO)
            node = BinOp(left=node, op=token, right=self.factor())
            return node
        elif token.type == ID:
            func_name = self.current_token.value
            self.eat(ID)
            self.eat(LPAREN)
            arg = self.expr()
            self.eat(RPAREN)
            return FuncCall(func_name, arg)
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE, FLOOR_DIVIDE, EXPONENTIATION, MODULO, LE, GE, LT, GT, EQ, NE, AND, OR, NOT):
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
            elif token.type == FACTORIAL:
                self.eat(FACTORIAL)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == LE:
                self.eat(LE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == GE:
                self.eat(GE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == LT:
                self.eat(LT)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == GT:
                self.eat(GT)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == EQ:
                self.eat(EQ)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == NE:
                self.eat(NE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == AND:
                self.eat(AND)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == OR:
                self.eat(OR)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == NOT:
                self.eat(NOT)
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
