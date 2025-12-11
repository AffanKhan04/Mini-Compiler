"""
Parser (Syntax Analyzer) for Mini Compiler Language
Phase 2: Converts tokens into Abstract Syntax Tree (AST)
Uses recursive descent parsing
"""

from lexer import Token, TokenType, Lexer
from typing import List, Optional, Any
from dataclasses import dataclass


# ============= AST Node Definitions =============

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int
    column: int


@dataclass
class Program(ASTNode):
    """Root node of the program"""
    statements: List[ASTNode]


@dataclass
class BinaryOp(ASTNode):
    """Binary operation (e.g., a + b)"""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """Unary operation (e.g., -a, not b)"""
    operator: str
    operand: ASTNode


@dataclass
class Literal(ASTNode):
    """Literal value (int, float, string, bool)"""
    value: Any
    type: str  # 'int', 'float', 'string', 'bool'


@dataclass
class Identifier(ASTNode):
    """Variable or function identifier"""
    name: str


@dataclass
class VarDeclaration(ASTNode):
    """Variable declaration"""
    var_type: str  # 'int', 'float', 'bool', 'string'
    name: str
    initializer: Optional[ASTNode]


@dataclass
class Assignment(ASTNode):
    """Variable assignment"""
    name: str
    value: ASTNode


@dataclass
class IfStatement(ASTNode):
    """If-else statement"""
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]]


@dataclass
class WhileStatement(ASTNode):
    """While loop"""
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class ForStatement(ASTNode):
    """For loop"""
    init: ASTNode
    condition: ASTNode
    update: ASTNode
    body: List[ASTNode]


@dataclass
class FunctionDef(ASTNode):
    """Function definition"""
    return_type: str
    name: str
    parameters: List[tuple]  # [(type, name), ...]
    body: List[ASTNode]


@dataclass
class FunctionCall(ASTNode):
    """Function call"""
    name: str
    arguments: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    """Return statement"""
    value: Optional[ASTNode]


@dataclass
class PrintStatement(ASTNode):
    """Print statement"""
    expressions: List[ASTNode]


@dataclass
class Block(ASTNode):
    """Block of statements"""
    statements: List[ASTNode]


@dataclass
class ArrayLiteral(ASTNode):
    """Array literal [1, 2, 3]"""
    elements: List[ASTNode]


@dataclass
class ArrayAccess(ASTNode):
    """Array element access arr[index]"""
    array: ASTNode
    index: ASTNode


@dataclass
class ArrayAssignment(ASTNode):
    """Array element assignment arr[index] = value"""
    array: str
    index: ASTNode
    value: ASTNode


@dataclass
class BuiltInCall(ASTNode):
    """Built-in function call (len, random, substr, concat, input)"""
    function: str
    arguments: List[ASTNode]


# ============= Parser Implementation =============

class Parser:
    """Recursive descent parser for NumCalc language"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise a syntax error"""
        if self.current_token:
            raise SyntaxError(
                f"Syntax error at line {self.current_token.line}, "
                f"column {self.current_token.column}: {message}"
            )
        raise SyntaxError(f"Syntax error: {message}")
    
    def peek(self) -> Token:
        """Get current token without consuming"""
        return self.current_token
    
    def advance(self) -> Token:
        """Consume current token and move to next"""
        token = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume token of expected type or raise error"""
        if self.current_token.type != token_type:
            self.error(f"Expected {token_type.name}, got {self.current_token.type.name}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token.type in token_types
    
    # ============= Parsing Methods =============
    
    def parse(self) -> Program:
        """Parse the entire program"""
        statements = []
        while not self.match(TokenType.EOF):
            statements.append(self.parse_statement())
        return Program(1, 1, statements)
    
    def parse_statement(self) -> ASTNode:
        """Parse a single statement"""
        # Variable declaration
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING):
            return self.parse_declaration()
        
        # Function definition
        elif self.match(TokenType.FUNCTION):
            return self.parse_function_def()
        
        # If statement
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        
        # While loop
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        
        # For loop
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        
        # Return statement
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        
        # Print statement
        elif self.match(TokenType.PRINT):
            return self.parse_print_statement()
        
        # Assignment or expression statement
        elif self.match(TokenType.IDENTIFIER):
            # Look ahead to determine if it's assignment or array assignment
            next_token_type = self.tokens[self.pos + 1].type if self.pos + 1 < len(self.tokens) else None
            
            if next_token_type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif next_token_type == TokenType.LBRACKET:
                # Could be array access or array assignment
                # Need to check further ahead
                # For now, parse as assignment which handles both cases
                return self.parse_assignment()
            else:
                # Expression statement (e.g., function call)
                expr = self.parse_expression()
                self.expect(TokenType.SEMICOLON)
                return expr
        
        else:
            self.error(f"Unexpected token: {self.current_token.type.name}")
    
    def parse_declaration(self) -> VarDeclaration:
        """Parse variable declaration"""
        var_type_token = self.advance()
        var_type = var_type_token.value if var_type_token.type == TokenType.IDENTIFIER else var_type_token.type.name.lower()
        
        # Check for array declaration (int[], float[], etc.)
        if self.match(TokenType.LBRACKET):
            self.advance()
            self.expect(TokenType.RBRACKET)
            var_type = var_type + "[]"  # Mark as array type
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        return VarDeclaration(name_token.line, name_token.column, var_type, name, initializer)
    
    def parse_assignment(self) -> Assignment:
        """Parse variable assignment or array element assignment"""
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Check for array element assignment: arr[index] = value
        if self.match(TokenType.LBRACKET):
            self.advance()
            index = self.parse_expression()
            self.expect(TokenType.RBRACKET)
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            return ArrayAssignment(name_token.line, name_token.column, name, index, value)
        
        # Regular variable assignment
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name_token.line, name_token.column, name, value)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if-else statement"""
        if_token = self.advance()
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        then_block = self.parse_block()
        
        else_block = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_block = self.parse_block()
        
        return IfStatement(if_token.line, if_token.column, condition, then_block, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse while loop"""
        while_token = self.advance()
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(while_token.line, while_token.column, condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        """Parse for loop"""
        for_token = self.advance()
        self.expect(TokenType.LPAREN)
        
        # Initialization - can be declaration or assignment
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING):
            # Variable declaration: int i = 0;
            var_type_token = self.advance()
            var_type = var_type_token.type.name.lower()
            
            # Check for array declaration
            if self.match(TokenType.LBRACKET):
                self.advance()
                self.expect(TokenType.RBRACKET)
                var_type = var_type + "[]"
            
            init_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.ASSIGN)
            init_value = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            init = VarDeclaration(for_token.line, for_token.column, var_type, init_name, init_value)
        else:
            # Assignment: i = 0;
            init_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.ASSIGN)
            init_value = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            init = Assignment(for_token.line, for_token.column, init_name, init_value)
        
        # Condition
        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        # Update (must be assignment)
        update_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        update_value = self.parse_expression()
        update = Assignment(for_token.line, for_token.column, update_name, update_value)
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        
        return ForStatement(for_token.line, for_token.column, init, condition, update, body)
    
    def parse_function_def(self) -> FunctionDef:
        """Parse function definition"""
        func_token = self.advance()
        
        # Return type
        return_type_token = self.advance()
        if return_type_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING]:
            return_type = return_type_token.type.name.lower()
        else:
            self.error(f"Expected type specifier, got {return_type_token.type.name}")
        
        # Function name
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Parameters
        self.expect(TokenType.LPAREN)
        parameters = []
        if not self.match(TokenType.RPAREN):
            parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN)
        
        # Body
        body = self.parse_block()
        
        return FunctionDef(func_token.line, func_token.column, return_type, name, parameters, body)
    
    def parse_parameter_list(self) -> List[tuple]:
        """Parse function parameter list"""
        parameters = []
        
        # First parameter
        param_type_token = self.advance()
        if param_type_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING]:
            param_type = param_type_token.type.name.lower()
        else:
            self.error(f"Expected type specifier, got {param_type_token.type.name}")
        param_name = self.expect(TokenType.IDENTIFIER).value
        parameters.append((param_type, param_name))
        
        # Additional parameters
        while self.match(TokenType.COMMA):
            self.advance()
            param_type_token = self.advance()
            if param_type_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING]:
                param_type = param_type_token.type.name.lower()
            else:
                self.error(f"Expected type specifier, got {param_type_token.type.name}")
            param_name = self.expect(TokenType.IDENTIFIER).value
            parameters.append((param_type, param_name))
        
        return parameters
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statement"""
        return_token = self.advance()
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(return_token.line, return_token.column, value)
    
    def parse_print_statement(self) -> PrintStatement:
        """Parse print statement"""
        print_token = self.advance()
        self.expect(TokenType.LPAREN)
        
        expressions = []
        if not self.match(TokenType.RPAREN):
            expressions.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                expressions.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(print_token.line, print_token.column, expressions)
    
    def parse_block(self) -> List[ASTNode]:
        """Parse block of statements"""
        self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE):
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return statements
    
    # ============= Expression Parsing =============
    
    def parse_expression(self) -> ASTNode:
        """Parse expression (logical OR level)"""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        """Parse logical OR expression"""
        left = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(op_token.line, op_token.column, left, 'or', right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND expression"""
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.parse_equality()
            left = BinaryOp(op_token.line, op_token.column, left, 'and', right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        """Parse equality expression (==, !=)"""
        left = self.parse_relational()
        
        while self.match(TokenType.EQ, TokenType.NE):
            op_token = self.advance()
            op = '==' if op_token.type == TokenType.EQ else '!='
            right = self.parse_relational()
            left = BinaryOp(op_token.line, op_token.column, left, op, right)
        
        return left
    
    def parse_relational(self) -> ASTNode:
        """Parse relational expression (<, >, <=, >=)"""
        left = self.parse_additive()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op_token = self.advance()
            op_map = {
                TokenType.LT: '<',
                TokenType.GT: '>',
                TokenType.LE: '<=',
                TokenType.GE: '>='
            }
            op = op_map[op_token.type]
            right = self.parse_additive()
            left = BinaryOp(op_token.line, op_token.column, left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expression (+, -)"""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = '+' if op_token.type == TokenType.PLUS else '-'
            right = self.parse_multiplicative()
            left = BinaryOp(op_token.line, op_token.column, left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expression (*, /, %)"""
        left = self.parse_power()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.advance()
            op_map = {
                TokenType.MULTIPLY: '*',
                TokenType.DIVIDE: '/',
                TokenType.MODULO: '%'
            }
            op = op_map[op_token.type]
            right = self.parse_power()
            left = BinaryOp(op_token.line, op_token.column, left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parse power expression (**)"""
        left = self.parse_unary()
        
        if self.match(TokenType.POWER):
            op_token = self.advance()
            right = self.parse_power()  # Right associative
            left = BinaryOp(op_token.line, op_token.column, left, '**', right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression (-, not)"""
        if self.match(TokenType.MINUS, TokenType.NOT):
            op_token = self.advance()
            op = '-' if op_token.type == TokenType.MINUS else 'not'
            operand = self.parse_unary()
            return UnaryOp(op_token.line, op_token.column, op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expression"""
        token = self.current_token
        
        # Literals
        if self.match(TokenType.INT_LITERAL):
            self.advance()
            return Literal(token.line, token.column, token.value, 'int')
        
        elif self.match(TokenType.FLOAT_LITERAL):
            self.advance()
            return Literal(token.line, token.column, token.value, 'float')
        
        elif self.match(TokenType.STRING_LITERAL):
            self.advance()
            return Literal(token.line, token.column, token.value, 'string')
        
        elif self.match(TokenType.BOOL_LITERAL):
            self.advance()
            return Literal(token.line, token.column, token.value, 'bool')
        
        # Array literal [1, 2, 3]
        elif self.match(TokenType.LBRACKET):
            return self.parse_array_literal()
        
        # Built-in functions or identifiers
        elif self.match(TokenType.LEN, TokenType.RANDOM, TokenType.SUBSTR, TokenType.CONCAT, TokenType.INPUT):
            func_name = token.value
            self.advance()
            self.expect(TokenType.LPAREN)
            arguments = []
            if not self.match(TokenType.RPAREN):
                arguments.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            return BuiltInCall(token.line, token.column, func_name, arguments)
        
        # Identifier or function call
        elif self.match(TokenType.IDENTIFIER):
            name = token.value
            self.advance()
            
            # Array access arr[index]
            if self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return ArrayAccess(token.line, token.column, Identifier(token.line, token.column, name), index)
            
            # Function call
            elif self.match(TokenType.LPAREN):
                self.advance()
                arguments = []
                if not self.match(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        self.advance()
                        arguments.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return FunctionCall(token.line, token.column, name, arguments)
            
            # Variable reference
            else:
                return Identifier(token.line, token.column, name)
        
        # Parenthesized expression
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {token.type.name}")
    
    def parse_array_literal(self) -> ArrayLiteral:
        """Parse array literal [1, 2, 3]"""
        bracket_token = self.expect(TokenType.LBRACKET)
        elements = []
        
        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                elements.append(self.parse_expression())
        
        self.expect(TokenType.RBRACKET)
        return ArrayLiteral(bracket_token.line, bracket_token.column, elements)


def test_parser():
    """Test the parser with sample code"""
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
    
    print("=== Syntax Analysis (AST) Output ===")
    print(ast)


if __name__ == "__main__":
    test_parser()
