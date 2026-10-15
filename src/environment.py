"""
Environment / Symbol Table for the Linen interpreter.
"""

from typing import Any, Dict, Optional


class RuntimeError_(Exception):
    """Raised when the interpreter hits an error at runtime."""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        self.message = message
        self.line = line
        self.column = column
        if line is not None and column is not None:
            super().__init__(f"[Runtime Error] line {line}, col {column}: {message}")
        else:
            super().__init__(f"[Runtime Error] {message}")


class Environment:
    """
    A single lexical scope.  `parent` chains to the enclosing scope.
    """

    def __init__(self, parent: "Environment" = None):
        self.parent: Optional[Environment] = parent
        self.values: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Scope management
    # ------------------------------------------------------------------
    def child(self) -> "Environment":
        """Return a new inner scope whose parent is this one."""
        return Environment(parent=self)

    # ------------------------------------------------------------------
    # Variable operations
    # ------------------------------------------------------------------
    def define(self, name: str, value: Any) -> None:
        """Introduce a new variable into the current scope."""
        self.values[name] = value

    def assign(self, name: str, value: Any, line: int = None, column: int = None) -> None:
        """Update an existing variable, searching outward through the chain."""
        env = self
        while env is not None:
            if name in env.values:
                env.values[name] = value
                return
            env = env.parent
        raise RuntimeError_(f"Undefined variable '{name}'", line, column)

    def lookup(self, name: str, line: int = None, column: int = None) -> Any:
        """Retrieve a variable's value, searching outward through the chain."""
        env = self
        while env is not None:
            if name in env.values:
                return env.values[name]
            env = env.parent
        raise RuntimeError_(f"Undefined variable '{name}'", line, column)

    def exists(self, name: str) -> bool:
        env = self
        while env is not None:
            if name in env.values:
                return True
            env = env.parent
        return False

    def __repr__(self) -> str:
        chain = []
        env = self
        while env is not None:
            chain.append(dict(env.values))
            env = env.parent
        return f"Environment({chain})"
