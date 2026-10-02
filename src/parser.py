'''
Parser that converts tokens from lexer.py into an AST.
'''

from typing import List
from lexer import Lexer, Token, TokenType, LexicalError


# ======================================================================
# SECTION 1: AST NODE DEFINITIONS
# ======================================================================



# ======================================================================
# SECTION 2: ERROR HANDLING
# ======================================================================

class ParseError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"[Syntax Error] line {line}, col {column}: {message}")


# ======================================================================
# SECTION 3: PARSER
# ======================================================================

# Binary operator precedence, lowest first.
PRECEDENCE: List[tuple] = [
    (TokenType.OR_OP,),                                            # ||
    (TokenType.AND_OP,),                                           # &&
    (TokenType.EQUALS, TokenType.NOT_EQUALS),                      # == !=
    (TokenType.LESS, TokenType.GREATER,
     TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL),               # < > <= >=
    (TokenType.PLUS, TokenType.MINUS),                             # + -
    (TokenType.STAR, TokenType.SLASH, TokenType.MODULO),           # * / %
]

# Keyword aliases for boolean operators.
KEYWORD_OPS = {
    TokenType.AND: TokenType.AND_OP,
    TokenType.OR:  TokenType.OR_OP,
    TokenType.NOT: TokenType.NOT_OP,
}

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    # Token helpers
    def cur(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def check(self, *types: TokenType) -> bool:
        return self.cur().type in types

    def match(self, *types: TokenType) -> bool:
        if self.check(*types):
            self.advance()
            return True
        return False

    def expect(self, token_type: TokenType, msg: str = "") -> Token:
        """ Consumes the next token if it matches one of the given types, otherwise raises a ParseError. """
        tok = self.cur()
        if tok.type != token_type:
            raise ParseError(msg or f"Expected {token_type.name}, got {tok.type.name}", 
                              tok.line, tok.column,)
        return self.advance()


    # --------------- Top-level parsing methods --------------

    def parse(self):
        stmts = []
        while not self.check(TokenType.EOF):
            stmts.append(self.statement())

        # TODO: return ProgramNode(stmts)
        raise NotImplementedError("ProgramNode not yet defined")


    # ---------------- Statements ----------------

    def statement(self):
        t = self.cur().type
        if t == TokenType.LET:       return self.var_decl()
        if t == TokenType.PRINT:     return self.print_stmt()
        if t == TokenType.IF:        return self.if_stmt()
        if t == TokenType.WHILE:     return self.while_stmt()
        if t == TokenType.LBRACE:    return self.block()
        if t == TokenType.IDENTIFIER: return self.assignment()

        tok = self.cur()
        raise ParseError(
            f"Unexpected token {tok.type.name} at start of statement",
            tok.line, tok.column,
        )

    def var_decl(self):
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER, "Expected variable name after 'let'")
        self.expect(TokenType.COLON, "Expected ':' after variable name")
        ty = self.type_name()
        self.expect(TokenType.ASSIGN, "Expected '=' in variable declaration")
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after declaration")

        # TODO: return VarDeclNode(name.value, ty, value)
        raise NotImplementedError

    def assignment(self):
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN, "Expected '=' in assignment")
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after assignment")

        # TODO: return AssignmentNode(name.value, value)
        raise NotImplementedError

    def print_stmt(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN, "Expected '(' after 'print'")
        expr = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after print expression")
        self.expect(TokenType.SEMICOLON, "Expected ';' after print")

        # TODO: return PrintNode(expr)
        raise NotImplementedError

    def if_stmt(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN, "Expected '(' after 'if'")
        cond = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after if condition")
        then = self.block()
        otherwise = self.block() if self.match(TokenType.ELSE) else None

        # TODO: return IfNode(cond, then, otherwise)
        raise NotImplementedError

    def while_stmt(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN, "Expected '(' after 'while'")
        cond = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after while condition")
        body = self.block()

        # TODO: return WhileNode(cond, body)
        raise NotImplementedError

    def block(self):
        self.expect(TokenType.LBRACE, "Expected '{' to start block")
        stmts = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self.statement())
        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        
        # TODO: return BlockNode(stmts)
        raise NotImplementedError

    def type_name(self) -> str:
        tok = self.cur()
        if tok.type in (TokenType.TYPE_INT, TokenType.TYPE_FLOAT,
                        TokenType.TYPE_BOOL, TokenType.TYPE_STRING):
            return self.advance().value
        raise ParseError(
            f"Expected a type (int, float, bool, string), got {tok.type.name}",
            tok.line, tok.column,
        )


    # ---------------- Expressions ----------------

    def expression(self):
        """Entry point: start at the lowest-precedence level."""
        return self.parse_binary(0)

    def parse_binary(self, level: int):
        """
        Recursive-descent with a precedence table.
        """

        if level >= len(PRECEDENCE):
            return self.parse_primary()

        ops = PRECEDENCE[level]
        left = self.parse_binary(level + 1)

        while KEYWORD_OPS.get(self.cur().type, self.cur().type) in ops:
            op_tok = self.advance()
            right = self.parse_binary(level + 1)
            
            # TODO: left = BinaryOpNode(left, op_tok.type, right)
            raise NotImplementedError("BinaryOpNode not yet defined")

        return left

    def parse_primary(self):
        """Numbers, strings, booleans, variables, parens, unary ops."""
        tok = self.cur()

        if tok.type == TokenType.NUMBER:
            self.advance()

            # TODO: return NumberNode(tok.literal, tok.line, tok.column)
            raise NotImplementedError("NumberNode not yet defined")

        if tok.type == TokenType.STRING:
            self.advance()

            # TODO: return StringNode(tok.literal, tok.line, tok.column)
            raise NotImplementedError("StringNode not yet defined")

        if tok.type in (TokenType.TRUE, TokenType.FALSE):
            self.advance()

            # TODO: return BooleanNode(tok.type == TokenType.TRUE)
            raise NotImplementedError("BooleanNode not yet defined")

        if tok.type == TokenType.IDENTIFIER:
            self.advance()

            # TODO: return VariableNode(tok.value, tok.line, tok.column)
            raise NotImplementedError("VariableNode not yet defined")

        if tok.type == TokenType.LPAREN:
            self.advance()
            inner = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' to close expression")
            return inner

        # Unary: -x, !x, not x
        if tok.type in (TokenType.MINUS, TokenType.NOT_OP, TokenType.NOT):
            self.advance()
            operand = self.parse_primary()

            # TODO: return UnaryOpNode(tok.type, operand)
            raise NotImplementedError("UnaryOpNode not yet defined")

        raise ParseError(
            f"Expected an expression, got {tok.type.name} ({tok.value!r})",
            tok.line, tok.column,
        )


# ======================================================================
# SECTION 4: CONVENIENCE ENTRY POINT
# ======================================================================

def parse(source: str):
    """Lex + parse a source string. Raises LexicalError or ParseError."""
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()

if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) != 2:
        print("Usage: python3 parser.py <source_file>")
        sys.exit(1)

    src = Path(sys.argv[1]).read_text()
    try:
        print(parse(src))
    except (LexicalError, ParseError) as e:
        print(e)
        sys.exit(1)