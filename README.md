# CS390---Linen
Group 6's CS 390 Final Project Repository for designing and building a Mini Programming Language Interpreter.

---

## Lexer 

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
