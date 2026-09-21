# Linen — Token Definitions

The Linen lexer recognizes the following tokens. Each token carries a `type`
(from the `TokenType` enum), a `value` (the raw source text), a `line`, and a
`column`. Some tokens also carry a `literal` (the parsed Python value).

## 1. Keywords

These are reserved words. The lexer maps them to their own token type rather
than to `IDENTIFIER`.

| Keyword    | Token Type    |
|------------|---------------|
| `let`      | `LET`         |
| `print`    | `PRINT`       |
| `if`       | `IF`          |
| `else`     | `ELSE`        |
| `while`    | `WHILE`       |
| `for`      | `FOR`         |
| `in`       | `IN`          |
| `is`       | `IS`          |
| `func`     | `FUNC`        |
| `return`   | `RETURN`      |
| `break`    | `BREAK`       |
| `continue` | `CONTINUE`    |
| `true`     | `TRUE`        |
| `false`    | `FALSE`       |
| `and`      | `AND`         |
| `or`       | `OR`          |
| `not`      | `NOT`         |

## 2. Type Keywords

| Keyword  | Token Type     |
|----------|----------------|
| `int`    | `TYPE_INT`     |
| `float`  | `TYPE_FLOAT`   |
| `bool`   | `TYPE_BOOL`    |
| `string` | `TYPE_STRING`  |

## 3. Literals

| Token Type      | Matches                                                    | `literal` field  |
|-----------------|------------------------------------------------------------|------------------|
| `NUMBER`        | Integer (`10`) or decimal (`3.14`) numeric literal         | `int` or `float` |
| `STRING`        | Text enclosed in double quotes, e.g. `"Hello"`             | the string value |
| `IDENTIFIER`    | A name starting with a letter or `_`, followed by letters, digits, or `_` | — |

**Note:** integers and floats both emit `NUMBER`. The parsed value is stored in
`token.literal` so downstream stages can distinguish `int` from `float`.

## 4. Operators

| Lexeme | Token Type       |
|--------|------------------|
| `+`    | `PLUS`           |
| `-`    | `MINUS`          |
| `*`    | `STAR`           |
| `/`    | `SLASH`          |
| `%`    | `MODULO`         |
| `=`    | `ASSIGN`         |
| `==`   | `EQUALS`         |
| `!=`   | `NOT_EQUALS`     |
| `<`    | `LESS`           |
| `>`    | `GREATER`        |
| `<=`   | `LESS_EQUAL`     |
| `>=`   | `GREATER_EQUAL`  |
| `&&`   | `AND_OP`         |
| `\|\|` | `OR_OP`          |
| `!`    | `NOT_OP`         |
| `->`   | `ARROW`          |

## 5. Delimiters

| Lexeme | Token Type   |
|--------|--------------|
| `(`    | `LPAREN`     |
| `)`    | `RPAREN`     |
| `{`    | `LBRACE`     |
| `}`    | `RBRACE`     |
| `[`    | `LBRACKET`   |
| `]`    | `RBRACKET`   |
| `,`    | `COMMA`      |
| `;`    | `SEMICOLON`  |
| `:`    | `COLON`      |

## 6. Special

| Token Type | Meaning                                          |
|------------|--------------------------------------------------|
| `EOF`      | End of input. Always the final token emitted.   |

## 7. Reserved Keywords Cannot Be Identifiers

Any string in the keyword lists above is always lexed as its keyword token —
never as an `IDENTIFIER`. For example, `let` will never produce an
`IDENTIFIER` token, even if the programmer wants to use it as a variable name.