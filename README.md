# Interpreter & Custom Programming Language
This project is a custom-built programming language developed to gain more experience in software design and development. It features a lexer, parser, semantic analyzer, interpreter, and code generator for x86-64 assembly code. Users can write and execute code using the included interpreter or Assembly code generator, both of which output the same result. This repository contains the source code and instructions on how to use it.

<br>
<p align="center">
  <img src="https://i.imgur.com/Vjhp5Ct.png"/>
</p>

### Lexer
The input expression is first converted into a token stream by the lexer, which identifies the different parts of the expression (such as numbers, operators, functions, and variables).

### Parser
The token stream is then parsed by the parser, which creates a tree of nodes that represents the expression. The tree is made up of several types of nodes: 

* Num nodes: represent individual numbers in the expression
* Var nodes: represent variables with a sub-expression as the value
* BinOp nodes: represent binary operations between two sub-expressions
* FuncCall nodes: represent functions such as sine, cosine, and tangent 
* UnaryOp nodes: represent unary operations on a single sub-expression

Each BinOp node has a left child node and a right child node, which can be any of the nodes types themselves (such as a number or another BinOp), depending on the complexity of the expression. Similarly, each FuncCall node has a function name and argument, which tells the interpreter/generator to perform the specified function with the given argument(s).

Example abstract syntax tree (AST) for `4 + 2 * 10 + 3 * (5 + 1)`:

<p align="center">
  <img src="https://keleshev.com/abstract-syntax-tree-an-example-in-c/ast.svg"/>
</p>

### Interpreter
Once the parser has constructed the tree of nodes, the Interpreter class is used to evaluate the expression. The Interpreter class contains a method called visit, which recursively traverses the tree of nodes and computes the final value of the expression. The visit method performs a different operation depending on the type of node it is currently visiting.

If it encounters a Num or Var node, it simply returns the value of the number or variable. If it encounters a BinOp node, it performs the appropriate arithmetic operation based on the type of operator, and recursively calls visit on the left and right child nodes to compute their values. Similarly, if it encounters a UnaryOp node, it performs the specified operation on the sub-expression. If it encounters a FuncCall node, it performs the specified function with the given argument(s). 

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
Overall, this application provides an implementation of an interpreter and code generator capable of evaluating and generating x86-64 assembly code for user code. It demonstrates the use of a lexer and parser to break down the input expression into tokens and construct a tree of nodes that represents the expression, an interpreter to traverse the tree and compute the final value of the expression, and a code generator to traverse the tree and generate Assembly code for the given expression.

Currently, it supports arithmetic binary operations such addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%). Unary operations such as negation (-) and factorials (!) are also supported.

Logical and comparison operators are also supported, such as and (&&), or (||), not (!), less than or equal to (<=), greater than or equal to (>=), less than (<), greater than (>), equivalent (==), and not equal (!=). 

It also supports several mathematical functions, such as sin, cos, tan, sqrt, log, and exp.

Works with integers, decimals, and negative numbers. Also supports parentheses, e.g. `(3 + 4) / 2` outputs `3.5` and `3 + 4 / 2` outputs `5`. 

###### Note: Assembly generator currently only supports integers

Users can also define custom variables by assigning them values, e.g. entering `x = 45` and `y = 3 ** 3` and running `x + y` with the interpreter will output `72`. The assembly generator also supports defined variables. The symbol table defines several math constants as variables such as pi, Euler's number (e), tau, and infinity (inf) by default.

## How to Use

<p align="center">
  <img width="750" src="https://jarvisar.github.io/assets/img/portfolio/portfolio-details-10-3.gif"/>
</p>

### Requirements

* [Python 3](https://www.python.org/)
* [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) (if using Windows)

### Running the CLI

To use the arithmetic interpreter, follow these steps:

1. Clone the repository to your local machine using the following command:

	`git clone https://github.com/jarvisar/interpreter.git`
    
2. Change directory into the root folder of the cloned repository:

	`cd interpreter`
    
3. Run main.py to start the interpreter:

	`python main.py`
    
4. After the interpreter is running, enter mathematical expressions to evaluate:

	`>> (2 + 3) * 4`
    
    `20`
    
    
    `>> cos(0)`
    
    `1.0`
    
5. To execute the assembly code generated by the interpreter, enter `1` at the prompt after entering an expression. The interpreter will show the result of the calculation after executing the generated assembly code.
6. To print the generated assembly code without executing it, enter `2` at the prompt.
7. To interpret and print the result without generating assembly code, press any key other than `1` or `2`.
8. Input `exit` to exit the program.
     
### Running from a File

The interpreter can also read expressions from a file and execute them. To do so, create a file with a `.jlang` extension and enter expressions in the file, one per line. For example, after creating a file called `example.jlang` with the following contents:

	# Define variables here
	x = 8 
	y = 9,000 # Can also use commas in numbers

	# Add comments using hash symbol

	z = x + y

	# Add semicolon to final calculation to execute assembly code
	sqrt(x) + z;
	
Execute the expressions in the file with the following command:

`python main.py -f example.jlang`
	
The compiler will generate and execute the final expression's assembly code and print out the results. Note that the final expression in the file must end with a semicolon to indicate that assembly code should be generated and executed.
 
### Known Issues & Limitations

The x86-64 assembly code generator is limited to integers and will round all calculations to the nearest whole number. However, the included interpreter is capable of handling decimals.

### Other Examples


 <img width="650" src="https://jarvisar.github.io/assets/img/portfolio/portfolio-details-10-4.gif"/>

