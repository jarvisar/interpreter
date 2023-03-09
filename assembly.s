# Example x64 assembly program to print out the result of the expression 2 + (6 / 2)
# Paste generated assembly code into the main function below to print out the result
.section .data
    result_fmt: .string "Result: %ld\n"

.section .text
    .globl main
    .type main, @function
main:
    subq $8, %rsp
    # Calculate expression (paste generated assembly code here)
    movq $2, %rax
    pushq %rax
    movq $6, %rax
    pushq %rax
    movq $2, %rax
    movq %rax, %rbx
    popq %rax
    cqto
    idivq %rbx
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
    addq $8, %rsp # restore stack stack
    movq $0, %rax
    retq

# by Adam Jarvis
