'''
AST Node definitions for the Linen language interpreter.
'''

from typing import List, Optional

# ======================================================================
# AST NODE DEFINITIONS
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
