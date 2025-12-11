"""
Semantic Analyzer for Mini Compiler Language
Phase 3: Performs semantic analysis including:
- Symbol table construction
- Type checking
- Scope management
- Semantic error detection
"""

from parser import *
from typing import Dict, List, Optional, Any


class SymbolTable:
    """Symbol table for managing variable and function declarations"""
    
    def __init__(self, parent=None):
        self.symbols: Dict[str, Dict] = {}
        self.parent = parent
        self.scope_level = 0 if parent is None else parent.scope_level + 1
    
    def define(self, name: str, symbol_type: str, data_type: str, **kwargs):
        """Define a new symbol in current scope"""
        if name in self.symbols:
            raise SemanticError(f"Redeclaration of '{name}' in the same scope")
        
        self.symbols[name] = {
            'type': symbol_type,  # 'variable' or 'function'
            'data_type': data_type,
            **kwargs
        }
    
    def lookup(self, name: str) -> Optional[Dict]:
        """Look up a symbol in current scope or parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        return None
    
    def exists(self, name: str) -> bool:
        """Check if symbol exists in any accessible scope"""
        return self.lookup(name) is not None
    
    def __repr__(self):
        return f"SymbolTable(level={self.scope_level}, symbols={self.symbols})"


class SemanticError(Exception):
    """Semantic analysis error"""
    pass


class SemanticAnalyzer:
    """Performs semantic analysis on the AST"""
    
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.current_function = None
        self.errors: List[str] = []
    
    def error(self, message: str, node: ASTNode):
        """Record a semantic error"""
        error_msg = f"Semantic error at line {node.line}, column {node.column}: {message}"
        self.errors.append(error_msg)
        raise SemanticError(error_msg)
    
    def enter_scope(self):
        """Enter a new scope"""
        self.current_scope = SymbolTable(parent=self.current_scope)
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def analyze(self, node: ASTNode) -> str:
        """
        Analyze a node and return its type
        Dispatches to specific analysis methods based on node type
        """
        method_name = f'analyze_{node.__class__.__name__}'
        method = getattr(self, method_name, None)
        
        if method:
            return method(node)
        else:
            raise SemanticError(f"No analysis method for {node.__class__.__name__}")
    
    # ============= Analysis Methods =============
    
    def analyze_Program(self, node: Program) -> str:
        """Analyze the entire program"""
        for statement in node.statements:
            self.analyze(statement)
        return 'void'
    
    def analyze_VarDeclaration(self, node: VarDeclaration) -> str:
        """Analyze variable declaration"""
        # Check if variable already exists in current scope
        if node.name in self.current_scope.symbols:
            self.error(f"Variable '{node.name}' already declared in this scope", node)
        
        # Type check initializer if present
        if node.initializer:
            init_type = self.analyze(node.initializer)
            if not self.is_compatible_type(node.var_type, init_type):
                self.error(
                    f"Type mismatch: cannot assign {init_type} to {node.var_type} "
                    f"in declaration of '{node.name}'",
                    node
                )
        
        # Add to symbol table
        self.current_scope.define(
            node.name,
            symbol_type='variable',
            data_type=node.var_type,
            initialized=node.initializer is not None
        )
        
        return 'void'
    
    def analyze_Assignment(self, node: Assignment) -> str:
        """Analyze assignment statement"""
        # Check if variable exists
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.error(f"Undefined variable '{node.name}'", node)
        
        if symbol['type'] != 'variable':
            self.error(f"'{node.name}' is not a variable", node)
        
        # Type check value
        value_type = self.analyze(node.value)
        var_type = symbol['data_type']
        
        if not self.is_compatible_type(var_type, value_type):
            self.error(
                f"Type mismatch: cannot assign {value_type} to {var_type} "
                f"variable '{node.name}'",
                node
            )
        
        return 'void'
    
    def analyze_BinaryOp(self, node: BinaryOp) -> str:
        """Analyze binary operation"""
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        # Arithmetic operators
        if node.operator in ['+', '-', '*', '/', '%', '**']:
            if not self.is_numeric(left_type) or not self.is_numeric(right_type):
                self.error(
                    f"Operator '{node.operator}' requires numeric operands, "
                    f"got {left_type} and {right_type}",
                    node
                )
            # Result type promotion
            if left_type == 'float' or right_type == 'float':
                return 'float'
            return 'int'
        
        # Relational operators
        elif node.operator in ['<', '>', '<=', '>=']:
            if not self.is_numeric(left_type) or not self.is_numeric(right_type):
                self.error(
                    f"Operator '{node.operator}' requires numeric operands, "
                    f"got {left_type} and {right_type}",
                    node
                )
            return 'bool'
        
        # Equality operators
        elif node.operator in ['==', '!=']:
            if not self.is_compatible_type(left_type, right_type):
                self.error(
                    f"Cannot compare {left_type} with {right_type}",
                    node
                )
            return 'bool'
        
        # Logical operators
        elif node.operator in ['and', 'or']:
            if left_type != 'bool' or right_type != 'bool':
                self.error(
                    f"Logical operator '{node.operator}' requires boolean operands, "
                    f"got {left_type} and {right_type}",
                    node
                )
            return 'bool'
        
        else:
            self.error(f"Unknown binary operator: {node.operator}", node)
    
    def analyze_UnaryOp(self, node: UnaryOp) -> str:
        """Analyze unary operation"""
        operand_type = self.analyze(node.operand)
        
        if node.operator == '-':
            if not self.is_numeric(operand_type):
                self.error(f"Unary '-' requires numeric operand, got {operand_type}", node)
            return operand_type
        
        elif node.operator == 'not':
            if operand_type != 'bool':
                self.error(f"Operator 'not' requires boolean operand, got {operand_type}", node)
            return 'bool'
        
        else:
            self.error(f"Unknown unary operator: {node.operator}", node)
    
    def analyze_Literal(self, node: Literal) -> str:
        """Analyze literal value"""
        return node.type
    
    def analyze_Identifier(self, node: Identifier) -> str:
        """Analyze identifier (variable reference)"""
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.error(f"Undefined variable '{node.name}'", node)
        
        if symbol['type'] != 'variable':
            self.error(f"'{node.name}' is not a variable", node)
        
        return symbol['data_type']
    
    def analyze_IfStatement(self, node: IfStatement) -> str:
        """Analyze if statement"""
        # Check condition type
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            self.error(f"If condition must be boolean, got {cond_type}", node)
        
        # Analyze then block
        self.enter_scope()
        for stmt in node.then_block:
            self.analyze(stmt)
        self.exit_scope()
        
        # Analyze else block if present
        if node.else_block:
            self.enter_scope()
            for stmt in node.else_block:
                self.analyze(stmt)
            self.exit_scope()
        
        return 'void'
    
    def analyze_WhileStatement(self, node: WhileStatement) -> str:
        """Analyze while loop"""
        # Check condition type
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            self.error(f"While condition must be boolean, got {cond_type}", node)
        
        # Analyze body
        self.enter_scope()
        for stmt in node.body:
            self.analyze(stmt)
        self.exit_scope()
        
        return 'void'
    
    def analyze_ForStatement(self, node: ForStatement) -> str:
        """Analyze for loop"""
        self.enter_scope()
        
        # Analyze initialization
        self.analyze(node.init)
        
        # Check condition type
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            self.error(f"For loop condition must be boolean, got {cond_type}", node)
        
        # Analyze update
        self.analyze(node.update)
        
        # Analyze body
        for stmt in node.body:
            self.analyze(stmt)
        
        self.exit_scope()
        return 'void'
    
    def analyze_FunctionDef(self, node: FunctionDef) -> str:
        """Analyze function definition"""
        # Check if function already exists
        if node.name in self.current_scope.symbols:
            self.error(f"Function '{node.name}' already declared", node)
        
        # Add function to symbol table
        self.current_scope.define(
            node.name,
            symbol_type='function',
            data_type=node.return_type,
            parameters=node.parameters
        )
        
        # Enter function scope
        self.enter_scope()
        old_function = self.current_function
        self.current_function = node
        
        # Add parameters to function scope
        for param_type, param_name in node.parameters:
            self.current_scope.define(
                param_name,
                symbol_type='variable',
                data_type=param_type,
                initialized=True
            )
        
        # Analyze function body
        has_return = False
        for stmt in node.body:
            self.analyze(stmt)
            if isinstance(stmt, ReturnStatement):
                has_return = True
        
        # Check if non-void function has return statement
        if node.return_type != 'void' and not has_return:
            self.error(f"Function '{node.name}' must return a value of type {node.return_type}", node)
        
        # Exit function scope
        self.current_function = old_function
        self.exit_scope()
        
        return 'void'
    
    def analyze_FunctionCall(self, node: FunctionCall) -> str:
        """Analyze function call"""
        # Check if function exists
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.error(f"Undefined function '{node.name}'", node)
        
        if symbol['type'] != 'function':
            self.error(f"'{node.name}' is not a function", node)
        
        # Check argument count
        expected_params = symbol['parameters']
        if len(node.arguments) != len(expected_params):
            self.error(
                f"Function '{node.name}' expects {len(expected_params)} arguments, "
                f"got {len(node.arguments)}",
                node
            )
        
        # Type check arguments
        for i, (arg, (param_type, param_name)) in enumerate(zip(node.arguments, expected_params)):
            arg_type = self.analyze(arg)
            if not self.is_compatible_type(param_type, arg_type):
                self.error(
                    f"Argument {i+1} of function '{node.name}' expects {param_type}, "
                    f"got {arg_type}",
                    node
                )
        
        return symbol['data_type']
    
    def analyze_ReturnStatement(self, node: ReturnStatement) -> str:
        """Analyze return statement"""
        if not self.current_function:
            self.error("Return statement outside function", node)
        
        expected_type = self.current_function.return_type
        
        if node.value:
            actual_type = self.analyze(node.value)
            if not self.is_compatible_type(expected_type, actual_type):
                self.error(
                    f"Return type mismatch: expected {expected_type}, got {actual_type}",
                    node
                )
        else:
            if expected_type != 'void':
                self.error(f"Function must return a value of type {expected_type}", node)
        
        return 'void'
    
    def analyze_PrintStatement(self, node: PrintStatement) -> str:
        """Analyze print statement"""
        for expr in node.expressions:
            self.analyze(expr)
        return 'void'
    
    def analyze_Block(self, node: Block) -> str:
        """Analyze a block of statements"""
        for stmt in node.statements:
            self.analyze(stmt)
        return 'void'
    
    def analyze_ArrayLiteral(self, node: ArrayLiteral) -> str:
        """Analyze array literal [1, 2, 3]"""
        if not node.elements:
            return 'int[]'  # Empty array defaults to int[]
        
        # All elements should have the same type
        first_type = self.analyze(node.elements[0])
        for elem in node.elements[1:]:
            elem_type = self.analyze(elem)
            if not self.is_compatible_type(first_type, elem_type):
                self.error(f"Array elements must have consistent types, got {first_type} and {elem_type}", node)
        
        # Remove '[]' suffix if present, then add it back
        base_type = first_type.replace('[]', '')
        return base_type + '[]'
    
    def analyze_ArrayAccess(self, node: ArrayAccess) -> str:
        """Analyze array element access arr[index]"""
        # Get array type
        array_type = self.analyze(node.array)
        
        if not array_type.endswith('[]'):
            self.error(f"Cannot index non-array type '{array_type}'", node)
        
        # Check index type
        index_type = self.analyze(node.index)
        if index_type != 'int':
            self.error(f"Array index must be int, got {index_type}", node)
        
        # Return element type (remove [] suffix)
        return array_type[:-2]
    
    def analyze_ArrayAssignment(self, node: ArrayAssignment) -> str:
        """Analyze array element assignment arr[index] = value"""
        # Check if array exists
        symbol = self.current_scope.lookup(node.array)
        if not symbol:
            self.error(f"Undefined array '{node.array}'", node)
        
        array_type = symbol['data_type']
        if not array_type.endswith('[]'):
            self.error(f"'{node.array}' is not an array", node)
        
        # Check index type
        index_type = self.analyze(node.index)
        if index_type != 'int':
            self.error(f"Array index must be int, got {index_type}", node)
        
        # Check value type
        value_type = self.analyze(node.value)
        element_type = array_type[:-2]
        
        if not self.is_compatible_type(element_type, value_type):
            self.error(
                f"Type mismatch: cannot assign {value_type} to {element_type} array element",
                node
            )
        
        return 'void'
    
    def analyze_BuiltInCall(self, node: BuiltInCall) -> str:
        """Analyze built-in function call"""
        func = node.function.lower()
        args = node.arguments
        
        # len(array) or len(string) -> int
        if func == 'len':
            if len(args) != 1:
                self.error(f"len() expects 1 argument, got {len(args)}", node)
            arg_type = self.analyze(args[0])
            if not (arg_type.endswith('[]') or arg_type == 'string'):
                self.error(f"len() requires array or string, got {arg_type}", node)
            return 'int'
        
        # random(min, max) -> int
        elif func == 'random':
            if len(args) != 2:
                self.error(f"random() expects 2 arguments, got {len(args)}", node)
            min_type = self.analyze(args[0])
            max_type = self.analyze(args[1])
            if not self.is_numeric(min_type) or not self.is_numeric(max_type):
                self.error(f"random() requires numeric arguments, got {min_type} and {max_type}", node)
            return 'int'
        
        # substr(string, start, end) -> string
        elif func == 'substr':
            if len(args) != 3:
                self.error(f"substr() expects 3 arguments, got {len(args)}", node)
            str_type = self.analyze(args[0])
            start_type = self.analyze(args[1])
            end_type = self.analyze(args[2])
            if str_type != 'string':
                self.error(f"substr() first argument must be string, got {str_type}", node)
            if start_type != 'int' or end_type != 'int':
                self.error(f"substr() indices must be int, got {start_type} and {end_type}", node)
            return 'string'
        
        # concat(string, string) -> string
        elif func == 'concat':
            if len(args) != 2:
                self.error(f"concat() expects 2 arguments, got {len(args)}", node)
            arg1_type = self.analyze(args[0])
            arg2_type = self.analyze(args[1])
            if arg1_type != 'string' or arg2_type != 'string':
                self.error(f"concat() requires string arguments, got {arg1_type} and {arg2_type}", node)
            return 'string'
        
        # input(prompt) -> string
        elif func == 'input':
            if len(args) != 1:
                self.error(f"input() expects 1 argument, got {len(args)}", node)
            prompt_type = self.analyze(args[0])
            if prompt_type != 'string':
                self.error(f"input() prompt must be string, got {prompt_type}", node)
            return 'string'
        
        else:
            self.error(f"Unknown built-in function: {func}", node)
    
    # ============= Helper Methods =============
    
    def is_numeric(self, type_name: str) -> bool:
        """Check if type is numeric"""
        return type_name in ['int', 'float']
    
    def is_compatible_type(self, expected: str, actual: str) -> bool:
        """Check if actual type is compatible with expected type"""
        if expected == actual:
            return True
        # Allow int to float coercion
        if expected == 'float' and actual == 'int':
            return True
        return False
    
    def get_symbol_table_string(self) -> str:
        """Get string representation of symbol table for debugging"""
        result = []
        
        def traverse(scope, indent=0):
            prefix = "  " * indent
            result.append(f"{prefix}Scope Level {scope.scope_level}:")
            for name, info in scope.symbols.items():
                result.append(f"{prefix}  {name}: {info}")
        
        traverse(self.global_scope)
        return "\n".join(result)


def test_semantic_analyzer():
    """Test the semantic analyzer"""
    test_code = """
    function int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    int x = 5;
    int result = factorial(x);
    print("Result:", result);
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(ast)
        print("=== Semantic Analysis Output ===")
        print("✓ No semantic errors found")
        print("\n=== Symbol Table ===")
        print(analyzer.get_symbol_table_string())
    except SemanticError as e:
        print(f"Semantic Error: {e}")


if __name__ == "__main__":
    test_semantic_analyzer()
