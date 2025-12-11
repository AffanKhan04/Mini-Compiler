# NumCalc Compiler - Example Programs

This directory contains example programs demonstrating various features of the NumCalc language.

## Running Examples

To run an example:
```bash
python compiler.py examples/fibonacci.nc
```

To see all compilation phases:
```bash
python compiler.py examples/fibonacci.nc -v
```

## Available Examples

### 1. fibonacci.nc
Generates the first 10 Fibonacci numbers using recursion.
**Demonstrates:** Recursion, conditionals, while loops

### 2. factorial.nc
Calculates factorials from 1 to 7.
**Demonstrates:** Recursion, mathematical operations

### 3. prime_numbers.nc
Finds and displays the first 15 prime numbers.
**Demonstrates:** Nested loops, boolean logic, modulo operation

### 4. patterns.nc
Generates triangle and square number patterns.
**Demonstrates:** Nested loops, pattern generation

### 5. math_operations.nc
Showcases all arithmetic and comparison operations.
**Demonstrates:** All operators, type mixing (int/float)

### 6. power_root.nc
Implements power function and square root approximation.
**Demonstrates:** Iterative algorithms, mathematical approximations

### 7. sum_average.nc
Calculates sum and sum of squares.
**Demonstrates:** Multiple functions, loops

### 8. gcd_lcm.nc
Computes GCD and LCM using Euclidean algorithm.
**Demonstrates:** Advanced algorithms, mathematical computations

## Language Features Demonstrated

- **Functions:** User-defined functions with parameters and return values
- **Recursion:** Factorial, Fibonacci, etc.
- **Loops:** While loops for iteration
- **Conditionals:** If-else statements
- **Operators:** Arithmetic (+, -, *, /, %, **), Relational (<, >, <=, >=, ==, !=), Logical (and, or, not)
- **Types:** int, float, bool
- **Print:** Output to console
