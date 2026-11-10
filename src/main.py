"""
Main entry point for the Linen Interpreter.

Pipeline: source text -> Lexer -> tokens -> Parser -> AST -> Interpreter -> output
Exit status: 0 on success, 1 on any lexical, syntax, or runtime error.
"""

import sys

from lexer import Lexer, LexicalError
from parser import Parser, ParseError
from interpreter import Interpreter


def run_source(source: str) -> bool:
    """Run a Linen program from a string. Returns True if it completed without error."""
    try:
        tokens = Lexer(source).tokenize()      # Lexical analysis
        ast = Parser(tokens).parse()           # Parsing
    except (LexicalError, ParseError) as e:
        print(e)
        return False
    return Interpreter().interpret(ast)        # Interpretation


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)

    filename = sys.argv[1]
    sys.setrecursionlimit(20000)   # room for deep (but bounded) Linen recursion

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    try:
        ok = run_source(source)
    except Exception as e:  # a bug in the interpreter itself, not in the Linen program
        print(f"Internal Error: {e}")
        ok = False
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
