# interpreter
This application is a basic arithmetic interpreter that takes in mathematical expressions as input and evaluates them. The input expression is first converted into a token stream by the lexer, which identifies the different parts of the expression, such as numbers and operators. The token stream is then parsed by the parser, which creates a tree of nodes that represents the expression.

The tree is made up of two types of nodes: Num nodes, which represent individual numbers in the expression, and BinOp nodes, which represent binary operations between two sub-expressions. Each BinOp node has a left child node and a right child node, which can be either Num or BinOp nodes themselves, depending on the complexity of the expression.

Once the parser has constructed the tree of nodes, the Interpreter class is used to evaluate the expression. The Interpreter class contains a method called visit, which recursively traverses the tree of nodes and computes the final value of the expression. The visit method performs a different operation depending on the type of node it is currently visiting.

If it encounters a Num node, it simply returns the value of the number. If it encounters a BinOp node, it performs the appropriate arithmetic operation based on the type of operator, and recursively calls visit on the left and right child nodes to compute their values.

Finally, the interpret method of the Interpreter class is called, which initiates the evaluation of the expression. The interpret method calls the expr method of the parser, which constructs the tree of nodes, and then passes the tree to the visit method of the Interpreter to compute the final result. The result is then returned as the output of the interpret method.

Overall, this application provides a basic implementation of an arithmetic interpreter, which is capable of evaluating simple mathematical expressions. It demonstrates the use of a lexer and parser to break down the input expression into tokens and construct a tree of nodes that represents the expression, and the use of an interpreter to traverse the tree and compute the final value of the expression.

Can be used as a starting point for a compiler in the future.

Currently supports addition (+), subtraction (-), multiplication (*), division (/), exponents (**), floor division (//), and modulus (%).

Also supports several functions, such as sin, cos, tan, and sqrt.

Works with integers, decimals, and negative numbers. Also supports parentheses, e.g. `(3 + 4) / 5` outputs `1.4` and `3 + 4 / 5` outputs `3.8`.
