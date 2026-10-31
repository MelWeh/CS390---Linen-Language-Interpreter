# Linen --- Architecture

Full architecture for the Linen mini programming language interpreter.

It describes the lexer, parser, interpreter, scope model, functions, extension features, test programs, and grammar pointer. For the formal grammar see `grammar.md`; for the high-level language design see `language_specification.md`; for the token vocabulary see `Linen Token Definitions.md`.

---

## Lexer Overview

lexer.py converts Linen source code into a list of Token objects printed to the terminal. It handles keywords, identifiers, integer and float literals, string literals, operators, delimiters, and reports lexical errors with line/column information.

### Running the Lexer

From the directory containing lexer.py and your .ln file, run:

```linen
py lexer.py test1.ln
```

This prints each token to the terminal, one per line, ending with an EOF token.

### Example

1\. Given a file test1.ln containing:

```linen
let x: int = 10;
let y: float = 3.14;
let flag: bool = true;
```

2\. Running (via bash/terminal):

```linen
py lexer.py test1.ln
```

3\. Produces:

```linen
Token(LET, 'let', line=1, col=1)
Token(IDENTIFIER, 'x', line=1, col=5)
Token(COLON, ':', line=1, col=6)
Token(TYPE_INT, 'int', line=1, col=8)
Token(ASSIGN, '=', line=1, col=12)
Token(NUMBER, '10', line=1, col=14)
Token(SEMICOLON, ';', line=1, col=16)
Token(LET, 'let', line=2, col=1)
Token(IDENTIFIER, 'y', line=2, col=5)
Token(COLON, ':', line=2, col=6)
Token(TYPE_FLOAT, 'float', line=2, col=8)
Token(ASSIGN, '=', line=2, col=14)
Token(NUMBER, '3.14', line=2, col=16)
Token(SEMICOLON, ';', line=2, col=20)
Token(LET, 'let', line=3, col=1)
Token(IDENTIFIER, 'flag', line=3, col=5)
Token(COLON, ':', line=3, col=6)
Token(TYPE_BOOL, 'bool', line=3, col=8)
Token(ASSIGN, '=', line=3, col=13)
Token(TRUE, 'true', line=3, col=15)
Token(SEMICOLON, ';', line=3, col=19)
Token(EOF, '', line=4, col=1)
```

Each line shows the token type, the raw text that produced it, and its line/column position in the source file.

---

## Parser Overview

parser.py converts the tokens produced by lexer.py into an Abstract Syntax Tree (AST), printed to the terminal. It handles variable declarations, assignments, print statements, arithmetic and boolean expressions, parenthesized expressions, if/else, while loops, for-in loops, function definitions, and function calls. Syntax errors are reported with line/column information.

### Running the Parser

From the directory containing parser.py, lexer.py, and your .ln file, run:

```linen
py parser.py test1.ln
```

This prints the AST for the program to the terminal as a single line (because it is a nested tree) starting with ProgramNode(...). If the program contains a syntax or lexical error, the parser prints an error message instead and exits with status 1.

### Example - Arithmetic Precedence

1\. Given a file test1.ln containing:

```linen
let x: int = 2 + 3 * 4;
```

2\. Running (via bash/terminal):

```linen
py parser.py test1.ln
```

3\. Produces:

```linen
ProgramNode([VarDeclNode(x, int, BinaryOpNode(NumberNode(2), TokenType.PLUS, BinaryOpNode(NumberNode(3), TokenType.STAR, NumberNode(4))))])
```

The AST shows the * node nested inside the right side of the + node, which confirms that multiplication binds tighter than addition.

4\. Expanded View of AST:

```linen
    ProgramNode
      VarDeclNode(x, int)
        BinaryOpNode(PLUS)
          NumberNode(2)
          BinaryOpNode(STAR)
            NumberNode(3)
            NumberNode(4)
```

This is a sample view of the "let x: int = 2 + 3 * 4;" AST as an indented tree, instead of a collapsed single line.

### Example - Syntax Error

If a program contains a syntax error, the parser prints a message and exits with status 1:

```linen
[Syntax Error] line 1, col 9: Expected an expression, got SEMICOLON (';')
```

No AST is printed in this case.

---

## Interpreter Overview

interpreter.py walks the AST produced by parser.py and executes the program, printing output to the terminal. It maintains variables in a scoped environment (symbol table), evaluates arithmetic and boolean expressions with correct precedence, executes if/else, while, for-in, and function definitions/calls, and reports runtime errors with line/column information.

The interpreter is reached through main.py, which runs the full pipeline: lex -> parse -> interpret.

### Running the Interpreter

From the directory containing main.py, parser.py, lexer.py, ast_nodes.py, environment.py, interpreter.py, and your .linen file, run:

```linen
py main.py test1.linen
```

This executes the program and prints any print(...) output to the terminal. If the program contains a lexical, syntax, or runtime error, the interpreter prints an error message instead and halts.

Linen source files use the .linen extension. The extension is not inspected by the interpreter; main.py reads whatever path is given.

### Environment / Symbol Table

Variables are stored in an Environment, which is a single lexical scope containing a dictionary of names to values plus a link to its parent scope.

- define(name, value) introduces a new variable in the current scope (used by let and function parameter binding).
- assign(name, value) updates an existing variable, searching outward through the parent chain (used by =).
- lookup(name) reads a variable, searching outward.

New scopes are created for every block, every if branch, every loop iteration, and every function call. Lookup walks inner -> outer, so a name resolves to the nearest enclosing scope that defines it. Assigning to a name that was never declared raises a runtime error.

### Example - Variables, Arithmetic, and Print

1\. Given a file arithmetic.linen containing:

```linen
let x: int = 10;
let y: int = 5;

print(x + y);
print(x - y);
print(x * y);
print(x / y);
```

2\. Running (via bash/terminal):

```linen
py main.py arithmetic.linen
```

3\. Produces:

```linen
15
5
50
2
```

### Example - If Else Logic

1\. Given a file if_else.linen containing:

```linen
let x: int = 10;

if (x >= 10) {
    print(1);
}
else {
    print(0);
}
```

2\. Running (via bash/terminal):

```linen
py main.py if_else.linen
```

3\. Produces:

```linen
1
```

### Example - While Loop

1\. Given a file while_loop.linen containing:

```linen
let x: int = 1;

while (x <= 5) {
    print(x);
    x = x + 1;
}
```

2\. Running (via bash/terminal):

```linen
py main.py while_loop.linen
```

3\. Produces:

```linen
1
2
3
4
5
```

### Example - Runtime Error (Division by Zero)

1\. Given a file runtime_error.linen containing:

```linen
let x: int = 10;
let y: int = 0;

print(x / y);
```

2\. Running (via bash/terminal):

```linen
py main.py runtime_error.linen
```

3\. Produces:

```linen
[Runtime Error] line 4, col 11: Division by zero
```

The interpreter checks the divisor before performing the division, so execution halts here rather than raising a Python ZeroDivisionError. No further statements are executed after the error.

---

## Functions

Linen supports user-defined functions with typed parameters and an optional return type.

### Syntax

```linen
func name(param1: type, param2: type) -> return_type {
    // body
    return value;
}
```

- The return type after -> is optional. A function without -> is void-like and returns None.
- Parameters must be declared with an explicit type (int, float, bool, string).
- A function with a declared return type must execute a return on every path; falling off the end of such a function raises a runtime error ("Function 'name' expected a return value").
- Function arguments are type-checked against the declared parameter types at call time.
- Functions may be recursive.

### Function Example

```linen
func add(a: int, b: int) -> int {
    let result: int = a + b;
    return result;
}

func greet(name: string) {
    print("Hello, " + name);
}

let x: int = add(3, 4);
print(x);          // 7
greet("Linen");    // Hello, Linen
```

### Implementation

- FuncDefNode stores the name, parameter list ([(name, type), ...]), optional return type, and body block.
- Defining a function binds the pair (FuncDefNode, defining_environment) into the current scope. Capturing the defining environment is what makes closures and recursion work.
- A call (FuncCallNode) looks up the name, evaluates the arguments, type-checks them against the declared parameter types, creates a fresh child scope of the defining environment, binds the parameters into that scope, and executes the body. return unwinds via an internal _Return exception, which `_call` catches and type-checks against the declared return type.

---

## Scope

Linen uses lexical (static) scoping with a parent-chain Environment.

### How scope is represented

- The interpreter holds one global_env at the root.
- Environment is a single scope: a Dict[str, Any] of names to values plus a parent pointer.
- Environment.child() creates a new inner scope whose parent is the current scope.
- let calls define, which always introduces a name in the current scope (shadowing any outer name of the same name).
- = calls assign, which searches outward from the current scope to the global scope and updates the nearest existing binding. Assigning to an undeclared name is a runtime error.
- Name lookup searches the current scope first, then walks parent outward. The nearest binding wins.
- New scopes are created for: every block ({ ... }), every if/else branch, every loop iteration, and every function call (via closure.child() -- the closure is the defining environment, not the caller's).

Because function call scopes are children of the defining environment, functions see the names available where they were defined, not where they were called.

### Example - Shadowing

```linen
let x: int = 10;

func test() {
    let x: int = 20;
    print(x);
}

test();
print(x);
```

Output:

```linen
20
10
```

Inside test(), "let x" creates a new binding in the function's local scope; the global x is untouched. After the call, print(x) resolves to the global x = 10.

### Example - Assignment Through Parent Chain

```linen
let counter: int = 0;

func bump() {
    counter = counter + 1;
}

bump();
bump();
print(counter);   // 2
```

bump declares no local counter, so assign walks up to the global scope and updates it.

---

## Extension Features

Beyond the core language, Linen implements the following extension features:

### 1. for-in loops over ranges and strings

```linen
for i in range(0, 5) {
    print(i);          // 0 1 2 3 4
}

for ch in "abc" {
    print(ch);         // a b c
}
```

range and input are built-in callables registered in the global scope. for iterates any list or str; each iteration creates a fresh loop scope binding the loop variable.

### 2. break and continue

```linen
let total: int = 0;
let count: int = 0;

while (true) {
    count = count + 1;
    if (count > 10) { break; }
    if (count % 2 == 0) { continue; }
    total = total + count;
}
print(total);   // 25
```

Implemented with internal `_Break` / `_Continue` exceptions caught by the loop executor. Used outside a loop, they produce a runtime error.

### 3. Strings and string literals

```linen
let greeting: string = "Hello, " + "Linen";
print(greeting);   // Hello, Linen
```

String literals use double quotes. + concatenates two strings. (Escape sequences are not currently supported.)

### 4. User input

```linen
let name: string = input("Enter your name: ");
print("Hello, " + name);
```

input reads a line from stdin and returns it as a string.

### 5. Statically typed functions

Explicit parameter types and optional return types, checked at call time (see the Functions section above).

### Recursion note

Recursion is supported (see test3), but recursion depth is bounded by Python's interpreter stack, since the Linen interpreter is written in Python. Very deep recursion will surface as a Python RecursionError, not a Linen runtime error.

---

## Test Programs

Six test programs exercise functions, scope, and the extension features. Each testN_*.linen file is paired with a testN_*.txt file containing its expected output.

| # | File | Demonstrates | Expected Output |
| --- | ------ | -------------- | ----------------- |
| 1 | test1_functions.linen | Function definitions, parameters, return values, string parameters, calls | 30 / 900 / Hello, Linen |
| 2 | test2_scope.linen | Local vs. global scope, shadowing with let | 20 / 10 |
| 3 | test3_recursion.linen | Recursion (factorial, fib) | 120 / 55 |
| 4 | test4_for_loop.linen | for-in over range and over a string, break, continue | 23 / a / b / c |
| 5 | test5_while_break.linen | while (true) with break and continue | 25 |
| 6 | test6_input.linen | input() and string concatenation | Enter your name: Alice / Hello, Alice |

### Test 1 - Functions

```linen
func add(a: int, b: int) -> int {
    return a + b;
}

func square(x: int) -> int {
    return x * x;
}

func greet(name: string) {
    print("Hello, " + name);
}

let result: int = add(10, 20);
print(result);

print(square(result));

greet("Linen");
```

Output:

```linen
30
900
Hello, Linen
```

### Test 2 - Scope

```linen
let x: int = 10;

func test() {
    let x: int = 20;
    print(x);
}

test();
print(x);
```

Output:

```linen
20
10
```

### Test 3 - Recursion

```linen
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func fib(n: int) -> int {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

print(factorial(5));
print(fib(10));
```

Output:

```linen
120
55
```

### Test 4 - For Loop with Break/Continue and String Iteration

```linen
let sum: int = 0;

for i in range(0, 10) {
    if (i == 5) {
        continue;
    }
    if (i == 8) {
        break;
    }
    sum = sum + i;
}
print(sum);

for ch in "abc" {
    print(ch);
}
```

Output:

```linen
23
a
b
c
```

### Test 5 - While with Break/Continue

```linen
let count: int = 0;
let total: int = 0;

while (true) {
    count = count + 1;
    if (count > 10) {
        break;
    }
    if (count % 2 == 0) {
        continue;
    }
    total = total + count;
}
print(total);
```

Output:

```linen
25
```

### Test 6 - User Input

```linen
let name: string = input("Enter your name: ");
print("Hello, " + name);
```

Sample run (with Alice typed at the prompt):

```linen
Enter your name: Alice
Hello, Alice
```

---
