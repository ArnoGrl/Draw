import unittest
from lexer import Lexer
from parser import Parser
from utils.tokens import TokenType
import pprint

class TestParser(unittest.TestCase):
    
    def parse_code(self, code):
        """Helper function to parse code and return the syntax tree."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    

    def test_boucle_for(self):
        code = """
        while(i < 12){
            myCursor.drawSquare(10);
        }
        for(int i = 0; i <= 10; i++){
            myCursor.drawCircle(10);
        }
        """
        syntax_tree = self.parse_code(code)
        pprint.pprint(syntax_tree)
