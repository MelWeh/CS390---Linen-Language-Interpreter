"""
Main entry point for the Linen Interpreter.
"""

import sys

from lexer import Lexer, LexicalError
from parser import Parser, ParseError
from interpreter import Interpreter


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        # Lexical Analysis
        tokens = Lexer(source).tokenize()

        # Parsing
        ast = Parser(tokens).parse()

        # Interpretation
        Interpreter().interpret(ast)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    except (LexicalError, ParseError) as e:
        print(e)

    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()