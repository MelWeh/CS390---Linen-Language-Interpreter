"""
Converts Linen source code into a list of Token objects.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, Optional

# ======================================================================
# SECTION 1: TOKEN DEFINITIONS
# ======================================================================

class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    IS = auto()
    FUNC = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Type keywords
    TYPE_INT = auto()
    TYPE_FLOAT = auto()
    TYPE_BOOL = auto()
    TYPE_STRING = auto()

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    STAR = auto()          # *
    SLASH = auto()         # /
    MODULO = auto()        # %
    ASSIGN = auto()        # =
    EQUALS = auto()        # ==
    NOT_EQUALS = auto()    # !=
    LESS = auto()          # <
    GREATER = auto()       # >
    LESS_EQUAL = auto()    # <=
    GREATER_EQUAL = auto() # >=
    AND_OP = auto()        # &&
    OR_OP = auto()         # ||
    NOT_OP = auto()        # !
    ARROW = auto()         # ->

    # Delimiters
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    COMMA = auto()         # ,
    SEMICOLON = auto()     # ;
    COLON = auto()         # :

    # Special
    EOF = auto()


@dataclass
class Token:
    """A single lexical token."""
    type: TokenType
    value: str
    line: int
    column: int
    literal: Optional[Any] = None

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


# Keyword string -> TokenType
KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "is": TokenType.IS,
    "func": TokenType.FUNC,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "int": TokenType.TYPE_INT,
    "float": TokenType.TYPE_FLOAT,
    "bool": TokenType.TYPE_BOOL,
    "string": TokenType.TYPE_STRING,
}


# ======================================================================
# SECTION 2: LEXER IMPLEMENTATION
# ----------------------------------------------------------------------
# TODO (Student A): Implement the Lexer class below.
# ======================================================================


# ======================================================================
# SECTION 3: ERROR HANDLING
# ----------------------------------------------------------------------
# TODO (Student B): Implement lexical error handling below.
# ======================================================================
