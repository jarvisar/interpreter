.section .data
    result_fmt: .string "Result: %ld\n"

.section .text
    .globl main
    .type main, @function
main:
    # Calculate expression (paste generated assembly code here)
    movq $3, %rax
    pushq %rax
    movq $4, %rax
    movq %rax, %rbx
    popq %rax
    imulq %rbx, %rax
    pushq %rax
    movq $5, %rax
    pushq %rax
    movq $4, %rax
    movq %rax, %rbx
    popq %rax
    imulq %rbx, %rax
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
    movq $0, %rax
    retq
