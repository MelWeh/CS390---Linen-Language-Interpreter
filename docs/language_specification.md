## 1.	Language name & description.
Linen is a statically typed, imperative programming language with a clean, readable syntax inspired by Python and C-style control flow. It supports variables, arithmetic, boolean logic, conditionals, loops, and functions with parameters and return values. Linen emphasizes clarity through explicit types and block-based structure using braces.

---

## 2.	Keywords
    ```
    and     or      not     is          if      else
    true    false   break   continue    func    return
    print   let     while   for         in     
    ```

---

## 3.	Operators and delimiters.
Operators:
•	+		Addition
•	-		Subtraction
•	/		Division
•	*		Multiplication
•	==		Equals to
•	<		Less than
•	>		Greater than
•	<= 	    Less than or equal
•	>=		Greater than or equal
•	&&	    AND (Logic)
•	||		OR
•	!		NO 
 
Delimiters:
•	( )
•	{ }
•	[ ]
•	;
•	:
•	,
•	=
•	=>

---

## 4. Variable declaration/assignment syntax.
Linen uses let with explicit types for declarations.

### Declaration

```linen
let x: int = 10;
let y: float = 3.14;
let flag: bool = true;
```

### Assignment (after declaration)

```linen
x = x + 5;
flag = false;
```
### Type examples

- `int` — integer numbers
- `float` — decimal numbers
- `bool` — `true` or `false`
- `string` — text in double quotes (extension feature)

> Variables must be declared with `let` before use.

---

## 5. Control-Structure Syntax

### if / else

```linen
if (x < y) {
    print(x);
} else {
    print(y);
}
```

### while

```linen
while (count < 10) {
    print(count);
    count = count + 1;
}
```

### for-in (extension-style loop)

```linen
for i in range(0, 5) {
    print(i);
}
```

### break / continue

```linen
while (true) {
    if (x > 100) {
        break;
    }
    if (x % 2 == 0) {
        x = x + 1;
        continue;
    }
    x = x + 2;
}
```

---

## 6. Function Syntax

Linen uses `func` with typed parameters and a return type using `->`.

### Function definition

```linen
func add(a: int, b: int) -> int {
    let result: int = a + b;
    return result;
}
```

### Void-like function (no return value)

```linen
func greet(name: string) {
    print("Hello, " + name);
}
```

### Function call

```linen
let x: int = add(3, 4);
print(x);
```

---

## 7. Sample Programs

### Sample Program 1 — Variables, arithmetic, print

```linen
let x: int = 10;
let y: int = 20;
let z: int = x + y * 2;

print(x);
print(y);
print(z);
```

### Sample Program 2 — if/else and while

```linen
let count: int = 0;
let limit: int = 5;

while (count < limit) {
    if (count % 2 == 0) {
        print(count);
    } else {
        print(count + 100);
    }
    count = count + 1;
}
```

### Sample Program 3 — Functions and boolean logic

```linen
func max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

let x: int = 3;
let y: int = 7;
let m: int = max(x, y);
let isLarge: bool = (m > 5);

if (isLarge == true) {
    print(m);
} else {
    print(0);
}
```

---

## 8. Extension Features

- Input recognition
- Print
- Transforming data types from one form to another
- Statically typed functions with explicit return types and typed parameters
- `for-in` loops over ranges
- `string` type and string literals

---

## 9. Grammar Reference

The formal BNF/EBNF grammar for Linen is maintained in
[`GRAMMAR.md`](./GRAMMAR.md).

---