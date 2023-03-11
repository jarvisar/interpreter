.section .data
result_fmt: .string "Result: %ld\n"

.section .text
.globl main
.type main, @function
main:
    subq $8, %rsp
    # Calculate expression (paste generated assembly code here)
    movq $8, %rax
    pushq %rax
    movq $9000, %rax
    pushq %rax
    movq $2, %rax
    movq %rax, %rbx
    popq %rax
    movq %rax, %rcx
    movq $1, %rax
    cmpq $0, %rbx
    je .exponentiation_1_done
    .exponentiation_1_loop:
    testq $1, %rbx
    jz .exponentiation_1_square
    imulq %rcx, %rax
    .exponentiation_1_square:
    imulq %rcx, %rcx
    shr $1, %rbx
    jnz .exponentiation_1_loop
    .exponentiation_1_done:
    movq %rax, %rbx
    popq %rax
    addq %rbx, %rax
    # End of calculation

    # Print the result
    movq %rax, %rsi
    movq $result_fmt, %rdi
    movq $0, %rax
    call printf

    # Exit
    addq $8, %rsp # restore stack
    movq $0, %rax
    retq
