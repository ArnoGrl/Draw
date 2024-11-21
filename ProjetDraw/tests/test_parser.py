# tests/test_parser.py
import unittest
from lexer import Lexer
from parser import Parser

class TestParser(unittest.TestCase):
    
    def parse_code(self, code):
        """Helper function to parse code and return the syntax tree."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_cursor_declaration(self):
        """Test if a simple cursor declaration is parsed correctly."""
        code = "cursor myCursor;"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "CURSOR_DECLARATION")
        self.assertEqual(syntax_tree[0]["name"], "myCursor")

    def test_set_position(self):
        """Test if setting the position of a cursor is parsed correctly."""
        code = "myCursor.setPosition(100, 200);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "SET_POSITION")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["x"], "100")
        self.assertEqual(syntax_tree[0]["y"], "200")

    def test_draw_line(self):
        """Test if drawLine instruction is parsed correctly."""
        code = "myCursor.drawLine(50);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "DRAW_LINE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["length"], "50")

    
    def test_invalid_syntax(self):
        """Test if the parser detects invalid syntax."""
        code = "cursor myCursor setPosition(100, 200);"  # Missing semicolon
        with self.assertRaises(SyntaxError):
            self.parse_code(code)

if __name__ == "__main__":
    unittest.main()
