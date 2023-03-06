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
        elif node.op.type == EXPONENTIATION:
            self.result.append("movq $1, %rcx")
            self.result.append("cmpq $0, %rbx")
            self.result.append("je .exponentiation_done")
            self.result.append(".exponentiation_loop:")
            self.result.append("testq %rbx, %rbx")
            self.result.append("je .exponentiation_done")
            self.result.append("shr $1, %rbx")
            self.result.append("jnc .exponentiation_square")
            self.result.append("imulq %rax, %rcx")
            self.result.append(".exponentiation_square:")
            self.result.append("imulq %rax, %rax")
            self.result.append("jmp .exponentiation_loop")
            self.result.append(".exponentiation_done:")

    def visit_FuncCall(self, node: FuncCall):
        self.visit(node.arg)
        if node.func == "sqrt":
            self.result.append("movq $0, %rax")
            self.result.append("movq %xmm0, %xmm1")
            self.result.append("sqrtsd %xmm1, %xmm0")
            self.result.append("movq %rax, %xmm0")
        elif node.func == "sin":
            self.result.append("movq $0, %rax")
            self.result.append("movq %xmm0, %xmm1")
            self.result.append("call sin")
            self.result.append("movq %rax, %xmm0")
        elif node.func == "cos":
            self.result.append("movq $0, %rax")
            self.result.append("movq %xmm0, %xmm1")
            self.result.append("call cos")
            self.result.append("movq %rax, %xmm0")
        elif node.func == "tan":
            self.result.append("movq $0, %rax")
            self.result.append("movq %xmm0, %xmm1")
            self.result.append("call tan")
            self.result.append("movq %rax, %xmm0")

    def generate_code(self) -> List[str]:
        tree = self.parser.expr()
        self.visit(tree)
        self.result.append("retq")
        return self.result
