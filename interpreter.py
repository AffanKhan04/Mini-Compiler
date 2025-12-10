"""
Interpreter/Code Generator for NumCalc Language
Phase 6: Executes the intermediate code (three-address code)
Acts as a virtual machine interpreter
"""

from ir_generator import ThreeAddressCode
from typing import Dict, List, Any, Optional
import sys


class RuntimeError(Exception):
    """Runtime execution error"""
    pass


class Interpreter:
    """Interprets and executes three-address code"""
    
    def __init__(self, code: List[ThreeAddressCode]):
        self.code = code
        self.variables: Dict[str, Any] = {}  # Variable storage
        self.functions: Dict[str, int] = {}  # Function name -> start index
        self.call_stack: List[Dict] = []  # Function call stack
        self.pc = 0  # Program counter
        self.output: List[str] = []  # Captured output
        
        # Build function table
        self._build_function_table()
    
    def _build_function_table(self):
        """Build table of function start addresses"""
        for i, instr in enumerate(self.code):
            if instr.op == 'begin_func':
                self.functions[instr.arg1] = i + 1
    
    def execute(self) -> List[str]:
        """Execute the program"""
        self.pc = 0
        
        while self.pc < len(self.code):
            instr = self.code[self.pc]
            old_pc = self.pc
            self.execute_instruction(instr)
            # Only increment pc if instruction didn't change it
            if self.pc == old_pc:
                self.pc += 1
        
        return self.output
    
    def execute_instruction(self, instr: ThreeAddressCode):
        """Execute a single instruction"""
        
        if instr.op == 'assign':
            # Assignment: result = arg1
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = value
        
        elif instr.op in ['+', '-', '*', '/', '%', '**']:
            # Arithmetic operations
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            
            if instr.op == '+':
                result = left + right
            elif instr.op == '-':
                result = left - right
            elif instr.op == '*':
                result = left * right
            elif instr.op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                if isinstance(left, int) and isinstance(right, int):
                    result = left // right
                else:
                    result = left / right
            elif instr.op == '%':
                if right == 0:
                    raise RuntimeError("Modulo by zero")
                result = left % right
            elif instr.op == '**':
                result = left ** right
            
            self.variables[instr.result] = result
        
        elif instr.op in ['<', '>', '<=', '>=', '==', '!=']:
            # Relational operations
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            
            if instr.op == '<':
                result = left < right
            elif instr.op == '>':
                result = left > right
            elif instr.op == '<=':
                result = left <= right
            elif instr.op == '>=':
                result = left >= right
            elif instr.op == '==':
                result = left == right
            elif instr.op == '!=':
                result = left != right
            
            self.variables[instr.result] = result
        
        elif instr.op in ['and', 'or']:
            # Logical operations
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            
            if instr.op == 'and':
                result = left and right
            elif instr.op == 'or':
                result = left or right
            
            self.variables[instr.result] = result
        
        elif instr.op == 'not':
            # Logical NOT
            operand = self.get_value(instr.arg1)
            self.variables[instr.result] = not operand
        
        elif instr.op == 'label':
            # Label - no operation, just a marker
            pass
        
        elif instr.op == 'goto':
            # Unconditional jump
            label = instr.result
            self.pc = self.find_label(label)
        
        elif instr.op == 'if_false':
            # Conditional jump (if arg1 is false, goto label)
            condition = self.get_value(instr.arg1)
            if not condition:
                label = instr.result
                self.pc = self.find_label(label)
        
        elif instr.op == 'if_true':
            # Conditional jump (if arg1 is true, goto label)
            condition = self.get_value(instr.arg1)
            if condition:
                label = instr.result
                self.pc = self.find_label(label)
        
        elif instr.op == 'print':
            # Print value
            value = self.get_value(instr.arg1)
            output_str = str(value)
            self.output.append(output_str)
            print(output_str, end=' ')
        
        elif instr.op == 'param':
            # Push parameter onto call stack (handled in call)
            pass
        
        elif instr.op == 'param_decl':
            # Declare a parameter variable (values come from call stack)
            if self.call_stack:
                frame = self.call_stack[-1]
                param_name = instr.arg1
                # Get the next parameter value from the frame
                if 'param_index' not in frame:
                    frame['param_index'] = 0
                if frame['param_index'] < len(frame['params']):
                    self.variables[param_name] = frame['params'][frame['param_index']]
                    frame['param_index'] += 1
        
        elif instr.op == 'call':
            # Function call
            func_name = instr.arg1
            num_params = instr.arg2
            
            # Save current state - return to instruction AFTER this call
            return_address = self.pc + 1
            saved_vars = self.variables.copy()
            
            # Get parameters from previous param instructions
            params = []
            for i in range(num_params):
                param_instr = self.code[self.pc - num_params + i]
                if param_instr.op == 'param':
                    params.append(self.get_value(param_instr.arg1))
            
            # Push call frame
            self.call_stack.append({
                'return_address': return_address,
                'saved_vars': saved_vars,
                'params': params,
                'return_value': None
            })
            
            # Jump to function
            if func_name not in self.functions:
                raise RuntimeError(f"Undefined function: {func_name}")
            self.pc = self.functions[func_name]
        
        elif instr.op == 'return':
            # Return from function
            if not self.call_stack:
                # Return from main program
                self.pc = len(self.code)
                return
            
            return_value = None
            if instr.arg1 is not None:
                return_value = self.get_value(instr.arg1)
            
            # Pop call frame
            frame = self.call_stack.pop()
            frame['return_value'] = return_value
            
            # Restore state
            self.variables = frame['saved_vars']
            
            # Store return value in result variable
            if return_value is not None:
                # Find the call instruction (which is one before return_address)
                call_pc = frame['return_address'] - 1
                call_instr = self.code[call_pc]
                if call_instr.result:
                    self.variables[call_instr.result] = return_value
            
            # Jump back
            self.pc = frame['return_address']
        
        elif instr.op == 'begin_func':
            # Function begin marker - skip to end
            func_name = instr.arg1
            self.pc = self.find_function_end(func_name)
        
        elif instr.op == 'end_func':
            # Function end marker
            pass
        
        elif instr.op == 'array_init':
            # Initialize empty array
            self.variables[instr.result] = []
        
        elif instr.op == 'array_append':
            # Append element to array
            array = self.variables.get(instr.result, [])
            value = self.get_value(instr.arg1)
            array.append(value)
            self.variables[instr.result] = array
        
        elif instr.op == 'array_get':
            # Get array element: result = array[index]
            array = self.get_value(instr.arg1)
            index = self.get_value(instr.arg2)
            
            if not isinstance(array, list):
                raise RuntimeError(f"Cannot index non-array type")
            if not isinstance(index, int):
                raise RuntimeError(f"Array index must be integer")
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Array index out of bounds: {index}")
            
            self.variables[instr.result] = array[index]
        
        elif instr.op == 'array_set':
            # Set array element: array[index] = value
            array = self.variables.get(instr.result)
            if not isinstance(array, list):
                raise RuntimeError(f"Cannot index non-array type")
            
            index = self.get_value(instr.arg1)
            value = self.get_value(instr.arg2)
            
            if not isinstance(index, int):
                raise RuntimeError(f"Array index must be integer")
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Array index out of bounds: {index}")
            
            array[index] = value
        
        elif instr.op == 'builtin_len':
            # len(array) or len(string)
            arg = self.get_value(instr.arg1)
            if isinstance(arg, (list, str)):
                self.variables[instr.result] = len(arg)
            else:
                raise RuntimeError(f"len() requires array or string")
        
        elif instr.op == 'builtin_random':
            # random(min, max)
            import random
            min_val = self.get_value(instr.arg1)
            max_val = self.get_value(instr.arg2)
            self.variables[instr.result] = random.randint(int(min_val), int(max_val))
        
        elif instr.op == 'builtin_substr':
            # substr(string, start, end)
            string = self.get_value(instr.arg1)
            start, end = instr.arg2
            start_val = self.get_value(start)
            end_val = self.get_value(end)
            
            if not isinstance(string, str):
                raise RuntimeError(f"substr() requires string")
            
            self.variables[instr.result] = string[int(start_val):int(end_val)]
        
        elif instr.op == 'builtin_concat':
            # concat(string1, string2)
            str1 = self.get_value(instr.arg1)
            str2 = self.get_value(instr.arg2)
            
            if not isinstance(str1, str) or not isinstance(str2, str):
                raise RuntimeError(f"concat() requires string arguments")
            
            self.variables[instr.result] = str1 + str2
        
        elif instr.op == 'builtin_input':
            # input(prompt)
            prompt = self.get_value(instr.arg1)
            
            if not isinstance(prompt, str):
                raise RuntimeError(f"input() prompt must be string")
            
            try:
                user_input = input(prompt)
                self.variables[instr.result] = user_input
            except EOFError:
                self.variables[instr.result] = ""
    
    def get_value(self, operand) -> Any:
        """Get the value of an operand (variable or constant)"""
        if operand is None:
            return None
        
        # Check if it's a boolean
        if operand is True or operand is False:
            return operand
        
        # Check if it's already a number
        if isinstance(operand, (int, float)):
            return operand
        
        # String literal
        if isinstance(operand, str):
            if operand.startswith('"') and operand.endswith('"'):
                return operand[1:-1]
            
            # Try to parse as number
            try:
                if '.' in operand:
                    return float(operand)
                return int(operand)
            except ValueError:
                pass
            
            # Boolean literals
            if operand == 'true':
                return True
            elif operand == 'false':
                return False
            
            # Must be a variable
            if operand not in self.variables:
                raise RuntimeError(f"Undefined variable: {operand}")
            return self.variables[operand]
        
        return operand
    
    def find_label(self, label: str) -> int:
        """Find the index of a label"""
        for i, instr in enumerate(self.code):
            if instr.op == 'label' and instr.result == label:
                return i
        raise RuntimeError(f"Label not found: {label}")
    
    def find_function_end(self, func_name: str) -> int:
        """Find the end of a function - returns index after end_func"""
        start = self.pc
        depth = 0
        for i in range(start, len(self.code)):
            if self.code[i].op == 'begin_func':
                depth += 1
            elif self.code[i].op == 'end_func':
                depth -= 1
                if depth == 0:
                    return i + 1  # Return position AFTER end_func
        return len(self.code)
    
    def get_output(self) -> str:
        """Get captured output as string"""
        return ' '.join(self.output)


def test_interpreter():
    """Test the interpreter"""
    from lexer import Lexer
    from parser import Parser
    from ir_generator import IRGenerator
    from optimizer import Optimizer
    
    test_code = """
    function int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    int x = 5;
    int result = factorial(x);
    print("Factorial of", x, "is", result);
    """
    
    print("=== Source Code ===")
    print(test_code)
    
    # Compile
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    ir_gen = IRGenerator()
    ir_gen.generate(ast)
    
    optimizer = Optimizer(ir_gen.code)
    optimized_code = optimizer.optimize()
    
    print("\n=== Optimized IR ===")
    for instr in optimized_code:
        print(instr)
    
    # Execute
    print("\n=== Program Output ===")
    interpreter = Interpreter(optimized_code)
    interpreter.execute()
    print()  # Newline after output


if __name__ == "__main__":
    test_interpreter()
