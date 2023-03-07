from typing import List
from ast import Num, BinOp, FuncCall, AST
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF

class CodeGenerator:
    def __init__(self, parser):
        self.parser = parser
        self.result = []

    def visit(self, node: AST):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST):
        raise NotImplementedError(f"No visit_{type(node).__name__} method")

    def visit_Num(self, node: Num):
        self.result.append(f"movq ${node.value}, %rax")

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
            self.result.append("movq %rax, %rcx")
            self.result.append("movq $1, %rax")
            self.result.append("cmpq $0, %rbx")
            self.result.append("je .exponentiation_done")
            self.result.append(".exponentiation_loop:")
            self.result.append("testq $1, %rbx")
            self.result.append("jz .exponentiation_square")
            self.result.append("imulq %rcx, %rax")
            self.result.append(".exponentiation_square:")
            self.result.append("imulq %rcx, %rcx")
            self.result.append("shr $1, %rbx")
            self.result.append("jnz .exponentiation_loop")
            self.result.append(".exponentiation_done:")

    def visit_FuncCall(self, node: FuncCall):
        self.visit(node.arg)
        if node.func == "sqrt":
            self.result.append("cvtsi2sd %rax, %xmm0")
            self.result.append("sqrtsd %xmm0, %xmm0")
            self.result.append("cvtsd2si %xmm0, %rax")
        elif node.func == "sin":
            self.result.append("movq %rax, %xmm0")
            self.result.append("call sin")
            self.result.append("movq %xmm0, %rax")
        elif node.func == "cos":
            self.result.append("movq %rax, %xmm0")
            self.result.append("call cos")
            self.result.append("movq %xmm0, %rax")
        elif node.func == "tan":
            self.result.append("movq %rax, %xmm0")
            self.result.append("call tan")
            self.result.append("movq %xmm0, %rax")

    def generate_code(self) -> List[str]:
        tree = self.parser.expr()
        self.visit(tree)
        return self.result
