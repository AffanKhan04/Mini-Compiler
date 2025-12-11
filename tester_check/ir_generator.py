"""
Intermediate Code Generator for NumCalc Language
Phase 4: Generates three-address code (TAC) from AST
Three-address code format: result = operand1 operator operand2
"""

from parser import *
from typing import List, Optional


class ThreeAddressCode:
    """Represents a single three-address code instruction"""
    
    def __init__(self, op: str, arg1=None, arg2=None, result=None):
        self.op = op  # Operation: +, -, *, /, assign, call, etc.
        self.arg1 = arg1  # First operand
        self.arg2 = arg2  # Second operand
        self.result = result  # Result variable
    
    def __repr__(self):
        if self.op == 'assign':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'label':
            return f"{self.result}:"
        elif self.op == 'goto':
            return f"goto {self.result}"
        elif self.op == 'if_false':
            return f"if_false {self.arg1} goto {self.result}"
        elif self.op == 'if_true':
            return f"if_true {self.arg1} goto {self.result}"
        elif self.op == 'param':
            return f"param {self.arg1}"
        elif self.op == 'param_decl':
            return f"param_decl {self.arg1}"
        elif self.op == 'call':
            if self.result:
                return f"{self.result} = call {self.arg1}, {self.arg2}"
            else:
                return f"call {self.arg1}, {self.arg2}"
        elif self.op == 'return':
            if self.arg1:
                return f"return {self.arg1}"
            else:
                return "return"
        elif self.op == 'print':
            return f"print {self.arg1}"
        elif self.op == 'begin_func':
            return f"begin_func {self.arg1}"
        elif self.op == 'end_func':
            return f"end_func {self.arg1}"
        elif self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        else:
            return f"{self.result} = {self.op} {self.arg1}"


class IRGenerator:
    """Generates intermediate representation (three-address code) from AST"""
    
    def __init__(self):
        self.code: List[ThreeAddressCode] = []
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self) -> str:
        """Generate a new temporary variable"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label"""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def emit(self, op: str, arg1=None, arg2=None, result=None):
        """Emit a three-address code instruction"""
        tac = ThreeAddressCode(op, arg1, arg2, result)
        self.code.append(tac)
        return tac
    
    def generate(self, node: ASTNode) -> Optional[str]:
        """
        Generate IR for a node
        Returns the name of the variable/temp holding the result
        """
        method_name = f'generate_{node.__class__.__name__}'
        method = getattr(self, method_name, None)
        
        if method:
            return method(node)
        else:
            raise NotImplementedError(f"No IR generation method for {node.__class__.__name__}")
    
    # ============= IR Generation Methods =============
    
    def generate_Program(self, node: Program) -> None:
        """Generate IR for entire program"""
        for statement in node.statements:
            self.generate(statement)
    
    def generate_VarDeclaration(self, node: VarDeclaration) -> None:
        """Generate IR for variable declaration"""
        if node.initializer:
            value = self.generate(node.initializer)
            self.emit('assign', value, None, node.name)
    
    def generate_Assignment(self, node: Assignment) -> None:
        """Generate IR for assignment"""
        value = self.generate(node.value)
        self.emit('assign', value, None, node.name)
    
    def generate_BinaryOp(self, node: BinaryOp) -> str:
        """Generate IR for binary operation"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        result = self.new_temp()
        self.emit(node.operator, left, right, result)
        return result
    
    def generate_UnaryOp(self, node: UnaryOp) -> str:
        """Generate IR for unary operation"""
        operand = self.generate(node.operand)
        result = self.new_temp()
        self.emit(node.operator, operand, None, result)
        return result
    
    def generate_Literal(self, node: Literal) -> str:
        """Generate IR for literal (return value directly)"""
        if isinstance(node.value, str):
            return f'"{node.value}"'
        if isinstance(node.value, bool):
            return 'true' if node.value else 'false'
        return str(node.value)
    
    def generate_Identifier(self, node: Identifier) -> str:
        """Generate IR for identifier (return name)"""
        return node.name
    
    def generate_IfStatement(self, node: IfStatement) -> None:
        """Generate IR for if statement"""
        # Generate condition
        cond = self.generate(node.condition)
        
        # Create labels
        false_label = self.new_label()
        end_label = self.new_label()
        
        # If condition is false, jump to false_label
        self.emit('if_false', cond, None, false_label)
        
        # Generate then block
        for stmt in node.then_block:
            self.generate(stmt)
        
        # Jump to end after then block
        if node.else_block:
            self.emit('goto', None, None, end_label)
        
        # False label
        self.emit('label', None, None, false_label)
        
        # Generate else block if present
        if node.else_block:
            for stmt in node.else_block:
                self.generate(stmt)
            self.emit('label', None, None, end_label)
    
    def generate_WhileStatement(self, node: WhileStatement) -> None:
        """Generate IR for while loop"""
        # Create labels
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start label
        self.emit('label', None, None, start_label)
        
        # Generate condition
        cond = self.generate(node.condition)
        
        # If condition is false, exit loop
        self.emit('if_false', cond, None, end_label)
        
        # Generate body
        for stmt in node.body:
            self.generate(stmt)
        
        # Jump back to start
        self.emit('goto', None, None, start_label)
        
        # End label
        self.emit('label', None, None, end_label)
    
    def generate_ForStatement(self, node: ForStatement) -> None:
        """Generate IR for for loop"""
        # Generate initialization
        self.generate(node.init)
        
        # Create labels
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start label
        self.emit('label', None, None, start_label)
        
        # Generate condition
        cond = self.generate(node.condition)
        
        # If condition is false, exit loop
        self.emit('if_false', cond, None, end_label)
        
        # Generate body
        for stmt in node.body:
            self.generate(stmt)
        
        # Generate update
        self.generate(node.update)
        
        # Jump back to start
        self.emit('goto', None, None, start_label)
        
        # End label
        self.emit('label', None, None, end_label)
    
    def generate_FunctionDef(self, node: FunctionDef) -> None:
        """Generate IR for function definition"""
        # Begin function
        self.emit('begin_func', node.name, None, None)
        
        # Emit parameter setup - store parameter names for the interpreter
        for param_type, param_name in node.parameters:
            self.emit('param_decl', param_name, None, None)
        
        # Generate body
        for stmt in node.body:
            self.generate(stmt)
        
        # End function
        self.emit('end_func', node.name, None, None)
    
    def generate_FunctionCall(self, node: FunctionCall) -> str:
        """Generate IR for function call"""
        # Push parameters
        for arg in node.arguments:
            arg_val = self.generate(arg)
            self.emit('param', arg_val, None, None)
        
        # Call function
        result = self.new_temp()
        self.emit('call', node.name, len(node.arguments), result)
        return result
    
    def generate_ReturnStatement(self, node: ReturnStatement) -> None:
        """Generate IR for return statement"""
        if node.value:
            value = self.generate(node.value)
            self.emit('return', value, None, None)
        else:
            self.emit('return', None, None, None)
    
    def generate_PrintStatement(self, node: PrintStatement) -> None:
        """Generate IR for print statement"""
        for expr in node.expressions:
            value = self.generate(expr)
            self.emit('print', value, None, None)
    
    def generate_Block(self, node: Block) -> None:
        """Generate IR for block"""
        for stmt in node.statements:
            self.generate(stmt)
    
    def generate_ArrayLiteral(self, node: ArrayLiteral) -> str:
        """Generate IR for array literal"""
        temp = self.new_temp()
        # Emit array creation instruction - result field holds the temp variable
        self.emit('array_init', None, None, temp)
        
        # Add each element - result field holds the array name, arg1 is the value
        for i, elem in enumerate(node.elements):
            elem_val = self.generate(elem)
            self.emit('array_append', elem_val, None, temp)
        
        return temp
    
    def generate_ArrayAccess(self, node: ArrayAccess) -> str:
        """Generate IR for array access"""
        array_val = self.generate(node.array)
        index_val = self.generate(node.index)
        temp = self.new_temp()
        self.emit('array_get', array_val, index_val, temp)
        return temp
    
    def generate_ArrayAssignment(self, node: ArrayAssignment) -> None:
        """Generate IR for array assignment"""
        index_val = self.generate(node.index)
        value_val = self.generate(node.value)
        # array_set: array[index] = value
        # Format: result=array_name, arg1=index, arg2=value
        self.emit('array_set', index_val, value_val, node.array)
    
    def generate_BuiltInCall(self, node: BuiltInCall) -> str:
        """Generate IR for built-in function call"""
        func = node.function.lower()
        temp = self.new_temp()
        
        if func == 'len':
            arg = self.generate(node.arguments[0])
            self.emit('builtin_len', arg, None, temp)
        
        elif func == 'random':
            min_val = self.generate(node.arguments[0])
            max_val = self.generate(node.arguments[1])
            self.emit('builtin_random', min_val, max_val, temp)
        
        elif func == 'substr':
            str_val = self.generate(node.arguments[0])
            start_val = self.generate(node.arguments[1])
            end_val = self.generate(node.arguments[2])
            self.emit('builtin_substr', str_val, (start_val, end_val), temp)
        
        elif func == 'concat':
            arg1 = self.generate(node.arguments[0])
            arg2 = self.generate(node.arguments[1])
            self.emit('builtin_concat', arg1, arg2, temp)
        
        elif func == 'input':
            prompt = self.generate(node.arguments[0])
            self.emit('builtin_input', prompt, None, temp)
        
        return temp
    
    def get_code_string(self) -> str:
        """Get string representation of generated code"""
        return '\n'.join(str(instr) for instr in self.code)


def test_ir_generator():
    """Test the IR generator"""
    test_code = """
    function int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    int x = 5;
    int result = factorial(x);
    print(result);
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    ir_gen = IRGenerator()
    ir_gen.generate(ast)
    
    print("=== Intermediate Code (Three-Address Code) ===")
    print(ir_gen.get_code_string())


if __name__ == "__main__":
    test_ir_generator()
