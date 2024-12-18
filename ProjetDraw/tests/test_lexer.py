# test_lexer.py
import unittest
from lexer import Lexer
from utils.tokens import TokenType

class TestLexer(unittest.TestCase):

    def tokenize_code(self, code):
        """Helper function to create a lexer and tokenize code."""
        lexer = Lexer(code)
        return lexer.tokenize()

    def test_cursor_declaration(self):
        """Test cursor declaration."""
        tokens = self.tokenize_code("cursor myCursor; == ")
        self.assertEqual(tokens[0].type, TokenType.CURSOR)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[3].type, TokenType.EQUAL)

    def test_set_position(self):
        """Test setPosition with coordinates."""
        tokens = self.tokenize_code("myCursor.setPosition(100, 200);")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.DOT)  # Ajout de DOT pour accéder à setPosition
        self.assertEqual(tokens[2].type, TokenType.SET_POSITION)
        self.assertEqual(tokens[3].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.NUMBER)
        self.assertEqual(tokens[5].type, TokenType.COMMA)
        self.assertEqual(tokens[6].type, TokenType.NUMBER)
        self.assertEqual(tokens[7].type, TokenType.RPAREN)
        self.assertEqual(tokens[8].type, TokenType.SEMICOLON)

    def test_set_color(self):
        """Test setColor command."""
        tokens = self.tokenize_code("myCursor.setColor(red);")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.DOT)  # Ajout de DOT pour accéder à setColor
        self.assertEqual(tokens[2].type, TokenType.SET_COLOR)
        self.assertEqual(tokens[3].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[5].type, TokenType.RPAREN)
        self.assertEqual(tokens[6].type, TokenType.SEMICOLON)

    def test_draw_square(self):
        """Test drawSquare command."""
        tokens = self.tokenize_code("myCursor.drawSquare(50);")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.DOT)  # Ajout de DOT pour accéder à drawSquare
        self.assertEqual(tokens[2].type, TokenType.DRAW_SQUARE)
        self.assertEqual(tokens[3].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.NUMBER)
        self.assertEqual(tokens[5].type, TokenType.RPAREN)
        self.assertEqual(tokens[6].type, TokenType.SEMICOLON)

    def test_if_statement(self):
        """Test if statement with a condition."""
        tokens = self.tokenize_code("if (length > 50) { myCursor.setColor(red); }")
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[1].type, TokenType.LPAREN)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.GREATER_THAN)
        self.assertEqual(tokens[4].type, TokenType.NUMBER)
        self.assertEqual(tokens[5].type, TokenType.RPAREN)
        self.assertEqual(tokens[6].type, TokenType.LBRACE)
        self.assertEqual(tokens[7].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[8].type, TokenType.DOT)  # Ajout de DOT pour accéder à setColor
        self.assertEqual(tokens[9].type, TokenType.SET_COLOR)
        self.assertEqual(tokens[10].type, TokenType.LPAREN)
        self.assertEqual(tokens[11].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[12].type, TokenType.RPAREN)
        self.assertEqual(tokens[13].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[14].type, TokenType.RBRACE)

    def test_for_loop(self):
        """Test for loop structure."""
        tokens = self.tokenize_code("for (int i = 0; i < 10; i++) { drawLine(50); }")
        self.assertEqual(tokens[0].type, TokenType.FOR)
        self.assertEqual(tokens[1].type, TokenType.LPAREN)
        self.assertEqual(tokens[2].type, TokenType.INT)          # 'int'
        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)   # 'i'
        self.assertEqual(tokens[4].type, TokenType.ASSIGN)       # '='
        self.assertEqual(tokens[5].type, TokenType.NUMBER)       # '0'
        self.assertEqual(tokens[6].type, TokenType.SEMICOLON)    # ';'
        self.assertEqual(tokens[7].type, TokenType.IDENTIFIER)   # 'i'
        self.assertEqual(tokens[8].type, TokenType.LESS_THAN)    # '<'
        self.assertEqual(tokens[9].type, TokenType.NUMBER)       # '10'
        self.assertEqual(tokens[10].type, TokenType.SEMICOLON)   # ';'
        self.assertEqual(tokens[11].type, TokenType.IDENTIFIER)  # 'i'
        self.assertEqual(tokens[12].type, TokenType.PLUS_PLUS)   # '++'
        self.assertEqual(tokens[13].type, TokenType.RPAREN)      # ')'
        self.assertEqual(tokens[14].type, TokenType.LBRACE)      # '{'
        self.assertEqual(tokens[15].type, TokenType.DRAW_LINE)
        self.assertEqual(tokens[16].type, TokenType.LPAREN)
        self.assertEqual(tokens[17].type, TokenType.NUMBER)
        self.assertEqual(tokens[18].type, TokenType.RPAREN)
        self.assertEqual(tokens[19].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[20].type, TokenType.RBRACE)

    def test_variable_decrement(self):
        tokens = self.tokenize_code("i--;")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.MINUS_MINUS)
        self.assertEqual(tokens[2].type, TokenType.SEMICOLON)


    def test_arithmetic_operators(self):
        """Test arithmetic operators."""
        tokens = self.tokenize_code("a + b - c * d / e % f;")
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)  # a
        self.assertEqual(tokens[1].type, TokenType.PLUS)        # +
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)  # b
        self.assertEqual(tokens[3].type, TokenType.MINUS)       # -
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)  # c
        self.assertEqual(tokens[5].type, TokenType.MULTIPLY)    # *
        self.assertEqual(tokens[6].type, TokenType.IDENTIFIER)  # d
        self.assertEqual(tokens[7].type, TokenType.DIVIDE)      # /
        self.assertEqual(tokens[8].type, TokenType.IDENTIFIER)  # e
        self.assertEqual(tokens[9].type, TokenType.MODULO)      # %
        self.assertEqual(tokens[10].type, TokenType.IDENTIFIER) # f
        self.assertEqual(tokens[11].type, TokenType.SEMICOLON)  # ;

    def test_braces_and_parentheses(self):
        """Test braces and parentheses."""
        tokens = self.tokenize_code("{ ( ) } ; , .")
        self.assertEqual(tokens[0].type, TokenType.LBRACE)      # {
        self.assertEqual(tokens[1].type, TokenType.LPAREN)      # (
        self.assertEqual(tokens[2].type, TokenType.RPAREN)      # )
        self.assertEqual(tokens[3].type, TokenType.RBRACE)      # }
        self.assertEqual(tokens[4].type, TokenType.SEMICOLON)   # ;
        self.assertEqual(tokens[5].type, TokenType.COMMA)       # ,
        self.assertEqual(tokens[6].type, TokenType.DOT)         # .

    def test_block_function_repeat(self):
        """Test keywords block, function, repeat."""
        tokens = self.tokenize_code("block myBlock { repeat(myBlock, 5); function myFunc() {} }")
        self.assertEqual(tokens[0].type, TokenType.BLOCK)       # block
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)  # myBlock
        self.assertEqual(tokens[2].type, TokenType.LBRACE)      # {
        self.assertEqual(tokens[3].type, TokenType.REPEAT)      # repeat
        self.assertEqual(tokens[4].type, TokenType.LPAREN)      # (
        self.assertEqual(tokens[5].type, TokenType.IDENTIFIER)  # myBlock
        self.assertEqual(tokens[6].type, TokenType.COMMA)       # ,
        self.assertEqual(tokens[7].type, TokenType.NUMBER)      # 5
        self.assertEqual(tokens[8].type, TokenType.RPAREN)      # )
        self.assertEqual(tokens[9].type, TokenType.SEMICOLON)   # ;
        self.assertEqual(tokens[10].type, TokenType.FUNCTION)   # function
        self.assertEqual(tokens[11].type, TokenType.IDENTIFIER) # myFunc
        self.assertEqual(tokens[12].type, TokenType.LPAREN)     # (
        self.assertEqual(tokens[13].type, TokenType.RPAREN)     # )
        self.assertEqual(tokens[14].type, TokenType.LBRACE)     # {
        self.assertEqual(tokens[15].type, TokenType.RBRACE)     # }
        self.assertEqual(tokens[16].type, TokenType.RBRACE)     # }

    def test_variable_declaration(self):
        """Test variable declaration."""
        tokens = self.tokenize_code("int x = 10; float y = 5.5;")
        self.assertEqual(tokens[0].type, TokenType.INT)         # int
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)  # x
        self.assertEqual(tokens[2].type, TokenType.ASSIGN)      # =
        self.assertEqual(tokens[3].type, TokenType.NUMBER)      # 10
        self.assertEqual(tokens[4].type, TokenType.SEMICOLON)   # ;
        self.assertEqual(tokens[5].type, TokenType.FLOAT)       # float
        self.assertEqual(tokens[6].type, TokenType.IDENTIFIER)  # y
        self.assertEqual(tokens[7].type, TokenType.ASSIGN)      # =
        self.assertEqual(tokens[8].type, TokenType.NUMBER)      # 5.5
        self.assertEqual(tokens[9].type, TokenType.SEMICOLON)   # ;

    def test_invalid_syntax(self):
        """Test invalid syntax raises SyntaxError."""
        with self.assertRaises(SyntaxError):
            self.tokenize_code("cursor my@Cursor;")

    def test_combined_commands(self):
        """Test a combination of commands."""
        tokens = self.tokenize_code("cursor myCursor; myCursor.setPosition(100, 200); if (a + b > 0) { drawLine(50); }")
        self.assertEqual(tokens[0].type, TokenType.CURSOR)      # cursor
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)  # myCursor
        self.assertEqual(tokens[2].type, TokenType.SEMICOLON)   # ;
        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)  # myCursor
        self.assertEqual(tokens[4].type, TokenType.DOT)         # .
        self.assertEqual(tokens[5].type, TokenType.SET_POSITION)# setPosition
        self.assertEqual(tokens[6].type, TokenType.LPAREN)      # (
        self.assertEqual(tokens[7].type, TokenType.NUMBER)      # 100
        self.assertEqual(tokens[8].type, TokenType.COMMA)       # ,
        self.assertEqual(tokens[9].type, TokenType.NUMBER)      # 200
        self.assertEqual(tokens[10].type, TokenType.RPAREN)     # )
        self.assertEqual(tokens[11].type, TokenType.SEMICOLON)  # ;

if __name__ == "__main__":
    unittest.main()
