"""
Tree-walking interpreter for the Linen language.
"""

from typing import Any, List, Union
from environment import Environment, RuntimeError_
from lexer import TokenType
from parser import (
    ProgramNode, VarDeclNode, AssignmentNode, PrintNode, IfNode, WhileNode,
    BlockNode, BinaryOpNode, UnaryOpNode, NumberNode, StringNode, BooleanNode,
    VariableNode, ASTNode, FuncDefNode, FuncCallNode, ReturnNode, ForNode,
    BreakNode, ContinueNode
)

# Small control-flow signals so return/break/continue can unwind execute().
class _Return(Exception):
    def __init__(self, value): self.value = value

class _Break(Exception): pass
class _Continue(Exception): pass


# Type conversion built-ins.
def _to_int(value):
    if isinstance(value, bool):
        raise RuntimeError_("Cannot convert bool to int")
    if isinstance(value, (int, float)):
        return int(value)                      # floats are truncated toward zero
    try:
        return int(value.strip())
    except ValueError:
        raise RuntimeError_(f"Cannot convert \"{value}\" to int")

def _to_float(value):
    if isinstance(value, bool):
        raise RuntimeError_("Cannot convert bool to float")
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value.strip())
    except ValueError:
        raise RuntimeError_(f"Cannot convert \"{value}\" to float")

def _to_string(value):
    return str(value).lower() if isinstance(value, bool) else str(value)

def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value in ("true", "false"):
        return value == "true"
    raise RuntimeError_(f"Cannot convert {value!r} to bool")


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        # Built-in range function
        self.global_env.define(
            "range",
            lambda *a: list(range(*a)),
        )
        # input function
        self.global_env.define(
            "input",
            lambda prompt="": input(prompt),
        )
        # Type conversion functions: int(x), float(x), string(x), bool(x)
        self.global_env.define("int", _to_int)
        self.global_env.define("float", _to_float)
        self.global_env.define("string", _to_string)
        self.global_env.define("bool", _to_bool)

    def interpret(self, program: ProgramNode) -> None:
        """Main entry point to execute a parsed program."""
        try:
            for stmt in program.stmts:
                self.execute(stmt, self.global_env)
            return True
        # Handle top-level control-flow signals as runtime errors.
        except _Return:
            print(RuntimeError_("'return' outside of function"))
        except _Break:
            print(RuntimeError_("'break' outside of loop"))
        except _Continue:
            print(RuntimeError_("'continue' outside of loop"))
        except RuntimeError_ as e:
            print(e)
        except RecursionError:
            print(RuntimeError_("Maximum recursion depth exceeded"))
        return False

    def execute(self, node: ASTNode, env: Environment) -> None:
        """Executes a statement node (does not return a value)."""
        if isinstance(node, VarDeclNode):
            val = self.evaluate(node.value, env)
            val = self._validate_type(node.ty, val, node.value)
            env.define(node.name, val, node.ty)

        elif isinstance(node, AssignmentNode):
            line, col = self._get_coords(node.value)

            if not env.exists(node.name):
                raise RuntimeError_(f"Undefined variable '{node.name}'", line, col)

            val = self.evaluate(node.value, env)
            if env.type_of(node.name) is not None:
                val = self._validate_type(env.type_of(node.name), val, node.value)
            env.assign(node.name, val, line, col)

        elif isinstance(node, PrintNode):
            val = self.evaluate(node.expr, env)
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

        # Handle while loops, catching _Break and _Continue signals.
        elif isinstance(node, WhileNode):
            line, col = self._get_coords(node.cond)
            while True:
                cond_val = self.evaluate(node.cond, env)
                if not isinstance(cond_val, bool):
                    raise RuntimeError_("Condition in 'while' loop must be a boolean", line, col)
                if not cond_val:
                    break
                try:
                    self.execute(node.body, env.child())
                except _Break:
                    break
                except _Continue:
                    continue

        elif isinstance(node, ForNode):
            iterable = self.evaluate(node.iterable, env)
            if not isinstance(iterable, (list, str)):
                line, col = self._get_coords(node.iterable)
                raise RuntimeError_(f"'for' loop needs a range or string, got {type(iterable).__name__}", line, col)
            for item in iterable:
                loop_env = env.child()
                loop_env.define(node.var, item)
                try:
                    self.execute(node.body, loop_env)
                except _Break:
                    break
                except _Continue:
                    continue

        elif isinstance(node, FuncCallNode):
            self.evaluate(node, env)

        elif isinstance(node, FuncDefNode):
            env.define(node.name, (node, env))

        elif isinstance(node, ReturnNode):
            value = self.evaluate(node.expr, env) if node.expr is not None else None
            raise _Return(value)

        elif isinstance(node, BreakNode):
            raise _Break()
        elif isinstance(node, ContinueNode):
            raise _Continue()

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

        elif isinstance(node, FuncCallNode):
            target = env.lookup(node.name, node.line, node.column)
            args = [self.evaluate(a, env) for a in node.args]
            if callable(target):
                # builtin like range() / input()
                try:
                    return target(*args)
                except RuntimeError_ as e:
                    raise RuntimeError_(e.message, node.line, node.column)
                except (TypeError, ValueError):
                    raise RuntimeError_(f"Invalid arguments to '{node.name}'", node.line, node.column)
            if isinstance(target, tuple) and len(target) == 2:
                # user-defined: (FuncDefNode, defining_env)
                defn, closure = target
                return self._call(defn, closure, args, node)
            raise RuntimeError_(f"'{node.name}' is not callable", node.line, node.column)

        elif isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand, env)
            line, col = self._get_coords(node.operand)
            if node.op_type == TokenType.MINUS:
                if not isinstance(operand, (int, float)) or isinstance(operand, bool):
                    raise RuntimeError_("Unary '-' operator requires a numeric value", line, col)
                return -operand
            if node.op_type == TokenType.NOT_OP:
                if not isinstance(operand, bool):
                    raise RuntimeError_("Unary '!'/'not' operator requires a boolean value", line, col)
                return not operand

        elif isinstance(node, BinaryOpNode):
            left_val = self.evaluate(node.left, env)
            line, col = self._get_coords(node.right)

            # Logical Operator (short-circuit: the right side is only evaluated if needed)
            if node.op_type in (TokenType.AND_OP, TokenType.OR_OP):
                symbol = "&&" if node.op_type == TokenType.AND_OP else "||"
                if not isinstance(left_val, bool):
                    raise RuntimeError_(f"Operator '{symbol}' requires boolean operands", line, col)
                if left_val == (node.op_type == TokenType.OR_OP):
                    return left_val
                right_val = self.evaluate(node.right, env)
                if not isinstance(right_val, bool):
                    raise RuntimeError_(f"Operator '{symbol}' requires boolean operands", line, col)
                return right_val

            right_val = self.evaluate(node.right, env)

            # Equality Operators (bool is never equal to a number, although Python treats True as 1)
            if node.op_type in (TokenType.EQUALS, TokenType.NOT_EQUALS) and isinstance(left_val, bool) != isinstance(right_val, bool):
                raise RuntimeError_(f"Cannot compare {type(left_val).__name__} and {type(right_val).__name__}", line, col)
            if node.op_type == TokenType.EQUALS:     return left_val == right_val
            if node.op_type == TokenType.NOT_EQUALS: return left_val != right_val

            # Arithmetic And Comparison Runtime Type Protection
            if type(left_val) != type(right_val) and not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
                raise RuntimeError_(f"Invalid operation matching {type(left_val).__name__} and {type(right_val).__name__}", line, col)

            # Guard against using arithmetic operators with boolean values.
            if isinstance(left_val, bool) or isinstance(right_val, bool):
                raise RuntimeError_("Arithmetic operators cannot be used with boolean values", line, col)

            # Strings only support + (concatenation) and comparisons.
            if isinstance(left_val, str) and node.op_type in (TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.MODULO):
                raise RuntimeError_("Only '+' and comparisons can be used with strings", line, col)

            # Arithmetic
            if node.op_type == TokenType.PLUS:   return left_val + right_val
            if node.op_type == TokenType.MINUS:  return left_val - right_val
            if node.op_type == TokenType.STAR:   return left_val * right_val
            if node.op_type == TokenType.SLASH:
                if right_val == 0:
                    raise RuntimeError_("Division by zero", line, col)
                if isinstance(left_val, int) and isinstance(right_val, int):
                    return left_val // right_val      # floor division
                return left_val / right_val           # float division if either is float
            # Guard against modulo by zero, same style as division-by-zero above.
            if node.op_type == TokenType.MODULO:
                if right_val == 0:
                    raise RuntimeError_("Modulo by zero", line, col)
                return left_val % right_val

            # Comparisons
            if node.op_type == TokenType.LESS:          return left_val < right_val
            if node.op_type == TokenType.GREATER:       return left_val > right_val
            if node.op_type == TokenType.LESS_EQUAL:    return left_val <= right_val
            if node.op_type == TokenType.GREATER_EQUAL: return left_val >= right_val

        raise RuntimeError_("Unknown expression node mapping")

    # Helper to call a user-defined function
    def _call(self, defn: FuncDefNode, closure: Environment, args: List[Any], call_node: FuncCallNode) -> Any:
        if len(args) != len(defn.params):
            raise RuntimeError_(f"Function '{defn.name}' expects {len(defn.params)} arg(s), got {len(args)}", call_node.line, call_node.column)

        call_env = closure.child()
        for (pname, ptype), arg in zip(defn.params, args):
            arg = self._validate_type(ptype, arg, call_node)
            call_env.define(pname, arg, ptype)

        try:
            for stmt in defn.body.stmts:
                self.execute(stmt, call_env)
        except _Return as r:
            if defn.return_type is not None:
                return self._validate_type(defn.return_type, r.value, call_node)
            return r.value
        # break/continue must not escape a function into the caller's loop.
        except (_Break, _Continue):
            raise RuntimeError_(f"'break'/'continue' outside of loop in function '{defn.name}'", call_node.line, call_node.column)

        if defn.return_type is not None:
            raise RuntimeError_(f"Function '{defn.name}' expected a return value", call_node.line, call_node.column)
        return None

    # Helper Utilities
    def _get_coords(self, node: ASTNode) -> tuple[Union[int, None], Union[int, None]]:
        """Safely extract coordinate metrics down the left branch of an expression."""
        if hasattr(node, 'line') and node.line is not None:
            return node.line, node.column
        if hasattr(node, 'left'):
            return self._get_coords(node.left)
        # Walk into unary operands to extract coordinates from the operand.
        if hasattr(node, 'operand'):
            return self._get_coords(node.operand)
        return None, None

    def _validate_type(self, expected_type: str, value: Any, value_node: ASTNode) -> Any:
        """Type verification to satisfy the explicit assignment declarations."""
        line, col = self._get_coords(value_node)
        mapping = {"int": int, "float": float, "bool": bool, "string": str}

        if expected_type in mapping:
            # Reject boolean values where other types are expected.
            if isinstance(value, bool) and expected_type != "bool":
                raise RuntimeError_(f"Type mismatch: Expected '{expected_type}', got value of type 'bool'", line, col)
            if not isinstance(value, mapping[expected_type]):
                # Allow promotion of ints to float implicitly if acceptable
                if expected_type == "float" and isinstance(value, int):
                    return float(value)
                raise RuntimeError_(f"Type mismatch: Expected '{expected_type}', got value of type '{type(value).__name__}'", line, col)
        return value
