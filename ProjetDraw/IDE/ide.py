import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to the Python path

import tkinter as tk
from tkinter import filedialog, messagebox
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
import compiler


class DrawPlusIDE:
    """
    Implements the main interface for the Draw++ IDE.
    - Provides a text area for code input.
    - Displays errors in a separate, dedicated area.
    - Includes functionality for file handling and menu setup.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Draw++ IDE")  # Set the window title

        # Main text area for writing code
        self.text_area = tk.Text(self.root, wrap="word", undo=True, height=20)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Dedicated error display area
        self.error_area = tk.Text(self.root, wrap="word", height=10, bg="lightgray", fg="red", state="disabled")
        self.error_area.pack(fill="both", expand=False, padx=5, pady=5)

        self.setup_menu()  # Initialize the menu
        self.file_path = None  # Current file path (if a file is open)

    def clear_error_area(self):
        """
        Clears the content of the error area.
        """
        self.error_area.config(state="normal")  # Enable editing in the error area
        self.error_area.delete(1.0, tk.END)  # Delete all content
        self.error_area.config(state="disabled")  # Disable editing again

    def display_error(self, message):
        """
        Displays an error message in the error area.
        - Appends the provided message to the error area.
        """
        self.error_area.config(state="normal")  # Enable editing
        self.error_area.insert(tk.END, message + "\n")  # Add the error message
        self.error_area.config(state="disabled")  # Disable editing

    def setup_menu(self):
        """
        Configures the application's menu bar.
        - Adds a "File" menu for file operations (New, Open, Save).
        - Adds a "Run" menu for executing code.
        """
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # File menu for creating, opening, and saving files
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu.add_cascade(label="File", menu=file_menu)

        # Run menu for executing the code
        run_menu = tk.Menu(menu, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menu.add_cascade(label="Run", menu=run_menu)

    def new_file(self):
        """
        Clears the text area and resets the file path.
        """
        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.file_path = None  # Reset the file path

    def open_file(self):
        """
        Opens a file dialog to select and load a file.
        - Reads the content of the selected file into the text area.
        """
        self.file_path = filedialog.askopenfilename(filetypes=[("Draw++ Files", "*.draw++"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)  # Clear current text
                self.text_area.insert(1.0, file.read())  # Load file content

    def save_file(self):
        """
        Saves the content of the text area to a file.
        - Prompts for a file name if none is specified.
        """
        if not self.file_path:
            # Open a save dialog if no file path is set
            self.file_path = filedialog.asksaveasfilename(defaultextension=".draw++",
                                                        filetypes=[("Draw++ Files", "*.draw++"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))  # Save the text area content
       

    def run_code(self):
        """
        Executes the code written in the text area.
        - Performs lexical analysis to generate tokens.
        - Parses tokens into an Abstract Syntax Tree (AST).
        - Interprets the AST and executes the logic.
        - Compiles the code into a C program and optionally runs it.
        """
        code = self.text_area.get(1.0, tk.END).strip()
        self.clear_error_area()

        if not code:
            self.display_error("Warning: No code to run!")
            return

        try:
            # Lexical analysis to generate tokens
            lexer = Lexer(source_code=code)
            tokens = lexer.tokenize()

            # Syntax analysis to generate the AST
            parser = Parser(tokens=tokens)
            ast = parser.parse()

            # Check for parsing errors
            if parser.errors:
                for error in parser.errors:
                    if "Unexpected token" not in error:  # Filter specific error messages
                        self.display_error(f"{error}")
                return

            # Interpretation: execute the AST
            interpreter = Interpreter(syntax_tree=ast)
            interpreter.execute()

            # Check for interpretation errors
            if interpreter.errors:
                for error in interpreter.errors:
                    self.display_error(f"{error}")
            else:
                messagebox.showinfo("Success", "Code executed successfully!")

                # Compile the C code
                c_code = compiler.generate_c_code(ast)  # Generate C code
                compiler.save_to_file("output.c", c_code)  # Save to a file
                compiler.compile_c_to_exe("output.c", "output.exe")  # Compile to an executable

                # Optionally run the compiled executable
                import subprocess
                subprocess.Popen(["./output.exe"])  # For Windows, just "output.exe" works

        except Exception as e:
            # Handle unexpected errors
            self.display_error(f"An unexpected error occurred: {e}")


    def validate_code(self):
        """
        Validates the code in the text area for syntax errors.
        - Performs lexical and syntax analysis without execution.
        """
        code = self.text_area.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "No code to validate!")
            return

        try:
            # Lexical analysis to generate tokens
            lexer = Lexer(source_code=code)
            tokens = lexer.tokenize()

            # Syntax analysis to validate the code
            parser = Parser(tokens=tokens)
            parser.parse()

            messagebox.showinfo("Validation", "No errors detected!")
        except Exception as e:
            # Handle and display errors
            messagebox.showerror("Validation Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    ide = DrawPlusIDE(root)
    root.mainloop()