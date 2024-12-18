from lexer import Lexer
from utils.tokens import Token
from utils.tokens import TokenType
from parser import Parser



# interpreter.py
class Interpreter:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
    
    def execute(self):
        # Execute commands from syntax tree
        for node in self.syntax_tree:
            self.execute_node(node)
    
    def execute_node(self, node):
        # Execute based on node type
        pass
