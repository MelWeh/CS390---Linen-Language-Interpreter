"""
Converts Linen source code into a list of Token objects.
"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional



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
# ======================================================================

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek(self) -> Optional[str]:
        if self.pos + 1 >= len(self.source):
            return None
        return self.source[self.pos + 1]

    def advance(self) -> None:
        ch = self.current_char()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1

    def skip_whitespace(self) -> None:
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def lex_number(self) -> Token:
        start_line, start_col = self.line, self.col
        num_str = ""
        has_dot = False

        while self.current_char() is not None and (self.current_char().isdigit() or self.current_char() == "."):
            if self.current_char() == ".":
                if has_dot:
                    raise LexicalError("Invalid number with multiple dots", self.line, self.col)
                has_dot = True
            num_str += self.current_char()
            self.advance()

        literal = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, num_str, start_line, start_col, literal)

    def lex_identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.col
        ident = ""

        while self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == "_"):
            ident += self.current_char()
            self.advance()

        if ident in KEYWORDS:
            return Token(KEYWORDS[ident], ident, start_line, start_col)
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)

    def lex_string(self) -> Token:
        start_line, start_col = self.line, self.col
        self.advance()  # skip opening quote
        s = ""
        while self.current_char() is not None and self.current_char() != '"':
            s += self.current_char()
            self.advance()
        if self.current_char() != '"':
            raise LexicalError("Unterminated string literal", start_line, start_col)
        self.advance()  # skip closing quote
        return Token(TokenType.STRING, s, start_line, start_col, s)

    def next_token(self) -> Token:
        self.skip_whitespace()
        ch = self.current_char()

        if ch is None:
            return Token(TokenType.EOF, "", self.line, self.col)

        # Numbers
        if ch.isdigit():
            return self.lex_number()

        # Identifiers / keywords
        if ch.isalpha() or ch == "_":
            return self.lex_identifier_or_keyword()

        # Strings
        if ch == '"':
            return self.lex_string()

        # Two-character operators / delimiters
        line, col = self.line, self.col
        nxt = self.peek()

        if ch == "=" and nxt == "=":
            self.advance(); self.advance()
            return Token(TokenType.EQUALS, "==", line, col)
        if ch == "!" and nxt == "=":
            self.advance(); self.advance()
            return Token(TokenType.NOT_EQUALS, "!=", line, col)
        if ch == "<" and nxt == "=":
            self.advance(); self.advance()
            return Token(TokenType.LESS_EQUAL, "<=", line, col)
        if ch == ">" and nxt == "=":
            self.advance(); self.advance()
            return Token(TokenType.GREATER_EQUAL, ">=", line, col)
        if ch == "&" and nxt == "&":
            self.advance(); self.advance()
            return Token(TokenType.AND_OP, "&&", line, col)
        if ch == "|" and nxt == "|":
            self.advance(); self.advance()
            return Token(TokenType.OR_OP, "||", line, col)
        if ch == "-" and nxt == ">":
            self.advance(); self.advance()
            return Token(TokenType.ARROW, "->", line, col)

        # Single-character tokens
        if ch == "+":
            self.advance()
            return Token(TokenType.PLUS, "+", line, col)
        if ch == "-":
            self.advance()
            return Token(TokenType.MINUS, "-", line, col)
        if ch == "*":
            self.advance()
            return Token(TokenType.STAR, "*", line, col)
        if ch == "/":
            self.advance()
            return Token(TokenType.SLASH, "/", line, col)
        if ch == "%":
            self.advance()
            return Token(TokenType.MODULO, "%", line, col)
        if ch == "=":
            self.advance()
            return Token(TokenType.ASSIGN, "=", line, col)
        if ch == "<":
            self.advance()
            return Token(TokenType.LESS, "<", line, col)
        if ch == ">":
            self.advance()
            return Token(TokenType.GREATER, ">", line, col)
        if ch == "!":
            self.advance()
            return Token(TokenType.NOT_OP, "!", line, col)
        if ch == "(":
            self.advance()
            return Token(TokenType.LPAREN, "(", line, col)
        if ch == ")":
            self.advance()
            return Token(TokenType.RPAREN, ")", line, col)
        if ch == "{":
            self.advance()
            return Token(TokenType.LBRACE, "{", line, col)
        if ch == "}":
            self.advance()
            return Token(TokenType.RBRACE, "}", line, col)
        if ch == "[":
            self.advance()
            return Token(TokenType.LBRACKET, "[", line, col)
        if ch == "]":
            self.advance()
            return Token(TokenType.RBRACKET, "]", line, col)
        if ch == ",":
            self.advance()
            return Token(TokenType.COMMA, ",", line, col)
        if ch == ";":
            self.advance()
            return Token(TokenType.SEMICOLON, ";", line, col)
        if ch == ":":
            self.advance()
            return Token(TokenType.COLON, ":", line, col)

        # Invalid character
        raise LexicalError(f"Invalid character '{ch}'", line, col)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens


# ======================================================================
# SECTION 3: ERROR HANDLING
# ======================================================================

class LexicalError(Exception):
    """Raised when the lexer encounters an invalid character or malformed token."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source_file>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        src = f.read()

    lexer = Lexer(src)
    try:
        for token in lexer.tokenize():
            print(token)
    except LexicalError as e:
        print("LexicalError:", e)
        sys.exit(1)
