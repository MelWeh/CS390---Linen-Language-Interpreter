from typing import Any, List, Union
from environment import Environment, RuntimeError_
from lexer import TokenType
from parser import (
    ProgramNode, VarDeclNode, AssignmentNode, PrintNode, IfNode, WhileNode,
    BlockNode, BinaryOpNode, UnaryOpNode, NumberNode, StringNode, BooleanNode,
    VariableNode, ASTNode
)

class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def interpret(self, program: ProgramNode) -> None:
        """Main entry point to execute a parsed program."""
        try:
            for stmt in program.stmts:
                self.execute(stmt, self.global_env)
        except RuntimeError_ as e:
            print(e)

    def execute(self, node: ASTNode, env: Environment) -> None:
        """Executes a statement node (does not return a value)."""
        if isinstance(node, VarDeclNode):
            val = self.evaluate(node.value, env)
            self._validate_type(node.ty, val, node.value)
            env.define(node.name, val)

        elif isinstance(node, AssignmentNode):
            # Try to get position metadata from the value node for error reporting
            line, col = self._get_coords(node.value)
            
            # Ensure the variable has been declared first
            if not env.exists(node.name):
                raise RuntimeError_(f"Undefined variable '{node.name}'", line, col)
                
            val = self.evaluate(node.value, env)
            env.assign(node.name, val, line, col)

        elif isinstance(node, PrintNode):
            val = self.evaluate(node.expr, env)
            # Match print format formatting
            if isinstance(val, bool):
                print(str(val).lower())
            else:
                print(val)

        elif isinstance(node, IfNode):
            cond_val = self.evaluate(node.cond, env)
            line, col = self._get_coords(node.cond)
            if not isinstance(cond_val, bool):
                raise RuntimeError_("Condition in 'if' statement must be a boolean", line, col)
            
            if cond_val:
                self.execute(node.then, env.child())
            elif node.otherwise:
                self.execute(node.otherwise, env.child())

        elif isinstance(node, WhileNode):
            line, col = self._get_coords(node.cond)
            while True:
                cond_val = self.evaluate(node.cond, env)
                if not isinstance(cond_val, bool):
                    raise RuntimeError_("Condition in 'while' loop must be a boolean", line, col)
                if not cond_val:
                    break
                self.execute(node.body, env.child())

        elif isinstance(node, BlockNode):
            block_env = env.child()
            for stmt in node.stmts:
                self.execute(stmt, block_env)
        else:
            raise RuntimeError_(f"Unknown statement type: {type(node).__name__}")

    def evaluate(self, node: ASTNode, env: Environment) -> Any:
        """Evaluates an expression node and returns its computed value."""
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, StringNode):
            return node.value

        elif isinstance(node, BooleanNode):
            return node.value

        elif isinstance(node, VariableNode):
            return env.lookup(node.value, node.line, node.column)

        elif isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand, env)
            line, col = self._get_coords(node.operand)

            if node.op_type == TokenType.MINUS:
                if not isinstance(operand, (int, float)):
                    raise RuntimeError_("Unary '-' operator requires a numeric value", line, col)
                return -operand
                
            if node.op_type == TokenType.NOT_OP:
                if not isinstance(operand, bool):
                    raise RuntimeError_("Unary '!'/'not' operator requires a boolean value", line, col)
                return not operand

        elif isinstance(node, BinaryOpNode):
            left_val = self.evaluate(node.left, env)
            right_val = self.evaluate(node.right, env)
            line, col = self._get_coords(node.right)

            # Logical Operator
            if node.op_type == TokenType.AND_OP:
                if not isinstance(left_val, bool) or not isinstance(right_val, bool):
                    raise RuntimeError_("Operator '&&' requires boolean operands", line, col)
                return left_val and right_val
                
            if node.op_type == TokenType.OR_OP:
                if not isinstance(left_val, bool) or not isinstance(right_val, bool):
                    raise RuntimeError_("Operator '||' requires boolean operands", line, col)
                return left_val or right_val

            # Equality Operators
            if node.op_type == TokenType.EQUALS:     return left_val == right_val
            if node.op_type == TokenType.NOT_EQUALS: return left_val != right_val

            # Arithmetic And Comparison Runtime Type Protection
            if type(left_val) != type(right_val) and not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
                raise RuntimeError_(f"Invalid operation matching {type(left_val).__name__} and {type(right_val).__name__}", line, col)

            # Arithmetic
            if node.op_type == TokenType.PLUS:   return left_val + right_val
            if node.op_type == TokenType.MINUS:  return left_val - right_val
            if node.op_type == TokenType.STAR:   return left_val * right_val
            if node.op_type == TokenType.SLASH:
                if right_val == 0:
                    raise RuntimeError_("Division by zero", line, col)
                return left_val / right_val
            if node.op_type == TokenType.MODULO: return left_val % right_val

            # Comparisons
            if node.op_type == TokenType.LESS:          return left_val < right_val
            if node.op_type == TokenType.GREATER:       return left_val > right_val
            if node.op_type == TokenType.LESS_EQUAL:    return left_val <= right_val
            if node.op_type == TokenType.GREATER_EQUAL: return left_val >= right_val

        raise RuntimeError_("Unknown expression node mapping")

    # Helper Utilities
    def _get_coords(self, node: ASTNode) -> tuple[Union[int, None], Union[int, None]]:
        """Safely extract coordinate metrics down the left branch of an expression."""
        if hasattr(node, 'line') and node.line is not None:
            return node.line, node.column
        if hasattr(node, 'left'):
            return self._get_coords(node.left)
        return None, None

    def _validate_type(self, expected_type: str, value: Any, value_node: ASTNode) -> None:
        """Type verification to satisfy the explicit assignment declarations."""
        line, col = self._get_coords(value_node)
        mapping = {"int": int, "float": float, "bool": bool, "string": str}
        
        if expected_type in mapping:
            if not isinstance(value, mapping[expected_type]):
                # Allow promotion of ints to float implicitly if acceptable
                if expected_type == "float" and isinstance(value, int):
                    return
                raise RuntimeError_(f"Type mismatch: Expected '{expected_type}', got value of type '{type(value).__name__}'", line, col)
