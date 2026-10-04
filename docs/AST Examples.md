# AST Examples

## Example 1 — Arithmetic Precedence

**Source (`testfile1.ln`):**
```
let x: int = 2 + 3 * 4;
```

**AST (`testfile1.out`):**
```
ProgramNode([VarDeclNode(x, int, BinaryOpNode(NumberNode(2), TokenType.PLUS, BinaryOpNode(NumberNode(3), TokenType.STAR, NumberNode(4))))])
```

**AST Expanded Tree:**
```
ProgramNode
  VarDeclNode(x, int)
    BinaryOpNode(PLUS)
      NumberNode(2)
      BinaryOpNode(STAR)
        NumberNode(3)
        NumberNode(4)
```

**Interpretation:** The `*` node is nested under the right side of the `+` node,
confirming that multiplication binds tighter than addition.

---

## Example 2 — Multiple Statements

**Source (`testfile2.ln`):**
```
let x: int = 10;
x = x + 5;
print(x);
```

**AST (`testfile2.out`):**
```
ProgramNode([VarDeclNode(x, int, NumberNode(10)), AssignmentNode(x, BinaryOpNode(VariableNode(x), TokenType.PLUS, NumberNode(5))), PrintNode(VariableNode(x))])
```

**AST Expanded Tree:**
```
ProgramNode
  VarDeclNode(x, int)
    NumberNode(10)
  AssignmentNode(x)
    BinaryOpNode(PLUS)
      VariableNode(x)
      NumberNode(5)
  PrintNode
    VariableNode(x)
```

**Interpretation:** Each top-level statement becomes a child of `ProgramNode`, in the order it appears in the source — a declaration, then an assignment that reuses the variable, then a print.

---

## Example 3 — If/Else Statements

**Source (`testfile3.ln`):**
```
let x: int = 5;
if (x > 3) {
    print(x);
} else {
    print(0);
}
```

**AST (`testfile3.out`):**
```
ProgramNode([VarDeclNode(x, int, NumberNode(5)), IfNode(BinaryOpNode(VariableNode(x), TokenType.GREATER, NumberNode(3)), BlockNode([PrintNode(VariableNode(x))]), BlockNode([PrintNode(NumberNode(0))]))])
```

**AST Expanded Tree:**
```
ProgramNode
  VarDeclNode(x, int)
    NumberNode(5)
  IfNode
    condition:
      BinaryOpNode(GREATER)
        VariableNode(x)
        NumberNode(3)
    then:
      BlockNode
        PrintNode
          VariableNode(x)
    else:
      BlockNode
        PrintNode
          NumberNode(0)
```

**Interpretation:** `IfNode` holds three children — the condition `(x > 3)`, the `then` block, and the `else` block — each represented as its own subtree.

---

## Example 4 — While Loop

**Source (`testfile4.ln`):**
```
let i: int = 0;
while (i < 3) {
    print(i);
    i = i + 1;
}
```

**AST (`testfile4.out`):**
```
ProgramNode([VarDeclNode(i, int, NumberNode(0)), WhileNode(BinaryOpNode(VariableNode(i), TokenType.LESS, NumberNode(3)), BlockNode([PrintNode(VariableNode(i)), AssignmentNode(i, BinaryOpNode(VariableNode(i), TokenType.PLUS, NumberNode(1)))]))])
```


**AST Expanded Tree:**
```
ProgramNode
  VarDeclNode(i, int)
    NumberNode(0)
  WhileNode
    condition:
      BinaryOpNode(LESS)
        VariableNode(i)
        NumberNode(3)
    body:
      BlockNode
        PrintNode
          VariableNode(i)
        AssignmentNode(i)
          BinaryOpNode(PLUS)
            VariableNode(i)
            NumberNode(1)
```


**Interpretation:** `WhileNode` holds the loop condition (`i < 3`) and a `BlockNode`
containing the two loop-body statements — a `print` and an increment assignment.

---

## Example 5 — Unary Operators

**Source (`testfile5.ln`):**
```
let x: int = -5;
print(not x);
```

**AST (`testfile5.out`):**
```
ProgramNode([VarDeclNode(x, int, UnaryOpNode(TokenType.MINUS, NumberNode(5))), PrintNode(UnaryOpNode(TokenType.NOT_OP, VariableNode(x)))])
```

**AST Expanded Tree:**
```
ProgramNode
  VarDeclNode(x, int)
    UnaryOpNode(MINUS)
      NumberNode(5)
  PrintNode
    UnaryOpNode(NOT_OP)
      VariableNode(x)
```

**Interpretation:** Both `-5` and `not x` are represented by `UnaryOpNode`, with the operand stored as a child node — a `NumberNode` for the literal and a `VariableNode` for the identifier.