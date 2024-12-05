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
    
    def test_block_with_two_statements(self):
        code = """
        {
            myCursor.setColor(red);
            myCursor.setThickness(5);
        }
        myCursor.setColor(red);
        {
            myCursor.setColor(red);
            myCursor.setThickness(5);
        }
        myCursor.setColor(red);
        """
        syntax_tree = self.parse_code(code)
        print("Generated AST:")
        pprint.pprint(syntax_tree)


            

        
        
        
        
        
        
        

        
    

if __name__ == "__main__":
    unittest.main()