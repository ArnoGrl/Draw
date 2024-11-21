# tests/test_compiler.py
import unittest
from compiler import Compiler

class TestCompiler(unittest.TestCase):
    def test_compile_to_c(self):
        syntax_tree = [...]  # Exemple d'arbre syntaxique
        compiler = Compiler(syntax_tree)
        c_code = compiler.compile_to_c()
        self.assertIn("int main()", c_code)

if __name__ == "__main__":
    unittest.main()
