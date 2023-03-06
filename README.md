# Arithmetic Interpreter
This application is a basic arithmetic interpreter that takes in mathematical expressions as input and evaluates them.

### Lexer
The input expression is first converted into a token stream by the lexer, which identifies the different parts of the expression, such as numbers and operators.

### Parser
The token stream is then parsed by the parser, which creates a tree of nodes that represents the expression. The tree is made up of two types of nodes: Num nodes, which represent individual numbers in the expression, and BinOp nodes, which represent binary operations between two sub-expressions. Each BinOp node has a left child node and a right child node, which can be either Num or BinOp nodes themselves, depending on the complexity of the expression.

Example abstract syntax tree (AST) for `4 + 2 * 10 + 3 * (5 + 1)`:

<p align="center">
  <img src="https://keleshev.com/abstract-syntax-tree-an-example-in-c/ast.svg"/>
</p>

### Interpreter
Once the parser has constructed the tree of nodes, the Interpreter class is used to evaluate the expression. The Interpreter class contains a method called visit, which recursively traverses the tree of nodes and computes the final value of the expression. The visit method performs a different operation depending on the type of node it is currently visiting.

If it encounters a Num node, it simply returns the value of the number. If it encounters a BinOp node, it performs the appropriate arithmetic operation based on the type of operator, and recursively calls visit on the left and right child nodes to compute their values.

Finally, the interpret method of the Interpreter class is called, which initiates the evaluation of the expression. The interpret method calls the expr method of the parser, which constructs the tree of nodes, and then passes the tree to the visit method of the Interpreter to compute the final result. The result is then returned as the output of the interpret method.

### Assembly Code Generator

The generator.py file contains a class called CodeGenerator, which generates assembly code from the AST produced by the parser. The CodeGenerator class defines several methods, each of which handles a specific type of AST node:

* visit_Num: This method generates assembly code for a Num node, which represents a number in the AST. The method moves the value of the number into the %rax register.

* visit_BinOp: This method generates assembly code for a BinOp node, which represents a binary operation (such as addition or multiplication) in the AST. The method recursively visits the left and right operands of the operation, then performs the operation using the appropriate assembly code and stores the result in the %rax register.

* visit_FuncCall: This method generates assembly code for a FuncCall node, which represents a function call in the AST. The method recursively visits the argument to the function call, then generates assembly code to call the appropriate function (such as sin or cos) and stores the result in the %xmm0 register.

The CodeGenerator class also defines a generate_code method, which takes an expression and returns a list of assembly instructions that can be executed by a processor. This method creates an AST from the expression using the parser, then visits the nodes of the AST using the appropriate methods in the CodeGenerator class to generate the corresponding assembly code.

### Features
Overall, this application provides a basic implementation of an arithmetic interpreter, which is capable of evaluating simple mathematical expressions. It demonstrates the use of a lexer and parser to break down the input expression into tokens and construct a tree of nodes that represents the expression, and the use of an interpreter to traverse the tree and compute the final value of the expression.

Currently, it supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).

It also supports several functions, such as sin, cos, tan, and sqrt.

Works with integers, decimals, and negative numbers. Also supports parentheses, e.g. `(3 + 4) / 5` outputs `1.4` and `3 + 4 / 5` outputs `3.8`.

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
    
    `14`
    
    
    `>> cos(0)`
    
    `1.0`
     
### Known Issues

Currently the interpreter has trouble generating Assembly code for functions (sin, cos, tan, sqrt) and floor division (//).

Also plan to implement unary operators, e.g. negative signs in front of paranetheses: `-(5 + 3) = -8`
