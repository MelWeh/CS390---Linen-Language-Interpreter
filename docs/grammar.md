# Linen — Formal Grammar (BNF/EBNF)

This document defines the formal grammar for the **Linen** programming
language. It is the reference for the lexer and parser implementations.

---

## Notation

| Symbol      | Meaning                                    |
|-------------|--------------------------------------------|
| `::=`       | "is defined as"                            |
| `{ X }`     | zero or more repetitions of `X`            |
| `[ X ]`     | optional `X`                               |
| `"x"`       | the literal terminal token `x`             |
| `\|`        | alternation ("or")                         |
| `..`        | shorthand for "all characters in between"  |

**Example of `..` shorthand**

Instead of writing every letter:

```
letter ::= "a" | "b" | "c" | ... | "z" | "A" | "B" | ... | "Z" ;
```

we use the compact form:

```
letter ::= "a" | ... | "z" | "A" | ... | "Z" ;
```

This means: a letter can be any lowercase English alphabet character
`a` through `z`, **or** any uppercase English alphabet character `A`
through `Z`.

---

## 1. Lexical Rules

```ebnf
letter         ::= "a" | ... | "z" | "A" | ... | "Z" ;
digit          ::= "0" | ... | "9" ;
number         ::= digit { digit } [ "." digit { digit } ] ;
identifier     ::= ( letter | "_" ) { letter | digit | "_" } ;
string_literal ::= '"' { any_char_except_quote } '"' ;
boolean        ::= "true" | "false" ;
```

---

## 2. Terminals (Keywords, Operators, Delimiters)

### Keywords

```
and   or    not   true  false
let   print if    else  while  for  in  func  return  break  continue
is
```

### Type keywords

```
int   float   bool   string
```

### Operators

```
+   -   *   /   %   =   ==   !=   <   >   <=   >=   &&   ||   !   ->
```

### Delimiters

```
(   )   {   }   [   ]   ,   ;   :
```

---

## 3. Grammar

```ebnf
program        ::= statement_list ;

statement_list ::= { statement } ;

statement      ::= var_decl
                 | assignment
                 | print_stmt
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | func_def
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 ;

var_decl       ::= "let" identifier ":" type "=" expression ";" ;
assignment     ::= identifier "=" expression ";" ;
print_stmt     ::= "print" "(" expression ")" ";" ;
if_stmt        ::= "if" "(" expression ")" block [ "else" block ] ;
while_stmt     ::= "while" "(" expression ")" block ;
for_stmt       ::= "for" identifier "in" expression block ;
func_def       ::= "func" identifier "(" param_list ")" [ "->" type ] block ;
param_list     ::= [ param { "," param } ] ;
param          ::= identifier ":" type ;
return_stmt    ::= "return" expression ";" ;
break_stmt     ::= "break" ";" ;
continue_stmt  ::= "continue" ";" ;
block          ::= "{" statement_list "}" ;

expression     ::= logic_or ;

logic_or       ::= logic_and { ( "||" | "or" ) logic_and } ;
logic_and      ::= equality  { ( "&&" | "and" ) equality } ;
equality       ::= relational { ( "==" | "!=" ) relational } ;
relational     ::= additive  { ( "<" | ">" | "<=" | ">=" ) additive } ;
additive       ::= term      { ( "+" | "-" ) term } ;
term           ::= factor    { ( "*" | "/" | "%" ) factor } ;
factor         ::= number
                 | boolean
                 | string_literal
                 | identifier
                 | func_call
                 | "(" expression ")"
                 ;

func_call      ::= identifier "(" [ expression { "," expression } ] ")" ;

type           ::= "int" | "float" | "bool" | "string" ;
```

---

## 4. Notes

- Every statement is terminated by `;`, except compound statements
  (`if`, `while`, `for`, `func`) which end with a `}` block.
- The `is` keyword is reserved for future type-check expressions
  (e.g., `x is int`). A production will be added when the feature lands.
- `and`, `or`, `not` are keyword aliases for `&&`, `||`, `!` and may appear
  anywhere the symbolic form is allowed.
- `range` is **not** a keyword — it is treated as a normal identifier and
  resolves at runtime.
