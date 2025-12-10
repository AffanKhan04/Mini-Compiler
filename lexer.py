"""
Lexical Analyzer (Tokenizer) for NumCalc Language
Phase 1: Converts source code into tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Token types for NumCalc language"""
    # Keywords
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    PRINT = auto()
    INPUT = auto()
    TRUE = auto()
    FALSE = auto()
    FUNCTION = auto()
    LEN = auto()
    RANDOM = auto()
    SUBSTR = auto()
    CONCAT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    
    # Literals and identifiers
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a single token"""
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    """Lexical analyzer that converts source code into tokens"""
    
    # Keywords mapping
    KEYWORDS = {
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'bool': TokenType.BOOL,
        'string': TokenType.STRING,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'return': TokenType.RETURN,
        'print': TokenType.PRINT,
        'input': TokenType.INPUT,
        'function': TokenType.FUNCTION,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'len': TokenType.LEN,
        'random': TokenType.RANDOM,
        'substr': TokenType.SUBSTR,
        'concat': TokenType.CONCAT,
        'function': TokenType.FUNCTION,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def error(self, message: str):
        """Raise a lexical error"""
        raise SyntaxError(f"Lexical error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Peek at character at current position + offset"""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return current character"""
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.peek() and self.peek() in ' \t\r\n':
            self.advance()
    
    def skip_single_line_comment(self):
        """Skip single-line comment // ..."""
        self.advance()  # /
        self.advance()  # /
        while self.peek() and self.peek() != '\n':
            self.advance()
    
    def skip_multi_line_comment(self):
        """Skip multi-line comment /* ... */"""
        self.advance()  # /
        self.advance()  # *
        while self.peek():
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()  # *
                self.advance()  # /
                return
            self.advance()
        self.error("Unterminated multi-line comment")
    
    def read_number(self) -> Token:
        """Read integer or float literal"""
        start_line = self.line
        start_column = self.column
        num_str = ''
        is_float = False
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if is_float:
                    self.error("Invalid number format: multiple decimal points")
                is_float = True
            num_str += self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT_LITERAL, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INT_LITERAL, int(num_str), start_line, start_column)
    
    def read_string(self) -> Token:
        """Read string literal"""
        start_line = self.line
        start_column = self.column
        self.advance()  # opening "
        string_value = ''
        
        while self.peek() and self.peek() != '"':
            if self.peek() == '\\':
                self.advance()
                next_char = self.peek()
                if next_char == 'n':
                    string_value += '\n'
                    self.advance()
                elif next_char == 't':
                    string_value += '\t'
                    self.advance()
                elif next_char == '\\':
                    string_value += '\\'
                    self.advance()
                elif next_char == '"':
                    string_value += '"'
                    self.advance()
                else:
                    string_value += next_char
                    self.advance()
            else:
                string_value += self.advance()
        
        if not self.peek():
            self.error("Unterminated string literal")
        
        self.advance()  # closing "
        return Token(TokenType.STRING_LITERAL, string_value, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            identifier += self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        # Handle boolean literals
        if token_type == TokenType.TRUE:
            return Token(TokenType.BOOL_LITERAL, True, start_line, start_column)
        elif token_type == TokenType.FALSE:
            return Token(TokenType.BOOL_LITERAL, False, start_line, start_column)
        
        return Token(token_type, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """Convert source code into list of tokens"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            char = self.peek()
            start_line = self.line
            start_column = self.column
            
            # Comments
            if char == '/' and self.peek(1) == '/':
                self.skip_single_line_comment()
                continue
            elif char == '/' and self.peek(1) == '*':
                self.skip_multi_line_comment()
                continue
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char == '"':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))
            
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))
            
            elif char == '*':
                self.advance()
                if self.peek() == '*':
                    self.advance()
                    self.tokens.append(Token(TokenType.POWER, '**', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_column))
            
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_column))
            
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_column))
            
            elif char == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_column))
            
            elif char == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, '!=', start_line, start_column))
                else:
                    self.error(f"Unexpected character: {char}")
            
            elif char == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LE, '<=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.LT, '<', start_line, start_column))
            
            elif char == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GE, '>=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.GT, '>', start_line, start_column))
            
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))
            
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))
            
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_column))
            
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_column))
            
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_column))
            
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_column))
            
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
            
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))
            
            else:
                self.error(f"Unexpected character: {char}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


def test_lexer():
    """Test the lexer with sample code"""
    test_code = """
    // Fibonacci function
    function int fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    int result = 5 ** 2;
    float pi = 3.14;
    bool flag = true;
    string name = "NumCalc";
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    print("=== Lexical Analysis Output ===")
    for token in tokens:
        print(token)


if __name__ == "__main__":
    test_lexer()
