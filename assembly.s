.section .data
result_fmt: .string "Result: %ld\n"

.section .text
.globl main
.type main, @function
main:
    subq $8, %rsp
    # Calculate expression (paste generated assembly code here)
    # Example input: (2 ^ 2)! > sqrt(625)
    movq $2, %rax
    pushq %rax
    movq $2, %rax
    movq %rax, %rbx
    popq %rax
    movq %rax, %rcx
    movq $1, %rax
    cmpq $0, %rbx
    je .exponentiation_2_done
    .exponentiation_2_loop:
    testq $1, %rbx
    jz .exponentiation_2_square
    imulq %rcx, %rax
    .exponentiation_2_square:
    imulq %rcx, %rcx
    shr $1, %rbx
    jnz .exponentiation_2_loop
    .exponentiation_2_done:
    movq %rax, %rcx
    movq $1, %rax
    cmpq $0, %rcx
    je .factorial_1_done
    .factorial_1_loop:
    imulq %rcx, %rax
    decq %rcx
    jnz .factorial_1_loop
    .factorial_1_done:
    pushq %rax
    movq $625, %rax
    cvtsi2sd %rax, %xmm0
    sqrtsd %xmm0, %xmm0
    cvttsd2si %xmm0, %rax
    movq %rax, %rbx
    popq %rax
    cmpq %rbx, %rax
    setg %al
    movzbq %al, %rax
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
