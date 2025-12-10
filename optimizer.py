"""
Optimizer for NumCalc Language
Phase 5: Performs basic optimizations on intermediate code
- Constant folding
- Dead code elimination
- Copy propagation
"""

from ir_generator import ThreeAddressCode, IRGenerator
from typing import List, Set, Dict


class Optimizer:
    """Performs optimizations on three-address code"""
    
    def __init__(self, code: List[ThreeAddressCode]):
        self.code = code
        self.optimized_code: List[ThreeAddressCode] = []
    
    def optimize(self) -> List[ThreeAddressCode]:
        """Apply all optimizations"""
        # Apply constant folding
        self.code = self.constant_folding(self.code)
        
        # Apply copy propagation
        self.code = self.copy_propagation(self.code)
        
        # Apply dead code elimination
        self.code = self.dead_code_elimination(self.code)
        
        return self.code
    
    def constant_folding(self, code: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        """
        Constant folding: Evaluate constant expressions at compile time
        Example: t1 = 2 + 3 => t1 = 5
        """
        optimized = []
        constants: Dict[str, any] = {}  # Map variable names to constant values
        
        for instr in code:
            # Clear all constants when encountering control flow (labels, gotos)
            # This prevents incorrect optimization across loop boundaries
            if instr.op in ['label', 'goto', 'if_false', 'if_true']:
                constants.clear()
                optimized.append(instr)
                continue
            
            # Track constant assignments
            if instr.op == 'assign':
                if self.is_constant(instr.arg1):
                    constants[instr.result] = self.get_constant_value(instr.arg1)
                    optimized.append(instr)
                elif instr.arg1 in constants:
                    # Propagate constant
                    value = constants[instr.arg1]
                    optimized.append(ThreeAddressCode('assign', value, None, instr.result))
                    constants[instr.result] = value
                else:
                    optimized.append(instr)
                    # Variable is no longer constant
                    if instr.result in constants:
                        del constants[instr.result]
            
            # Fold binary operations with constant operands
            elif instr.op in ['+', '-', '*', '/', '%', '**', '<', '>', '<=', '>=', '==', '!=']:
                arg1_val = constants.get(instr.arg1) if instr.arg1 in constants else self.get_constant_value(instr.arg1) if self.is_constant(instr.arg1) else None
                arg2_val = constants.get(instr.arg2) if instr.arg2 in constants else self.get_constant_value(instr.arg2) if self.is_constant(instr.arg2) else None
                
                if arg1_val is not None and arg2_val is not None:
                    # Both operands are constants, evaluate at compile time
                    try:
                        result_val = self.evaluate_operation(instr.op, arg1_val, arg2_val)
                        optimized.append(ThreeAddressCode('assign', result_val, None, instr.result))
                        constants[instr.result] = result_val
                    except:
                        # If evaluation fails, keep original instruction
                        optimized.append(instr)
                else:
                    optimized.append(instr)
                    # Result is no longer constant
                    if instr.result in constants:
                        del constants[instr.result]
            
            # Fold unary operations
            elif instr.op in ['-', 'not']:
                arg_val = constants.get(instr.arg1) if instr.arg1 in constants else self.get_constant_value(instr.arg1) if self.is_constant(instr.arg1) else None
                
                if arg_val is not None:
                    if instr.op == '-':
                        result_val = -arg_val
                    elif instr.op == 'not':
                        result_val = not arg_val
                    optimized.append(ThreeAddressCode('assign', result_val, None, instr.result))
                    constants[instr.result] = result_val
                else:
                    optimized.append(instr)
            
            else:
                # For all other instructions, clear constants that might be modified
                if instr.result and instr.result in constants:
                    del constants[instr.result]
                optimized.append(instr)
        
        return optimized
    
    def copy_propagation(self, code: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        """
        Copy propagation: Replace variable with its value
        Example: x = y; z = x + 1 => x = y; z = y + 1
        """
        optimized = []
        copies: Dict[str, str] = {}  # Map variable to its copy source
        
        for instr in code:
            # Clear all copies when encountering control flow (labels, gotos)
            # This prevents incorrect optimization across loop boundaries
            if instr.op in ['label', 'goto', 'if_false', 'if_true']:
                copies.clear()
                optimized.append(instr)
                continue
            
            # Track simple copies
            if instr.op == 'assign' and isinstance(instr.arg1, str) and not self.is_constant(instr.arg1):
                copies[instr.result] = instr.arg1
                optimized.append(instr)
            
            # Propagate copies in binary operations
            elif instr.op in ['+', '-', '*', '/', '%', '**', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']:
                arg1 = copies.get(instr.arg1, instr.arg1)
                arg2 = copies.get(instr.arg2, instr.arg2)
                optimized.append(ThreeAddressCode(instr.op, arg1, arg2, instr.result))
                # Result is not a copy
                if instr.result in copies:
                    del copies[instr.result]
            
            # Propagate copies in unary operations
            elif instr.op in ['-', 'not']:
                arg1 = copies.get(instr.arg1, instr.arg1)
                optimized.append(ThreeAddressCode(instr.op, arg1, None, instr.result))
                if instr.result in copies:
                    del copies[instr.result]
            
            # Propagate in other instructions
            else:
                new_instr = ThreeAddressCode(instr.op, instr.arg1, instr.arg2, instr.result)
                if instr.arg1 and isinstance(instr.arg1, str) and instr.arg1 in copies:
                    new_instr.arg1 = copies[instr.arg1]
                if instr.arg2 and isinstance(instr.arg2, str) and instr.arg2 in copies:
                    new_instr.arg2 = copies[instr.arg2]
                optimized.append(new_instr)
                
                # Clear copy information if variable is modified
                if instr.result and instr.result in copies:
                    del copies[instr.result]
        
        return optimized
    
    def dead_code_elimination(self, code: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        """
        Dead code elimination: Remove unused variable assignments
        """
        # First pass: identify all used variables
        used_vars: Set[str] = set()
        
        for instr in code:
            # Add variables used as operands
            if instr.arg1 and isinstance(instr.arg1, str) and not self.is_constant(instr.arg1):
                used_vars.add(instr.arg1)
            if instr.arg2 and isinstance(instr.arg2, str) and not self.is_constant(instr.arg2):
                used_vars.add(instr.arg2)
            
            # Variables used in control flow, calls, returns, prints are live
            if instr.op in ['if_false', 'if_true', 'return', 'print', 'param', 'call']:
                if instr.arg1 and isinstance(instr.arg1, str):
                    used_vars.add(instr.arg1)
                if instr.result and isinstance(instr.result, str) and instr.op != 'label':
                    used_vars.add(instr.result)
        
        # Second pass: keep only instructions that define used variables or have side effects
        optimized = []
        
        for instr in code:
            # Always keep control flow, function markers, prints, returns, calls
            if instr.op in ['label', 'goto', 'if_false', 'if_true', 'begin_func', 'end_func', 
                           'print', 'return', 'call', 'param']:
                optimized.append(instr)
            
            # Keep assignments to used variables
            elif instr.result:
                # Keep if result is used, or if it's a regular variable (not temp)
                if instr.result in used_vars or not instr.result.startswith('t'):
                    optimized.append(instr)
            
            else:
                optimized.append(instr)
        
        return optimized
    
    # ============= Helper Methods =============
    
    def is_constant(self, value) -> bool:
        """Check if value is a constant literal"""
        if isinstance(value, (int, float, bool)):
            return True
        if isinstance(value, str):
            # Check if it's a string literal (in quotes) or a number
            if value.startswith('"') and value.endswith('"'):
                return True
            try:
                float(value)
                return True
            except:
                return False
        return False
    
    def get_constant_value(self, value):
        """Extract constant value"""
        if isinstance(value, (int, float, bool)):
            return value
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return value[1:-1]
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except:
                return None
        return None
    
    def evaluate_operation(self, op: str, left, right):
        """Evaluate binary operation on constants"""
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if isinstance(left, int) and isinstance(right, int):
                return left // right
            return left / right
        elif op == '%':
            return left % right
        elif op == '**':
            return left ** right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        else:
            raise ValueError(f"Unknown operator: {op}")


def test_optimizer():
    """Test the optimizer"""
    from lexer import Lexer
    from parser import Parser
    
    test_code = """
    int a = 5 + 3;
    int b = a * 2;
    int c = 10;
    int unused = 99;
    print(b);
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    ir_gen = IRGenerator()
    ir_gen.generate(ast)
    
    print("=== Original Intermediate Code ===")
    print(ir_gen.get_code_string())
    
    optimizer = Optimizer(ir_gen.code)
    optimized_code = optimizer.optimize()
    
    print("\n=== Optimized Intermediate Code ===")
    for instr in optimized_code:
        print(instr)


if __name__ == "__main__":
    test_optimizer()
