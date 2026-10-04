'''
Parser that converts tokens from lexer.py into an AST.
'''

from typing import List
from lexer import Lexer, Token, TokenType, LexicalError

# ======================================================================
# SECTION 1: AST NODE DEFINITIONS
# ======================================================================

class ASTNode:
    """Optional base class for clear typing of tree elements."""
    pass

class ProgramNode(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts
    def __repr__(self):
        return f"ProgramNode({self.stmts})"

class VarDeclNode(ASTNode):
    def __init__(self, name, ty, value):
        self.name = name
        self.ty = ty
        self.value = value
    def __repr__(self):
        return f"VarDeclNode({self.name}, {self.ty}, {self.value})"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"AssignmentNode({self.name}, {self.value})"

class FuncCallNode(ASTNode):
    def __init__(self, name, args, line=None, column=None):
        self.name = name
        self.args = args
        self.line = line
        self.column = column
    def __repr__(self):
        return f"FuncCallNode({self.name}, {self.args})"

class PrintNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"PrintNode({self.expr})"

class IfNode(ASTNode):
    def __init__(self, cond, then, otherwise):
        self.cond = cond
        self.then = then
        self.otherwise = otherwise
    def __repr__(self):
        return f"IfNode({self.cond}, {self.then}, {self.otherwise})"

class WhileNode(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f"WhileNode({self.cond}, {self.body})"

class BlockNode(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts
    def __repr__(self):
        return f"BlockNode({self.stmts})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, op_type, right):
        self.left = left
        self.op_type = op_type
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op_type}, {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op_type, operand):
        self.op_type = op_type
        self.operand = operand
    def __repr__(self):
        return f"UnaryOpNode({self.op_type}, {self.operand})"

class NumberNode(ASTNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"StringNode({self.value})"

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BooleanNode({self.value})"

class VariableNode(ASTNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"VariableNode({self.value})"

class FuncDefNode(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params          # list of (name, type) tuples
        self.return_type = return_type  # str or None
        self.body = body
    def __repr__(self):
        return f"FuncDefNode({self.name}, {self.params}, -> {self.return_type}, {self.body})"

class ReturnNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"ReturnNode({self.expr})"

class BreakNode(ASTNode):
    def __repr__(self): return "BreakNode()"

class ContinueNode(ASTNode):
    def __repr__(self): return "ContinueNode()"

class ForNode(ASTNode):
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body
    def __repr__(self):
        return f"ForNode({self.var}, {self.iterable}, {self.body})"

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
# SECTION 3: PARSER SETUP & RECURSIVE DESCENT LOGIC
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
        self.pos = 0

    # Token navigation helpers
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
        """Consumes the next token if it matches, otherwise raises ParseError."""
        tok = self.cur()
        if tok.type != token_type:
            raise ParseError(msg or f"Expected {token_type.name}, got {tok.type.name}", 
                            tok.line, tok.column)
        return self.advance()

# --------------- Top-level parsing methods --------------

    def parse(self) -> ProgramNode:
        stmts = []
        while not self.check(TokenType.EOF):
            stmts.append(self.statement())
        return ProgramNode(stmts)

# ---------------- Statements ----------------

    def statement(self):
        t = self.cur().type
        if t == TokenType.LET:        return self.var_decl()
        if t == TokenType.PRINT:      return self.print_stmt()
        if t == TokenType.IF:         return self.if_stmt()
        if t == TokenType.WHILE:      return self.while_stmt()
        if t == TokenType.LBRACE:     return self.block()
        if t == TokenType.IDENTIFIER: return self.assignment()

        tok = self.cur()
        raise ParseError(
            f"Unexpected token {tok.type.name} at start of statement",
            tok.line, tok.column,
        )

    def var_decl(self) -> VarDeclNode:
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER, "Expected variable name after 'let'")
        self.expect(TokenType.COLON, "Expected ':' after variable name")
        ty = self.type_name()
        self.expect(TokenType.ASSIGN, "Expected '=' in variable declaration")
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after declaration")
        return VarDeclNode(name.value, ty, value)

    def assignment(self) -> AssignmentNode:
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN, "Expected '=' in assignment")
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after assignment")
        return AssignmentNode(name.value, value)

    def print_stmt(self) -> PrintNode:
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN, "Expected '(' after 'print'")
        expr = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after print expression")
        self.expect(TokenType.SEMICOLON, "Expected ';' after print")
        return PrintNode(expr)

    def if_stmt(self) -> IfNode:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN, "Expected '(' after 'if'")
        cond = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after if condition")
        then = self.block()
        otherwise = self.block() if self.match(TokenType.ELSE) else None
        return IfNode(cond, then, otherwise)

    def while_stmt(self) -> WhileNode:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN, "Expected '(' after 'while'")
        cond = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after while condition")
        body = self.block()
        return WhileNode(cond, body)

    def block(self) -> BlockNode:
        self.expect(TokenType.LBRACE, "Expected '{' to start block")
        stmts = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self.statement())
        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        return BlockNode(stmts)

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
        """Recursive-descent engine utilizing the PRECEDENCE table."""
        if level >= len(PRECEDENCE):
            return self.parse_primary()

        ops = PRECEDENCE[level]
        left = self.parse_binary(level + 1)

        while KEYWORD_OPS.get(self.cur().type, self.cur().type) in ops:
            op_tok = self.advance()
            # Normalize keyword aliases (like 'and' -> TokenType.AND_OP)
            normalized_op = KEYWORD_OPS.get(op_tok.type, op_tok.type)

            right = self.parse_binary(level + 1)
            left = BinaryOpNode(left, normalized_op, right)

        return left

    def parse_primary(self):
        """Numbers, strings, booleans, variables, parens, and unary ops."""
        tok = self.cur()

        # Numbers
        if tok.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(tok.literal, tok.line, tok.column)

        # Strings
        if tok.type == TokenType.STRING:
            self.advance()
            return StringNode(tok.value, tok.line, tok.column)

        # Booleans
        if tok.type in (TokenType.TRUE, TokenType.FALSE):
            self.advance()
            return BooleanNode(tok.type == TokenType.TRUE)

        # Identifiers (variables or function calls)
        if tok.type == TokenType.IDENTIFIER:
            ident = self.advance()

            # Function call: foo(x, y)
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.expect(TokenType.RPAREN, "Expected ')' after function call")
                return FuncCallNode(ident.value, args, ident.line, ident.column)

            # Variable reference
            return VariableNode(ident.value, ident.line, ident.column)

        # Parenthesized expression
        if tok.type == TokenType.LPAREN:
            self.advance()
            inner = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' to close expression")
            return inner

        # Unary operations: -x, !x, not x
        if tok.type in (TokenType.MINUS, TokenType.NOT_OP, TokenType.NOT):
            self.advance()
            normalized_op = KEYWORD_OPS.get(tok.type, tok.type)
            operand = self.parse_binary(len(PRECEDENCE))
            return UnaryOpNode(normalized_op, operand)

        # Otherwise: error
        raise ParseError(
            f"Expected an expression, got {tok.type.name} ({tok.value!r})",
            tok.line, tok.column,
        )




# ======================================================================
# SECTION 4: CONVENIENCE ENTRY POINT
# ======================================================================

def parse(source: str) -> ProgramNode:
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