import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import filedialog, messagebox
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
import compiler


class DrawPlusIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw++ IDE")

        # Zone principale pour le code
        self.text_area = tk.Text(self.root, wrap="word", undo=True, height=20)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Zone dédiée pour les erreurs
        self.error_area = tk.Text(self.root, wrap="word", height=10, bg="lightgray", fg="red", state="disabled")
        self.error_area.pack(fill="both", expand=False, padx=5, pady=5)

        self.setup_menu()
        self.file_path = None

    def clear_error_area(self):
        self.error_area.config(state="normal")
        self.error_area.delete(1.0, tk.END)
        self.error_area.config(state="disabled")

    def display_error(self, message):
        self.error_area.config(state="normal")
        self.error_area.insert(tk.END, message + "\n")
        self.error_area.config(state="disabled")

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menu, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menu.add_cascade(label="Run", menu=run_menu)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Draw++ Files", "*.draw++"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".draw++",
                                                          filetypes=[("Draw++ Files", "*.draw++"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
       
    def run_code(self):
        code = self.text_area.get(1.0, tk.END).strip()
        self.clear_error_area()

        if not code:
            self.display_error("Warning: No code to run!")
            return

        try:
            # Lexer : Générer les tokens
            lexer = Lexer(source_code=code)
            tokens = lexer.tokenize()

            # Parser : Générer l'AST
            parser = Parser(tokens=tokens)
            ast = parser.parse()

            # Vérifiez les erreurs du parser
            if parser.errors:
                for error in parser.errors:
                    # Filtrer les messages qui contiennent "Unexpected token"
                    if "Unexpected token" not in error:
                        self.display_error(f"{error}")
                return  # Ne pas continuer si des erreurs de parsing sont présentes
            # Interpreter : Exécuter l'AST
            interpreter = Interpreter(syntax_tree=ast)
            interpreter.execute()

            # Vérifiez les erreurs de l'interpreter
            if interpreter.errors:
                for error in interpreter.errors:
                    self.display_error(f"{error}")
            else:
                messagebox.showinfo("Success", "Code executed successfully!")

                 # 4) Compilation du code C
                c_code = compiler.generate_c_code(ast)  # Génération du C
                compiler.save_to_file("output.c", c_code)
                compiler.compile_c_to_exe("output.c", "output.exe")

                # 5) (Optionnel) Exécuter l’exécutable
                import subprocess
                subprocess.Popen(["./output.exe"])  # Sur Windows, simplement "output.exe" fonctionne

        except Exception as e:
            # Si une erreur inattendue survient
            self.display_error(f"An unexpected error occurred: {e}")

  
    def validate_code(self):
     code = self.text_area.get(1.0, tk.END).strip()
     if not code:
         messagebox.showwarning("Warning", "No code to validate!")
         return

     try:
         # Initialisation du Lexer et génération des tokens
         lexer = Lexer(source_code=code)
         tokens = lexer.tokenize()

         # Initialisation du Parser et analyse syntaxique
         parser = Parser(tokens=tokens)
         parser.parse()

         messagebox.showinfo("Validation", "No errors detected!")
     except Exception as e:
         # Gestion et affichage des erreurs
         messagebox.showerror("Validation Error", f"An error occurred: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    ide = DrawPlusIDE(root)
    root.mainloop()
