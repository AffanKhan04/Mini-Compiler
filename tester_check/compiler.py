"""
Mini Compiler - Main Entry Point
Complete compiler for Mini mini language
Demonstrates all 6 phases of compilation
"""

import sys
import argparse
from lexer import Lexer, TokenType
from parser import Parser
from semantic_analyzer import SemanticAnalyzer, SemanticError
from ir_generator import IRGenerator
from optimizer import Optimizer
from interpreter import Interpreter


class NumCalcCompiler:
    """Main compiler class that orchestrates all phases"""
    
    def __init__(self, verbose=False, optimize=True):
        self.verbose = verbose
        self.optimize = optimize
    
    def compile_and_run(self, source_code: str, filename="<input>"):
        """Compile and execute source code"""
        try:
            # Phase 1: Lexical Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 1: LEXICAL ANALYSIS")
                print("=" * 60)
            
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            if self.verbose:
                print(f"✓ Generated {len(tokens)} tokens")
                for token in tokens[:10]:  # Show first 10 tokens
                    print(f"  {token}")
                if len(tokens) > 10:
                    print(f"  ... and {len(tokens) - 10} more tokens")
                print()
            
            # Phase 2: Syntax Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 2: SYNTAX ANALYSIS")
                print("=" * 60)
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            if self.verbose:
                print(f"✓ Parse tree created successfully")
                print(f"  Root: {ast}")
                print(f"  Statements: {len(ast.statements)}")
                print()
            
            # Phase 3: Semantic Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 3: SEMANTIC ANALYSIS")
                print("=" * 60)
            
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            
            if self.verbose:
                print("✓ Semantic analysis completed")
                print("\nSymbol Table:")
                print(analyzer.get_symbol_table_string())
                print()
            
            # Phase 4: Intermediate Code Generation
            if self.verbose:
                print("=" * 60)
                print("PHASE 4: INTERMEDIATE CODE GENERATION")
                print("=" * 60)
            
            ir_gen = IRGenerator()
            ir_gen.generate(ast)
            
            if self.verbose:
                print(f"✓ Generated {len(ir_gen.code)} IR instructions")
                print("\nThree-Address Code:")
                for i, instr in enumerate(ir_gen.code):
                    print(f"  {i:3d}: {instr}")
                print()
            
            code = ir_gen.code
            
            # Phase 5: Optimization
            if self.optimize:
                if self.verbose:
                    print("=" * 60)
                    print("PHASE 5: OPTIMIZATION")
                    print("=" * 60)
                
                optimizer = Optimizer(code)
                code = optimizer.optimize()
                
                if self.verbose:
                    print(f"✓ Optimization completed")
                    print(f"  Original instructions: {len(ir_gen.code)}")
                    print(f"  Optimized instructions: {len(code)}")
                    print(f"  Reduction: {len(ir_gen.code) - len(code)} instructions")
                    print("\nOptimized Code:")
                    for i, instr in enumerate(code):
                        print(f"  {i:3d}: {instr}")
                    print()
            
            # Phase 6: Code Generation / Execution
            if self.verbose:
                print("=" * 60)
                print("PHASE 6: CODE EXECUTION")
                print("=" * 60)
            
            interpreter = Interpreter(code)
            interpreter.execute()
            
            if self.verbose:
                print("\n✓ Execution completed successfully")
            else:
                print()  # Newline after output
            
            return True
            
        except SyntaxError as e:
            print(f"\n❌ Syntax Error in {filename}:")
            print(f"  {e}")
            return False
        
        except SemanticError as e:
            print(f"\n❌ Semantic Error in {filename}:")
            print(f"  {e}")
            return False
        
        except Exception as e:
            print(f"\n❌ Runtime Error in {filename}:")
            print(f"  {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def compile_file(self, filename: str):
        """Compile and execute a file"""
        try:
            with open(filename, 'r') as f:
                source_code = f.read()
            
            print(f"Compiling {filename}...")
            print()
            return self.compile_and_run(source_code, filename)
        
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return False
        except IOError as e:
            print(f"❌ Error reading file: {e}")
            return False


def main():
    """Main entry point for the compiler"""
    parser = argparse.ArgumentParser(
        description='Mini Compiler - A mini language compiler with 6 compilation phases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compiler.py program.nc              # Compile and run a file
  python compiler.py program.nc -v           # Verbose mode (show all phases)
  python compiler.py program.nc --no-opt     # Disable optimizations
  python compiler.py -i                      # Interactive mode

About Mini Compiler:
  Mini Compiler is a domain-specific language for numerical computations.
  It supports variables, functions, loops, and mathematical operations.
        """
    )
    
    parser.add_argument('file', nargs='?', help='Source file to compile (.nc)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show all compilation phases')
    parser.add_argument('--no-opt', action='store_true',
                       help='Disable optimizations')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode (REPL)')
    
    args = parser.parse_args()
    
    compiler = NumCalcCompiler(verbose=args.verbose, optimize=not args.no_opt)
    
    # Interactive mode
    if args.interactive:
        print("Mini compiler Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                code_lines = []
                print("\nEnter code (empty line to execute):")
                while True:
                    line = input(">>> " if not code_lines else "... ")
                    if line.strip().lower() in ['exit', 'quit']:
                        print("Goodbye!")
                        return
                    if not line.strip() and code_lines:
                        break
                    if line.strip():
                        code_lines.append(line)
                
                if code_lines:
                    code = '\n'.join(code_lines)
                    compiler.compile_and_run(code, "<interactive>")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    # File mode
    elif args.file:
        success = compiler.compile_file(args.file)
        sys.exit(0 if success else 1)
    
    # No arguments - show help
    else:
        parser.print_help()
        print("\nNo input file specified. Use -i for interactive mode.")
        sys.exit(1)


if __name__ == "__main__":
    main()
