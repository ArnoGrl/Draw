import tkinter as tk
from tkinter import filedialog, messagebox
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from test import Test

class DrawPlusIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw++ IDE")
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.setup_menu()
        self.file_path = None

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
      if not code:
          messagebox.showwarning("Warning", "No code to run!")
          return
      try:
          # Initialisation du Lexer avec le code source
          lexer = Lexer(source_code=code)
        
          # Génération des tokens
          tokens = lexer.tokenize()
        
          # Initialisation du Parser avec les tokens
          parser = Parser(tokens=tokens)
        
          # Analyse syntaxique pour générer l'AST
          ast = parser.parse()
        
          # Exécution de l'AST
          interpreter = Interpreter()
          interpreter.execute(ast)

          test = Test()
          test.execute(ast)
        
          messagebox.showinfo("Success", "Code executed successfully!")
      except Exception as e:
          messagebox.showerror("Error", f"An error occurred: {e}")
   
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
