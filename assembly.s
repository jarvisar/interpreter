# Example x64 assembly program to print out the result of the expression 2 + (3 * 4) - 1 
# Paste generated assembly code in the main function below to print out the result
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
    movq $3, %rax
    pushq %rax
    movq $4, %rax
    movq %rax, %rbx
    popq %rax
    imulq %rbx, %rax
    movq %rax, %rbx
    popq %rax
    addq %rbx, %rax
    pushq %rax
    movq $1, %rax
    movq %rax, %rbx
    popq %rax
    subq %rbx, %rax
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

# by Adam Jarvis
