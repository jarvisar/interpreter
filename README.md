# Arithmetic Interpreter & Assembly Code Generator
An arithmetic interpreter and compiler for evaluating mathematical expressions and generating x86-64 assembly code.

This program consists of four main steps:

### Lexer
The input expression is first converted into a token stream by the lexer, which identifies the different parts of the expression (such as numbers, operators, functions, and variables).

### Parser
The token stream is then parsed by the parser, which creates a tree of nodes that represents the expression. The tree is made up of three types of nodes: 

* Num nodes: represent individual numbers in the expression
* Var nodes: represent variables with a sub-expression as a value
* BinOp nodes: represent binary operations between two sub-expressions
* FuncCall nodes: represent mathematical functions such as sine, cosine, and tangent 
* UnaryOp nodes: represent unary operations on a single sub-expression

Each BinOp node has a left child node and a right child node, which can be any of the nodes types themselves (such as a number or another BinOp), depending on the complexity of the expression. Similarly, each FuncCall node has a function name and argument, which tells the interpreter/generator to perform the specified function with the given argument(s).

Example abstract syntax tree (AST) for `4 + 2 * 10 + 3 * (5 + 1)`:

<p align="center">
  <img src="https://keleshev.com/abstract-syntax-tree-an-example-in-c/ast.svg"/>
</p>

### Interpreter
Once the parser has constructed the tree of nodes, the Interpreter class is used to evaluate the expression. The Interpreter class contains a method called visit, which recursively traverses the tree of nodes and computes the final value of the expression. The visit method performs a different operation depending on the type of node it is currently visiting.

If it encounters a Num or Var node, it simply returns the value of the number or variable. If it encounters a BinOp node, it performs the appropriate arithmetic operation based on the type of operator, and recursively calls visit on the left and right child nodes to compute their values. If it encounters a FuncCall node, it performs the specified function with the given argument(s). Additionally, if it encounters a UnaryOp node, it performs the specified operation on the sub-expression.

Finally, the interpret method of the Interpreter class is called, which initiates the evaluation of the expression. The interpret method calls the expr method of the parser, which constructs the tree of nodes, and then passes the tree to the visit method of the Interpreter to compute the final result. The result is then returned as the output of the interpret method.

### Assembly Code Generator

The `generator.py` file contains a class called CodeGenerator, which generates x86-64 assembly code from the AST produced by the parser. The CodeGenerator class defines several methods, each of which handles a specific type of AST node:

* visit_Num: This method generates assembly code for a Num node, which represents a number in the AST. The method moves the value of the number into the %rax register.

* visit_Var: This method generates assembly code for a Var node, which represents a variable in the AST. The method copies the value of the variable from the symbol table into the %rax register.

* visit_BinOp: This method generates assembly code for a BinOp node, which represents a binary operation (such as addition or multiplication) in the AST. The method recursively visits the left and right operands of the operation, then performs the operation using the appropriate assembly code and stores the result in the %rax register.

* visit_FuncCall: This method generates assembly code for a FuncCall node, which represents a function call in the AST. The method recursively visits the argument to the function call, then generates assembly code to call the appropriate function (such as sin or cos) and stores the result in the %xmm0 register.

* visit_UnaryOp: This method generates assembly code for a UnaryOp node, which represents a unary operation (such as negation or factorials) in the AST. The method recursively visits the sub-expression of the node, then performs the operation using the appropriate assembly code and stores the result in the %rax register.

The CodeGenerator class also defines a generate_code method, which takes an expression and returns a list of assembly instructions that can be executed by a processor. This method creates an AST from the expression using the parser, then visits the nodes of the AST using the appropriate methods in the CodeGenerator class to generate the corresponding assembly code.

The CodeGenerator outputs a list of x86-64 assembly instructions corresponding to the user's input expression. The included `assembly.s` file contains a set of initial assembly code to print the result of the assembly calculation. To compile and execute it, refer to the instructions below.

### Features
Overall, this application provides a basic implementation of an arithmetic interpreter capable of evaluating and generating x86-64 assembly code for simple mathematical expressions. It demonstrates the use of a lexer and parser to break down the input expression into tokens and construct a tree of nodes that represents the expression, an interpreter to traverse the tree and compute the final value of the expression, and a code generator to traverse the tree and generate assembly code for the given expression.

Currently, it supports binary operations such addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).

It also supports several functions, such as sin, cos, tan, sqrt, log, and exp. Also supports unary operations, such as factorials and negatives with non-numbers. E.g. `-(2 + 3)` outputs `-5`

Works with integers, decimals, and negative numbers. Also supports parentheses, e.g. `(3 + 4) / 5` outputs `1.4` and `3 + 4 / 5` outputs `3.8`.

Users can also define custom variables by assigning them values, e.g. entering `x = 45` and `y = 3 ** 3` and running `x + y` will output `72`. The assembly generator also supports defined variables.

### How to Use

To use the arithmetic interpreter, follow these steps:

1. Clone the repository to your local machine using the following command:

	`git clone https://github.com/jarvisar/interpreter.git`
    
2. Change directory into the root folder of the cloned repository:

	`cd interpreter`
    
3. Run the main.py file to start the interpreter:

	`python main.py`
    
4. Once the interpreter is running, you can enter mathematical expressions to evaluate. For example:

	`>> (2 + 3) * 4`
    
    `20`
    
    
    `>> cos(0)`
    
    `1.0`
    
5. To generate assembly code for a given expression, press 2 after entering the input. The assembly code should be printed to the terminal.

6. To test the generated code, add the generated code to the the included `assembly.s` file. Paste the code in the "Calculate expression" section, before the result is printed. To run the assembly code, use the following commands:

	`$ as -o assembly.o assembly.s --64`
	
	`$ gcc -shared -o assembly assembly.o -lm -no-pie`
	
	`$ ./assembly`
	
  <b>Note:</b> The assembly.s file may need to be modified to ensure compatibility with the system architecture or operating system of the computer it is being run on.
     
### Known Issues & Limitations

The x86-64 assembly code generator is limited to integers and will round all calculations to the nearest whole number. However, the included interpreter is capable of handling decimals.

## Reflection

Working on this project has been an excellent learning opportunity, allowing me to improve my programming skills and gain a deeper understanding of various concepts in computer science. Creating the lexer and parser helped me better understand how programming languages are parsed and executed, and allowed me to gain a better understanding of how syntax affects the overall structure of a program. Creating the code generator allowed me to learn more about assembly language and understand how it interacts with hardware. This project also allowed me to gain experience working with abstract data structures such as syntax trees, and I hope to apply these skills to build more complex software in the future. Overall, this project has been a great way to improve my skills and deepen my understanding of fundemental computer science concepts.
