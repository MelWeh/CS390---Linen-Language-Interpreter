# CS390---Linen
Group 6's CS 390 Final Project Repository for designing and building a Mini Programming Language Interpreter.

---

# Lexer 

### Overview

`lexer.py` converts Linen source code into a list of `Token` objects printed to the terminal. It handles keywords, identifiers, integer and float literals, string literals, operators, delimiters, and reports lexical errors with line/column information.

### Running the Lexer

From the directory containing `lexer.py` and your `.ln` file, run:

```bash
py lexer.py test1.ln
```

This prints each token to the terminal, one per line, ending with an `EOF` token.

### Example

**1. Given a file `test1.ln` containing:**

```linen
let x: int = 10;
let y: float = 3.14;
let flag: bool = true;
```

**2. Running (via bash/terminal):**

```bash
py lexer.py test1.ln
```

**3. Produces:**

```
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

# Parser

### Overview

`parser.py` converts the tokens produced by `lexer.py` into an Abstract Syntax Tree (AST), printed to the terminal. It handles variable declarations, assignments, print statements, arithmetic and boolean expressions, parenthesized expressions, `if/else`, and `while` loops. Syntax errors are reported with line/column information.

### Running the Parser

From the directory containing `parser.py`, `lexer.py`, and your `.ln` file, run:

```bash
py parser.py test1.ln
```

This prints the AST for the program to the terminal as a single line (because it is a nested tree) starting with ProgramNode(...). If the program contains a syntax or lexical error, the parser prints an error message instead and exits with status 1.

### Example - Arithmetic Precedence

**1. Given a file `test1.ln` containing:**

```linen
let x: int = 2 + 3 * 4;
```

**2. Running (via bash/terminal):**

```bash
py parser.py test1.ln
```

**3. Produces:**

```
ProgramNode([VarDeclNode(x, int, BinaryOpNode(NumberNode(2), TokenType.PLUS, BinaryOpNode(NumberNode(3), TokenType.STAR, NumberNode(4))))])
```

The AST shows the `*` node nested inside the right side of the `+` node,
which confirms that multiplication binds tighter than addition.

**4. Expanded View of AST:**

```
ProgramNode
  VarDeclNode(x, int)
    BinaryOpNode(PLUS)
      NumberNode(2)
      BinaryOpNode(STAR)
        NumberNode(3)
        NumberNode(4)
```

This is a sample view of the `let x: int = 2 + 3 * 4;` AST as an indented tree, instead of a collapsed single line.

### Example - Syntax Error
If a program contains a syntax error, the parser prints a message and exits with status 1:

```
[Syntax Error] line 1, col 9: Expected an expression, got SEMICOLON (';')
```
No AST is printed in this case.

---

# Interpreter

### Overview

`interpreter.py` walks the AST produced by `parser.py` and executes the program, printing output to the terminal. It maintains variables in a scoped environment (symbol table), evaluates arithmetic and boolean expressions with correct precedence, executes `if/else`, `while`, `for-in`, and function definitions/calls, and reports runtime errors with line/column information.

The interpreter is reached through `main.py`, which runs the full pipeline: lex → parse → interpret.

### Running the Interpreter

From the directory containing `main.py`, `parser.py`, `lexer.py`, `ast_nodes.py`, `environment.py`, `interpreter.py`, and your `.linen` file, run:

```bash
py main.py test1.linen
```
This executes the program and prints any `print(...)` output to the terminal. If the program contains a lexical, syntax, or runtime error, the interpreter prints an error message instead and halts.

Linen source files use the `.linen` extension. The extension is not inspected by the interpreter; `main.py` reads whatever path is given.

### Environment / Symbol Table
Variables are stored in an `Environment`, which is a single lexical scope containing a dictionary of names to values plus a link to its parent scope.

- `define(name, value)` introduces a new variable in the current scope (used by `let` and function parameter binding).
- `assign(name, value)` updates an existing variable, searching outward through the parent chain (used by `=`).
- `lookup(name)` reads a variable, searching outward.

New scopes are created for every block, every `if` branch, every loop iteration, and every function call. Lookup walks inner → outer, so a name resolves to the nearest enclosing scope that defines it. Assigning to a name that was never declared raises a runtime error.

### Example - Variables, Arithmetic, and Print

**1. Given a file `test1.linen` containing:**

```linen
let x: int = 10;
let y: int = 20;
let z: int = x + y * 2;
print(x);
print(y);
print(z);
```

**2. Running (via bash/terminal):**

```bash
py main.py test1.linen
```

**3. Produces:**

```
10
20
50
```
`y * 2` is evaluated before `x + ...`, so `z` is `10 + 40 = 50`. Each `print(...)` writes one line.

### Example - Functions and Boolean Logic

**1. Given a file `test2.linen` containing:**

```linen
func max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

let x: int = 3;
let y: int = 7;
let m: int = max(x, y);
let isLarge: bool = (m > 5);
if (isLarge == true) {
    print(m);
} else {
    print(0);
}
```

**2. Running (via bash/terminal):**

```bash
py main.py test2.linen
```

**3. Produces:**

```
7
```

`max(x, y)` is called with `3` and `7` and returns `7`. The boolean `isLarge` is `true`, so `m` is printed.

### Example - While Loop
**1. Given a file `test3.linen` containing:**

```linen
let count: int = 0;
let limit: int = 5;
while (count < limit) {
    print(count);
    count = count + 1;
}
```

**2. Running (via bash/terminal):**

```bash
py main.py test3.linen
```

**3. Produces:**

```
0
1
2
3
4
```

The loop runs five times. The loop variable `count` is declared outside the loop and reassigned each iteration, so the condition eventually becomes `false`.

### Example - Runtime Error (Division by Zero)

**1. Given a file `runtime_error.linen` containing:**

```linen
let x: int = 10;
let y: int = 0;

print(x / y);
```

**2. Running (via bash/terminal):**

```bash
py main.py runtime_error.linen
```

**3. Produces:**

```
[Runtime Error] line 4, col 11: Division by zero
```

The interpreter checks the divisor before performing the division, so execution halts here rather than raising a Python `ZeroDivisionError`. No further statements are executed after the error.
