"""
NumCalc Compiler - Graphical User Interface
A simple GUI for the NumCalc compiler with editor, output, and IR viewer
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from interpreter import Interpreter


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NumCalc Compiler")
        self.root.geometry("1200x800")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main container
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Title and toolbar
        self.create_toolbar(main_container)
        
        # Create paned window for editor and output
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Editor
        self.create_editor_panel(paned)
        
        # Right panel - Output and IR
        self.create_output_panel(paned)
        
        # Status bar
        self.create_status_bar(main_container)
        
        # Load example code
        self.load_example()
    
    def create_toolbar(self, parent):
        """Create toolbar with buttons"""
        toolbar = ttk.Frame(parent)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Title
        title = ttk.Label(toolbar, text="NumCalc Compiler", font=("Arial", 16, "bold"))
        title.pack(side=tk.LEFT, padx=10)
        
        # Buttons
        ttk.Button(toolbar, text="▶ Compile & Run", command=self.compile_and_run, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📁 Open", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="💾 Save", command=self.save_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑 Clear", command=self.clear_editor).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📝 Examples", command=self.show_examples).pack(side=tk.LEFT, padx=5)
        
        # Optimization checkbox
        self.optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Optimize", variable=self.optimize_var).pack(side=tk.LEFT, padx=10)
        
        # Verbose checkbox
        self.verbose_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar, text="Verbose", variable=self.verbose_var).pack(side=tk.LEFT, padx=5)
    
    def create_editor_panel(self, parent):
        """Create editor panel"""
        editor_frame = ttk.Frame(parent)
        parent.add(editor_frame, weight=1)
        
        # Editor label
        ttk.Label(editor_frame, text="Source Code", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Editor with line numbers
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_container, width=4, padx=5, takefocus=0, border=0,
                                     background='#f0f0f0', state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor
        self.editor = scrolledtext.ScrolledText(editor_container, wrap=tk.NONE, font=("Consolas", 11),
                                                 undo=True, maxundo=-1)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Syntax highlighting
        self.editor.tag_configure("keyword", foreground="#0000FF")
        self.editor.tag_configure("comment", foreground="#008000")
        self.editor.tag_configure("string", foreground="#A31515")
        self.editor.tag_configure("number", foreground="#098658")
        
        # Bind events
        self.editor.bind('<KeyRelease>', self.update_line_numbers)
        self.editor.bind('<KeyRelease>', self.apply_syntax_highlighting, add='+')
    
    def create_output_panel(self, parent):
        """Create output and IR panel"""
        output_frame = ttk.Frame(parent)
        parent.add(output_frame, weight=1)
        
        # Notebook for tabs
        notebook = ttk.Notebook(output_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Output tab
        output_tab = ttk.Frame(notebook)
        notebook.add(output_tab, text="Program Output")
        
        ttk.Label(output_tab, text="Execution Output", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 5))
        self.output = scrolledtext.ScrolledText(output_tab, wrap=tk.WORD, font=("Consolas", 10),
                                                 height=10, state='disabled', background='#f8f8f8')
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # IR tab
        ir_tab = ttk.Frame(notebook)
        notebook.add(ir_tab, text="Intermediate Code")
        
        ttk.Label(ir_tab, text="Three-Address Code (IR)", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 5))
        self.ir_view = scrolledtext.ScrolledText(ir_tab, wrap=tk.NONE, font=("Consolas", 10),
                                                  state='disabled', background='#f8f8f8')
        self.ir_view.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Console tab
        console_tab = ttk.Frame(notebook)
        notebook.add(console_tab, text="Console")
        
        ttk.Label(console_tab, text="Compiler Messages", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 5))
        self.console = scrolledtext.ScrolledText(console_tab, wrap=tk.WORD, font=("Consolas", 9),
                                                  state='disabled', background='#1e1e1e', foreground='#d4d4d4')
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_bar = ttk.Label(parent, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def update_line_numbers(self, event=None):
        """Update line numbers"""
        lines = self.editor.get('1.0', tk.END).count('\n')
        line_numbers_string = "\n".join(str(i) for i in range(1, lines))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    def apply_syntax_highlighting(self, event=None):
        """Simple syntax highlighting"""
        # Clear existing tags
        self.editor.tag_remove("keyword", "1.0", tk.END)
        self.editor.tag_remove("comment", "1.0", tk.END)
        self.editor.tag_remove("string", "1.0", tk.END)
        self.editor.tag_remove("number", "1.0", tk.END)
        
        # Keywords
        keywords = ['int', 'float', 'bool', 'string', 'function', 'return', 'if', 'else', 
                   'while', 'print', 'true', 'false']
        
        content = self.editor.get('1.0', tk.END)
        for keyword in keywords:
            start = '1.0'
            while True:
                pos = self.editor.search(f'\\m{keyword}\\M', start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.editor.tag_add("keyword", pos, end)
                start = end
        
        # Comments
        start = '1.0'
        while True:
            pos = self.editor.search('//', start, tk.END)
            if not pos:
                break
            end = f"{pos} lineend"
            self.editor.tag_add("comment", pos, end)
            start = f"{pos}+1line"
    
    def compile_and_run(self):
        """Compile and run the code"""
        source_code = self.editor.get('1.0', tk.END)
        
        # Clear outputs
        self.clear_output()
        self.append_console("Compiling...\n", "info")
        self.status_bar.config(text="Compiling...")
        self.root.update()
        
        try:
            # Phase 1: Lexical Analysis
            lexer = Lexer(source_code)
            tokens = list(lexer.tokenize())
            if self.verbose_var.get():
                self.append_console(f"✓ Lexical analysis: {len(tokens)} tokens\n", "success")
            
            # Phase 2: Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            if self.verbose_var.get():
                self.append_console("✓ Parsing complete\n", "success")
            
            # Phase 3: Semantic Analysis
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            if self.verbose_var.get():
                self.append_console("✓ Semantic analysis complete\n", "success")
            
            # Phase 4: IR Generation
            ir_gen = IRGenerator()
            ir_gen.generate(ast)
            if self.verbose_var.get():
                self.append_console(f"✓ IR generation: {len(ir_gen.code)} instructions\n", "success")
            
            # Display IR
            self.display_ir(ir_gen.code)
            
            code = ir_gen.code
            
            # Phase 5: Optimization
            if self.optimize_var.get():
                optimizer = Optimizer(code)
                code = optimizer.optimize()
                if self.verbose_var.get():
                    self.append_console(f"✓ Optimization: {len(ir_gen.code)} → {len(code)} instructions\n", "success")
            
            # Phase 6: Execution
            interpreter = Interpreter(code)
            
            # Capture output
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                interpreter.execute()
            
            # Display output
            output_text = output_buffer.getvalue()
            if output_text:
                self.append_output(output_text)
            else:
                self.append_output("(No output)")
            
            self.append_console("\n✓ Compilation and execution successful!\n", "success")
            self.status_bar.config(text="Compilation successful")
            
        except SyntaxError as e:
            self.append_console(f"\n❌ Syntax Error: {e}\n", "error")
            self.status_bar.config(text="Syntax Error")
            messagebox.showerror("Syntax Error", str(e))
            
        except RuntimeError as e:
            self.append_console(f"\n❌ Runtime Error: {e}\n", "error")
            self.status_bar.config(text="Runtime Error")
            messagebox.showerror("Runtime Error", str(e))
            
        except Exception as e:
            self.append_console(f"\n❌ Error: {e}\n", "error")
            self.status_bar.config(text="Error")
            messagebox.showerror("Error", str(e))
    
    def display_ir(self, code):
        """Display IR code"""
        self.ir_view.config(state='normal')
        self.ir_view.delete('1.0', tk.END)
        for i, instr in enumerate(code):
            self.ir_view.insert(tk.END, f"{i:3d}: {instr}\n")
        self.ir_view.config(state='disabled')
    
    def append_output(self, text):
        """Append text to output"""
        self.output.config(state='normal')
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state='disabled')
    
    def append_console(self, text, style="normal"):
        """Append text to console"""
        self.console.config(state='normal')
        
        # Configure tags for different styles
        self.console.tag_configure("error", foreground="#f48771")
        self.console.tag_configure("success", foreground="#73c991")
        self.console.tag_configure("info", foreground="#89d8ff")
        
        if style != "normal":
            self.console.insert(tk.END, text, style)
        else:
            self.console.insert(tk.END, text)
        
        self.console.see(tk.END)
        self.console.config(state='disabled')
    
    def clear_output(self):
        """Clear all output windows"""
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.config(state='disabled')
        
        self.console.config(state='normal')
        self.console.delete('1.0', tk.END)
        self.console.config(state='disabled')
        
        self.ir_view.config(state='normal')
        self.ir_view.delete('1.0', tk.END)
        self.ir_view.config(state='disabled')
    
    def clear_editor(self):
        """Clear editor"""
        if messagebox.askyesno("Clear Editor", "Are you sure you want to clear the editor?"):
            self.editor.delete('1.0', tk.END)
            self.update_line_numbers()
    
    def open_file(self):
        """Open a file"""
        filename = filedialog.askopenfilename(
            title="Open NumCalc File",
            filetypes=[("NumCalc Files", "*.nc"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.editor.delete('1.0', tk.END)
                self.editor.insert('1.0', content)
                self.update_line_numbers()
                self.apply_syntax_highlighting()
                self.status_bar.config(text=f"Opened: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self):
        """Save file"""
        filename = filedialog.asksaveasfilename(
            title="Save NumCalc File",
            defaultextension=".nc",
            filetypes=[("NumCalc Files", "*.nc"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    content = self.editor.get('1.0', tk.END)
                    f.write(content)
                self.status_bar.config(text=f"Saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def show_examples(self):
        """Show examples menu"""
        examples_window = tk.Toplevel(self.root)
        examples_window.title("Example Programs")
        examples_window.geometry("400x500")
        
        ttk.Label(examples_window, text="Select an Example", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # List of examples
        examples_dir = Path("examples")
        if examples_dir.exists():
            listbox = tk.Listbox(examples_window, font=("Consolas", 10))
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for file in sorted(examples_dir.glob("*.nc")):
                listbox.insert(tk.END, file.name)
            
            def load_selected():
                selection = listbox.curselection()
                if selection:
                    filename = listbox.get(selection[0])
                    filepath = examples_dir / filename
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                        self.editor.delete('1.0', tk.END)
                        self.editor.insert('1.0', content)
                        self.update_line_numbers()
                        self.apply_syntax_highlighting()
                        self.status_bar.config(text=f"Loaded: {filename}")
                        examples_window.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not load example: {e}")
            
            ttk.Button(examples_window, text="Load", command=load_selected).pack(pady=10)
        else:
            ttk.Label(examples_window, text="No examples directory found").pack(pady=20)
    
    def load_example(self):
        """Load default example"""
        example_code = """// Factorial Calculator
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("Factorial Examples:");
int i = 1;
while (i <= 5) {
    int result = factorial(i);
    print(i, "! =", result);
    i = i + 1;
}
"""
        self.editor.insert('1.0', example_code)
        self.update_line_numbers()
        self.apply_syntax_highlighting()


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
