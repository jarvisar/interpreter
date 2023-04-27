const   dd 1000.0
.section .data
result_fmt: .string "Result: %.1f\n"

.section .text
.globl main
.type main, @function
main:
subq $8, %rsp
movss xmm0,[const]
movq $2, %rax
movq %rax, %xmm1
addsd %xmm1, %xmm0
movq %xmm0, %rdi
movq $result_fmt, %rax
call printf
addq $8, %rsp
xorq %rax, %rax
retq