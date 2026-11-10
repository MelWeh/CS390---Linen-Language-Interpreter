# CS390 --- Linen

Group 6's CS 390 Final Project Repository for designing and building a Mini Programming Language Interpreter.

---

## Language Name

**Linen** --- a statically typed, imperative programming language with a clean, readable syntax inspired by Python and C-style control flow. Linen supports variables, arithmetic, boolean logic, conditionals, loops, functions with typed parameters and return values, strings, and user input. It emphasizes clarity through explicit types and block-based structure using braces.

## Group Members

- Melissa Weitekamp
- Jacob Hay
- Hasibur Rahman
- Ilyas Bouchalkha

## Language Features

### Core features

- **Statically typed variables** --- declared with `let` and an explicit type (`int`, `float`, `bool`, `string`)
- **Arithmetic** --- `+`, `-`, `*`, `/`, `%` with correct operator precedence
- **Boolean logic** --- `&&`/`and`, `||`/`or`, `!`/`not`, plus comparisons (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Conditionals** --- `if` / `else` / `else if`
- **Loops** --- `while` and `for-in`
- **Functions** --- typed parameters, optional `->` return type, `return` statements, recursion, and closures
- **Scope** --- lexical scoping with a parent-chain environment; local and global variables; shadowing via `let`
- **Print** --- `print(expr);` writes to stdout
- **No comments** --- Linen has no comment syntax; `//` is reported as a lexical error

### Extension features

- **Strings** --- string literals in double quotes, `+` concatenation, iteration over a string with `for-in`
- **`for-in` loops** --- iterate over `range(...)` results and strings
- **`break` / `continue`** --- early loop exit and skip-to-next-iteration
- **User input** --- `input(prompt)` reads a line from stdin
- **Statically typed functions** --- parameter and return types checked at call time
- **Type conversion** --- `int(x)`, `float(x)`, `string(x)`, `bool(x)`
- **Built-ins** --- `range(...)`, `input(...)` and the conversion functions available in the global scope

## Installation / Setup Requirements

- **Python 3.10 or later** (uses modern type hints such as `list[Token]` and `tuple[int, None]`)
- No third-party packages are required --- the interpreter uses only the Python standard library (`sys`, `typing`, `dataclasses`, `enum`, `pathlib`)

### Setup

1\. Clone or download the repository.
2\. Ensure `python3` (or `py` on Windows) is on your PATH.
3\. No install step is needed --- all source files are plain Python modules in the same directory.

## How to Run the Interpreter

The full pipeline (lex -> parse -> interpret) is run through `main.py`:

    py main.py <source_file.linen>

On macOS/Linux:

    python3 main.py <source_file.linen>

The interpreter prints any `print(...)` output to the terminal. If the program contains a lexical, syntax, or runtime error, it prints an error message and halts.

You can also run each stage independently:

- Lexer only (prints tokens):

      py lexer.py <source_file.ln>

- Parser only (prints AST):

      py parser.py <source_file.ln>

## How to Execute a Sample Program

1\. Create a file named `hello.linen` containing:

       let x: int = 10;
       let y: int = 20;

       func add(a: int, b: int) -> int {
           return a + b;
       }

       print(add(x, y));

2\. Run it:

       py main.py hello.linen

3\. Expected output:

       30

More sample programs are documented in `docs/architecture.md` (the full language and interpreter reference) and in the `tests/` directory.

## Repository Organization

    .
    |-- main.py                         Entry point: lex -> parse -> interpret
    |-- lexer.py                        Tokenizer (source text -> Token list)
    |-- parser.py                       Recursive-descent parser (tokens -> AST)
    |-- ast_nodes.py                    AST node class definitions
    |-- interpreter.py                  Tree-walking interpreter
    |-- environment.py                  Scope / symbol table (Environment + RuntimeError_)
    |
    |-- docs/
    |   |-- architecture.md             Full interpreter architecture and reference
    |   |-- grammar.md                  Formal BNF/EBNF grammar for Linen
    |   |-- language_specification.md   High-level language design doc
    |   |-- AST Examples.md             Examples of AST 
    |   |-- Linen Token Definitions.md  Token vocabulary reference
    |
    |-- tests/
    |   |-- extend_tests                Test cases for the extension features
    |   |-- final_error_tests           Final submission: 8 intentional-error programs + expected output
    |   |-- final_feature_tests         Final submission: 10 feature programs + expected output
    |   |-- interpreter_tests           Test cases for the interpreter
    |   |-- lexer_tests                 Test cases for the lexer
    |   |-- parser_tests                Test cases for the parser
    |
    |-- README.md                       This file

### File responsibilities

- **main.py** --- reads the source file, invokes the lexer, parser, and interpreter, and reports errors from any stage.
- **lexer.py** --- character-by-character scanner producing `Token` objects with line/column info; reports `LexicalError`.
- **parser.py** --- recursive-descent parser using a precedence table for binary operators; produces the AST; reports `ParseError`.
- **ast_nodes.py** --- dataclass-like node classes: `ProgramNode`, `VarDeclNode`, `AssignmentNode`, `PrintNode`, `IfNode`, `WhileNode`, `ForNode`, `FuncDefNode`, `FuncCallNode`, `ReturnNode`, `BreakNode`, `ContinueNode`, `BlockNode`, `BinaryOpNode`, `UnaryOpNode`, `NumberNode`, `StringNode`, `BooleanNode`, `VariableNode`.
- **interpreter.py** --- executes the AST, evaluates expressions, manages scope, handles control flow (`return`/`break`/`continue`) via internal exceptions, and reports `RuntimeError_`.
- **environment.py** --- the `Environment` class (name -> value map + parent pointer) and the `RuntimeError_` exception type.

## Documentation

- **docs/architecture.md** --- full reference for the lexer, parser, interpreter, scope model, functions, extension features, and test programs.
- **grammar.md** --- formal BNF/EBNF grammar.
- **language_specification.md** --- high-level design (keywords, operators, syntax examples, sample programs).
- **Linen Token Definitions.md** --- token vocabulary (keyword/operator/delimiter -> TokenType).
