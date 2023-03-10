from typing import List
from ast import Num, BinOp, FuncCall, AST, UnaryOp, Var
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, LOG, EXP, FACTORIAL

class CodeGenerator:

    def __init__(self, parser, symbol_table):
        self.parser = parser
        self.symbol_table = symbol_table
        self.result = []
        self.counter = 0 # counter for exponentiation

    def visit(self, node: AST):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST):
        raise NotImplementedError(f"No visit_{type(node).__name__} method")

    def visit_Num(self, node: Num):
        self.result.append(f"movq ${node.value}, %rax")
    
    def visit_Var(self, node: Var):
        self.result.append(f"movq ${int(self.symbol_table[node.name.value])}, %rax")

    # Binary operators
    def visit_BinOp(self, node: BinOp):
        self.visit(node.left)
        self.result.append("pushq %rax")
        self.visit(node.right)
        self.result.append("movq %rax, %rbx")
        self.result.append("popq %rax")
        if node.op.type == PLUS:
            self.result.append("addq %rbx, %rax")
        elif node.op.type == MINUS:
            self.result.append("subq %rbx, %rax")
        elif node.op.type == MULTIPLY:
            self.result.append("imulq %rbx, %rax")
        elif node.op.type == DIVIDE:
            self.result.append("cqto")
            self.result.append("idivq %rbx")
        elif node.op.type == MODULO:
            self.result.append("cqto")
            self.result.append("idivq %rbx")
            self.result.append("movq %rdx, %rax")
        elif node.op.type == FLOOR_DIVIDE:
            self.result.append("cqto")
            self.result.append("idivq %rbx")
        elif node.op.type == EXPONENTIATION:
            self.counter += 1 # increment the counter
            exponentiation_label = f".exponentiation_{self.counter}"
            self.result.append(f"movq %rax, %rcx")
            self.result.append("movq $1, %rax")
            self.result.append("cmpq $0, %rbx")
            self.result.append(f"je {exponentiation_label}_done")
            self.result.append(f"{exponentiation_label}_loop:")
            self.result.append("testq $1, %rbx")
            self.result.append(f"jz {exponentiation_label}_square")
            self.result.append("imulq %rcx, %rax")
            self.result.append(f"{exponentiation_label}_square:")
            self.result.append("imulq %rcx, %rcx")
            self.result.append("shr $1, %rbx")
            self.result.append(f"jnz {exponentiation_label}_loop")
            self.result.append(f"{exponentiation_label}_done:")

    # Functions
    def visit_FuncCall(self, node: FuncCall):
        self.visit(node.arg)
        if node.func == "sqrt":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("sqrtsd %xmm0, %xmm0")
            self.result.append("cvttsd2si %xmm0, %rax")
        elif node.func == "sin":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("call sin")
            self.result.append("cvttsd2si %xmm0, %rax")
        elif node.func == "cos":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("call cos")
            self.result.append("cvttsd2si %xmm0, %rax")
        elif node.func == "tan":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("call tan")
            self.result.append("cvttsd2si %xmm0, %rax")
        elif node.func == "log":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("call log")
            self.result.append("cvttsd2si %xmm0, %rax")
        elif node.func == "exp":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("call exp")
            self.result.append("cvttsd2si %xmm0, %rax")

    # Unary Operators
    def visit_UnaryOp(self, node: UnaryOp):
        if node.op.type == MINUS:
            self.visit(node.expr)
            self.result.append("movq $0, %rbx")
            self.result.append("subq %rax, %rbx") # Subtract from 0 if negative
            self.result.append("movq %rbx, %rax")
        elif node.op.type == FACTORIAL:
            self.counter += 1 # increment the counter
            factorial_label = f".factorial_{self.counter}"
            self.visit(node.expr)
            self.result.append("movq %rax, %rcx")
            self.result.append("movq $1, %rax")
            self.result.append("cmpq $0, %rcx")
            self.result.append(f"je {factorial_label}_done")
            self.result.append(f"{factorial_label}_loop:")
            self.result.append("imulq %rcx, %rax")
            self.result.append("decq %rcx")
            self.result.append(f"jnz {factorial_label}_loop")
            self.result.append(f"{factorial_label}_done:")
        
    def generate_code(self) -> List[str]:
        tree = self.parser.expr()
        self.visit(tree)
        return self.result
