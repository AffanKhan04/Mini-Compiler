# NumCalc Mini Language Compiler

A complete compiler implementation for **NumCalc**, a domain-specific mini language designed for numerical computations and pattern generation. This project demonstrates all six major phases of compiler construction.

## 🎯 Project Overview

NumCalc is a statically-typed mini language that supports:
- Variables (int, float, bool, string)
- Functions with parameters and return values
- Control structures (if-else, while loops, for loops)
- Arithmetic, relational, and logical operations
- Recursion
- Pattern generation and mathematical computations

## 📋 Language Features

### Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `bool` - Boolean values (true/false)
- `string` - String literals

### Operators
- **Arithmetic:** `+`, `-`, `*`, `/`, `%`, `**` (power)
- **Relational:** `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Logical:** `and`, `or`, `not`
- **Assignment:** `=`

### Control Structures
- `if-else` statements
- `while` loops
- `for` loops
- `function` definitions

### Built-in Functions
- `print()` - Output to console

## 🏗️ Compiler Architecture

The compiler implements all six phases of compilation:

### Phase 1: Lexical Analysis (lexer.py)
- Tokenizes source code into meaningful symbols
- Recognizes keywords, identifiers, literals, operators, and delimiters
- Handles comments (single-line // and multi-line /* */)
- Line and column tracking for error reporting

### Phase 2: Syntax Analysis (parser.py)
- Recursive descent parser
- Builds Abstract Syntax Tree (AST) from tokens
- Validates program structure against BNF grammar
- Detects syntax errors with precise location

### Phase 3: Semantic Analysis (semantic_analyzer.py)
- Type checking and type inference
- Symbol table management (variables and functions)
- Scope management (block-level scoping)
- Detects semantic errors:
  - Type mismatches
  - Undeclared variables
  - Duplicate declarations
  - Invalid operations

### Phase 4: Intermediate Code Generation (ir_generator.py)
- Generates three-address code (TAC)
- Converts AST to linear instruction sequence
- Instruction format: `result = operand1 operator operand2`
- Supports labels, jumps, and function calls

### Phase 5: Optimization (optimizer.py)
- **Constant folding:** Evaluates constant expressions at compile time
- **Copy propagation:** Eliminates unnecessary variable copies
- **Dead code elimination:** Removes unused variable assignments

### Phase 6: Code Generation/Execution (interpreter.py)
- Interprets optimized intermediate code
- Virtual machine execution model
- Runtime environment with call stack
- Executes programs and displays output

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Installation
```bash
# Clone or download the project
cd Compiler-Construction-Project

# No installation needed - pure Python implementation
```

## 📖 Usage

### Compile and Run a Program
```bash
python compiler.py examples/fibonacci.nc
```

### Verbose Mode (Show All Phases)
```bash
python compiler.py examples/fibonacci.nc -v
```

This displays:
- Phase 1: Token list
- Phase 2: Parse tree structure
- Phase 3: Symbol table
- Phase 4: Three-address code
- Phase 5: Optimized code
- Phase 6: Program output

### Disable Optimizations
```bash
python compiler.py examples/fibonacci.nc --no-opt
```

### Interactive Mode (REPL)
```bash
python compiler.py -i
```

### Help
```bash
python compiler.py --help
```

## 📝 Example Programs

See the `examples/` directory for sample programs:

1. **fibonacci.nc** - Fibonacci sequence generator
2. **factorial.nc** - Factorial calculator
3. **prime_numbers.nc** - Prime number finder
4. **patterns.nc** - Number pattern generator
5. **math_operations.nc** - Arithmetic operations demo
6. **power_root.nc** - Power and square root functions
7. **sum_average.nc** - Sum calculations
8. **gcd_lcm.nc** - GCD and LCM calculator

## 💡 Sample Code

```numcalc
// Calculate factorial recursively
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int x = 5;
int result = factorial(x);
print("Factorial of", x, "is", result);
```

## 🔍 Language Specification

Detailed language specification is available in `LANGUAGE_SPEC.md`, including:
- Complete BNF grammar
- Lexical rules
- Semantic rules
- Type system
- Example programs with expected output

## 📂 Project Structure

```
Compiler-Construction-Project/
├── compiler.py              # Main compiler driver
├── lexer.py                 # Phase 1: Lexical analyzer
├── parser.py                # Phase 2: Syntax analyzer
├── semantic_analyzer.py     # Phase 3: Semantic analyzer
├── ir_generator.py          # Phase 4: IR generator
├── optimizer.py             # Phase 5: Optimizer
├── interpreter.py           # Phase 6: Interpreter
├── LANGUAGE_SPEC.md         # Complete language specification
├── README.md                # This file
└── examples/                # Example programs
    ├── fibonacci.nc
    ├── factorial.nc
    ├── prime_numbers.nc
    ├── patterns.nc
    ├── math_operations.nc
    ├── power_root.nc
    ├── sum_average.nc
    ├── gcd_lcm.nc
    └── README.md
```

## 🧪 Testing

Each module includes a test function. Run individual phases:

```bash
# Test lexer
python lexer.py

# Test parser
python parser.py

# Test semantic analyzer
python semantic_analyzer.py

# Test IR generator
python ir_generator.py

# Test optimizer
python optimizer.py

# Test interpreter
python interpreter.py
```

## 🎓 Educational Value

This compiler demonstrates:
- **Lexical Analysis:** DFA-based tokenization
- **Parsing:** Recursive descent with operator precedence
- **Semantic Analysis:** Symbol tables, type systems, scope management
- **IR Generation:** Three-address code representation
- **Optimization:** Classic compiler optimizations
- **Code Generation:** Virtual machine interpretation

## ⚠️ Known Limitations

- No array or struct types
- Limited string operations
- No file I/O
- Integer division only (no mixed int/float division)
- Basic optimization (no advanced techniques like loop optimization)
- No garbage collection (not needed for current scope)

## 🔮 Future Enhancements

- Add array and struct types
- Implement more optimizations (loop unrolling, strength reduction)
- Add native code generation (x86/ARM assembly)
- Implement debugger support
- Add more built-in functions
- Support for imports/modules

## 👥 Project Information

**Course:** Compiler Construction  
**Project:** Mini Language Compiler  
**Language:** NumCalc (Domain-specific language for numerical computations)  

## 📄 License

This project is created for educational purposes as part of a Compiler Construction course.

## 🤝 Contributing

This is an academic project. Suggestions and improvements are welcome!

## 📞 Contact

For questions about the implementation or language features, please refer to the language specification document.

---

**Note:** This compiler is designed for educational purposes to demonstrate compiler construction concepts. It is not intended for production use.
