from typing import List
from ast import Num, BinOp, FuncCall, AST
from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF

class CodeGenerator:
    def __init__(self, parser):
        self.parser = parser
        self.result = []
        self.floating_point_register_count = 0

    def visit(self, node: AST):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST):
        raise NotImplementedError(f"No visit_{type(node).__name__} method")

    def get_floating_point_register(self) -> str:
        if self.floating_point_register_count >= 8:
            raise Exception("Out of floating point registers")
        register = f"%xmm{self.floating_point_register_count}"
        self.floating_point_register_count += 1
        return register

    def visit_Num(self, node: Num):
        if isinstance(node.value, int):
            self.result.append(f"movq ${node.value}, %rax")
        elif isinstance(node.value, float):
            register = self.get_floating_point_register()
            self.result.append(f"movsd ${node.value}, {register}")

    def visit_BinOp(self, node: BinOp):
        self.visit(node.left)
        if isinstance(node.left.value, int):
            self.result.append("pushq %rax")
        elif isinstance(node.left.value, float):
            register = self.get_floating_point_register()
            self.result.append(f"movsd {register}, %xmm0")
        self.visit(node.right)
        if isinstance(node.right.value, int):
            self.result.append("movq %rax, %rbx")
            self.result.append("popq %rax")
        elif isinstance(node.right.value, float):
            register = self.get_floating_point_register()
            self.result.append(f"movsd {register}, %xmm1")
            self.result.append(f"movsd %xmm0, {register}")
        if node.op.type == PLUS:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("addq %rbx, %rax")
            else:
                self.result.append("addsd %xmm1, %xmm0")
        elif node.op.type == MINUS:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("subq %rbx, %rax")
            else:
                self.result.append("subsd %xmm1, %xmm0")
        elif node.op.type == MULTIPLY:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("imulq %rbx, %rax")
            else:
                self.result.append("mulsd %xmm1, %xmm0")
        elif node.op.type == DIVIDE:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("cqto")
                self.result.append("idivq %rbx")
            else:
                self.result.append("divsd %xmm1, %xmm0")
        elif node.op.type == MODULO:
            self.result.append("cqto")
            self.result.append("idivq %rbx")
            self.result.append("movq %rdx, %rax")
        elif node.op.type == FLOOR_DIVIDE:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("cqto")
                self.result.append("idivq %rbx")
            else:
                self.result.append("cvtsd2si %xmm0, %rax")
                self.result.append("cvtsd2si %xmm1, %rbx")
                self.result.append("cqto")
                self.result.append("idivq %rbx")
        elif node.op.type == EXPONENT:
            if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                self.result.append("movq %rax, %rbx")
                self.result.append("movq $1, %rax")
                self.result.append("cmpq $0, %rbx")
                self.result.append("je .done")
                self.result.append(".loop:")
                self.result.append("imulq %rax, %rax")
                self.result.append("decq %rbx")
                self.result.append("jne .loop")
                self.result.append(".done:")




    def generate_code(self) -> List[str]:
        tree = self.parser.expr()
        self.visit(tree)
        return self.result
