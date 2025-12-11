# Mini Compiler Language Specification

## 1. Overview
Mini Compiler is a domain-specific mini language designed for numerical computations, pattern generation, and mathematical operations. It supports variables, functions, loops, conditionals, and common mathematical operations.

## 2. Lexical Rules

### 2.1 Keywords
```
int, float, bool, string
if, else, while, for, return
print, input
true, false
function
```

### 2.2 Operators
```
Arithmetic: +, -, *, /, %, **
Relational: ==, !=, <, >, <=, >=
Logical: and, or, not
Assignment: =
```

### 2.3 Delimiters
```
( ) { } [ ] ; , :
```

### 2.4 Identifiers
- Start with a letter or underscore
- Followed by letters, digits, or underscores
- Pattern: [a-zA-Z_][a-zA-Z0-9_]*

### 2.5 Literals
- **Integer**: [0-9]+
- **Float**: [0-9]+\.[0-9]+
- **String**: ".*"
- **Boolean**: true, false

### 2.6 Comments
```
// Single line comment
/* Multi-line comment */
```

## 3. Syntax (BNF Grammar)

```bnf
<program> ::= <statement_list>

<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <declaration>
              | <assignment>
              | <if_statement>
              | <while_statement>
              | <for_statement>
              | <function_def>
              | <return_statement>
              | <print_statement>
              | <expression_statement>

<declaration> ::= <type> <identifier> ";" 
                | <type> <identifier> "=" <expression> ";"

<type> ::= "int" | "float" | "bool" | "string"

<assignment> ::= <identifier> "=" <expression> ";"

<if_statement> ::= "if" "(" <expression> ")" <block>
                 | "if" "(" <expression> ")" <block> "else" <block>

<while_statement> ::= "while" "(" <expression> ")" <block>

<for_statement> ::= "for" "(" <assignment> <expression> ";" <assignment> ")" <block>

<function_def> ::= "function" <type> <identifier> "(" <param_list> ")" <block>

<param_list> ::= <type> <identifier> | <type> <identifier> "," <param_list> | ε

<return_statement> ::= "return" <expression> ";"

<print_statement> ::= "print" "(" <expression_list> ")" ";"

<expression_statement> ::= <expression> ";"

<block> ::= "{" <statement_list> "}" | "{" "}"

<expression> ::= <logical_or>

<logical_or> ::= <logical_and> | <logical_or> "or" <logical_and>

<logical_and> ::= <equality> | <logical_and> "and" <equality>

<equality> ::= <relational> | <equality> ("==" | "!=") <relational>

<relational> ::= <additive> | <relational> ("<" | ">" | "<=" | ">=") <additive>

<additive> ::= <multiplicative> | <additive> ("+" | "-") <multiplicative>

<multiplicative> ::= <power> | <multiplicative> ("*" | "/" | "%") <power>

<power> ::= <unary> | <power> "**" <unary>

<unary> ::= <primary> | "not" <unary> | "-" <unary>

<primary> ::= <identifier>
            | <literal>
            | "(" <expression> ")"
            | <function_call>

<function_call> ::= <identifier> "(" <expression_list> ")"

<expression_list> ::= <expression> | <expression> "," <expression_list> | ε

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]*

<literal> ::= <integer> | <float> | <string> | <boolean>
```

## 4. Semantic Rules

### 4.1 Type System
- Static typing with type inference in declarations with initialization
- Supported types: int, float, bool, string
- Type coercion: int → float (automatic), others require explicit conversion

### 4.2 Type Checking Rules
1. Arithmetic operations (+, -, *, /, %, **) require numeric types (int, float)
2. Relational operations (<, >, <=, >=) require numeric types, return bool
3. Equality operations (==, !=) work on any type, return bool
4. Logical operations (and, or, not) require bool type
5. Assignment requires matching types or valid coercion
6. Function return type must match declared return type

### 4.3 Scope Rules
- Block-level scoping
- Variables must be declared before use
- Functions must be declared before calls
- No shadowing of variables in nested scopes

### 4.4 Symbol Table
- Track variables: name, type, scope level
- Track functions: name, return type, parameters
- Check for duplicate declarations in same scope

## 5. Example Programs

### Example 1: Fibonacci Sequence Generator
```numcalc
// Generate Fibonacci sequence
function int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int i = 0;
while (i < 10) {
    print("Fibonacci(", i, ") = ", fibonacci(i));
    i = i + 1;
}
```

### Example 2: Factorial Calculator
```numcalc
// Calculate factorial
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int num = 5;
int result = factorial(num);
print("Factorial of ", num, " is ", result);
```

### Example 3: Prime Number Checker
```numcalc
// Check if number is prime
function bool isPrime(int n) {
    if (n <= 1) {
        return false;
    }
    int i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

int count = 0;
int num = 2;
while (count < 10) {
    if (isPrime(num)) {
        print(num);
        count = count + 1;
    }
    num = num + 1;
}
```

### Example 4: Pattern Generation
```numcalc
// Generate number patterns
int rows = 5;
int i = 1;
while (i <= rows) {
    int j = 1;
    while (j <= i) {
        print(j);
        j = j + 1;
    }
    print("\n");
    i = i + 1;
}
```

### Example 5: Mathematical Operations
```numcalc
// Basic math operations
int a = 10;
int b = 3;
float c = 2.5;

print("Sum: ", a + b);
print("Difference: ", a - b);
print("Product: ", a * b);
print("Division: ", a / b);
print("Modulo: ", a % b);
print("Power: ", a ** 2);
print("Float arithmetic: ", c * 2.0);
```

## 6. Expected Output Format

Programs output results through `print` statements. Numbers, strings, and boolean values are printed sequentially. Each print statement outputs on a new line unless explicitly concatenated.

## 7. Error Handling

The compiler should detect and report:
- Lexical errors (invalid tokens)
- Syntax errors (grammar violations)
- Semantic errors (type mismatches, undeclared variables)
- Runtime errors (division by zero, stack overflow)
