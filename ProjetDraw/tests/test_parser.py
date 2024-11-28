import unittest
from lexer import Lexer
from parser import Parser
from utils.tokens import TokenType


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
        self.assertEqual(syntax_tree[0]["x"], {"type": "VALUE", "value": "100"})
        self.assertEqual(syntax_tree[0]["y"], {"type": "VALUE", "value": "200"})

    def test_draw_line(self):
        """Test if drawing a line is parsed correctly."""
        code = "myCursor.drawLine(100);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "DRAW_LINE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["length"], {"type": "VALUE", "value": "100"})

    def test_move(self):
        """Test if moving the cursor is parsed correctly."""
        code = "myCursor.move(50);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "MOVE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["distance"], {"type": "VALUE", "value": "50"})

    def test_rotate(self):
        """Test if rotating the cursor is parsed correctly."""
        code = "myCursor.rotate(90);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "ROTATE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["angle"], {"type": "VALUE", "value": "90"})

    def test_set_thickness(self):
        """Test if setting the thickness of a cursor is parsed correctly."""
        code = "myCursor.setThickness(5);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "SET_THICKNESS")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["thickness"], {"type": "VALUE", "value": "5"})

    def test_draw_square(self):
        """Test if drawing a square is parsed correctly."""
        code = "myCursor.drawSquare(50);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "DRAW_SQUARE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["side_length"], {"type": "VALUE", "value": "50"})

    def test_draw_circle(self):
        """Test if drawing a circle is parsed correctly."""
        code = "myCursor.drawCircle(30);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "DRAW_CIRCLE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["radius"], {"type": "VALUE", "value": "30"})

    def test_draw_arc(self):
        """Test if drawing an arc is parsed correctly."""
        code = "myCursor.drawArc(50, 90);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "DRAW_ARC")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["radius"], {"type": "VALUE", "value": "50"})
        self.assertEqual(syntax_tree[0]["angle"], {"type": "VALUE", "value": "90"})

    def test_animate(self):
        """Test if animating a cursor is parsed correctly."""
        code = "myCursor.animate(10);"
        syntax_tree = self.parse_code(code)
        self.assertEqual(syntax_tree[0]["type"], "ANIMATE")
        self.assertEqual(syntax_tree[0]["cursor"], "myCursor")
        self.assertEqual(syntax_tree[0]["steps"], {"type": "VALUE", "value": "10"})
    

if __name__ == "__main__":
    unittest.main()