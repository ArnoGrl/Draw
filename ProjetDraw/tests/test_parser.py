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
    

    def test_positionnement_curseur(self):
        code = "myCursor.setPosition(10, 20);"
        expected_ast = [
            {
                "type": "SET_POSITION",
                "cursor": "myCursor",
                "x": {"type": "VALUE", "value": "10"},
                "y": {"type": "VALUE", "value": "20"}
            }
        ]
        self.assertEqual(self.parse_code(code), expected_ast)

    def test_couleur_curseur(self):
        code = "myCursor.setColor(red);"
        expected_ast = [
            {
                "type": "SET_COLOR",
                "cursor": "myCursor",
                "color": "red"
            }
        ]
        self.assertEqual(self.parse_code(code), expected_ast)


    def test_boucle_for(self):
        code = """
        for(int i = 0; i < 5; i++) {
            myCursor.drawLine(10);
        }
        """
        syntax_tree = self.parse_code(code)

        expected_ast = [
            {
                'type': 'FOR_LOOP',
                'init': {
                    'type': 'VARIABLE_DECLARATION',
                    'var_type': TokenType.INT,
                    'name': 'i',
                    'value': '0'
                },
                'condition': {
                    'left': {'type': 'VALUE', 'value': 'i'},
                    'operator': TokenType.LESS_THAN,
                    'right': {'type': 'VALUE', 'value': '5'}
                },
                'update': {
                    'type': 'VARIABLE_UPDATE',
                    'name': 'i',
                    'operator': TokenType.PLUS_PLUS
                },
                'body': {
                    'type': 'BLOCK',
                    'statements': [
                        [
                            {
                                'type': 'DRAW_LINE',
                                'cursor': 'myCursor',
                                'length': {'type': 'VALUE', 'value': '10'}
                            }
                        ]
                    ]
                }
            }
        ]

        self.assertEqual(syntax_tree, expected_ast)

    def test_boucle_while(self):
        code = """
        while(x > 0) {
            myCursor.drawPoint();
            x--
        }
        """
        expected_ast = [
            {
                'type': 'WHILE_LOOP',
                'condition': {
                    'left': {'type': 'VALUE', 'value': 'x'},
                    'operator': TokenType.GREATER_THAN,
                    'right': {'type': 'VALUE', 'value': '0'}
                },
                'body': {
                    'type': 'BLOCK',
                    'statements': [
                        [
                            {'cursor': 'myCursor', 'type': 'DRAW_POINT'},
                            {
                                'type': 'VARIABLE_UPDATE',
                                'name': 'x',
                                'operator': TokenType.MINUS_MINUS
                            }
                        ]
                    ]
                }
            }
        ]

        self.assertEqual(self.parse_code(code), expected_ast)

    def test_if_else(self):
        code = """
        if(x == 5) {
            myCursor.setColor(blue);
        } else {
            myCursor.setColor(red);
        }
        """
        expected_ast = [
            {
                "type": "IF_STATEMENT",
                "condition": {
                    "left": {"type": "VALUE", "value": "x"},
                    "operator": TokenType.EQUAL,
                    "right": {"type": "VALUE", "value": "5"}
                },
                "true_block": {
                    "type": "BLOCK",
                    "statements": [
                        [
                            {
                                "type": "SET_COLOR",
                                "cursor": "myCursor",
                                "color": "blue"
                            }
                        ]
                    ]
                },
                "false_block": {
                    "type": "BLOCK",
                    "statements": [
                        [
                            {
                                "type": "SET_COLOR",
                                "cursor": "myCursor",
                                "color": "red"
                            }
                        ]
                    ]
                }
            }
        ]
        
        # Exécute le parseur et compare l'AST généré à l'AST attendu
        self.assertEqual(self.parse_code(code), expected_ast)

    def test_variable_update(self):
        code = ''' 
                i++
                i--    
                i+=2
                i-=3
                
                '''
        expected_ast = [
            {"type": "VARIABLE_UPDATE", "name": "i", "operator": TokenType.PLUS_PLUS},
            {"type": "VARIABLE_UPDATE", "name": "i", "operator": TokenType.MINUS_MINUS},
            {
                "type": "VARIABLE_UPDATE",
                "name": "i",
                "operator": TokenType.PLUS_EQUAL,
                "value": {"type": "VALUE", "value": "2"}
            },
            {
                "type": "VARIABLE_UPDATE",
                "name": "i",
                "operator": TokenType.MINUS_EQUAL,
                "value": {"type": "VALUE", "value": "3"}
            }
        ]
        ast = self.parse_code(code)
        self.assertEqual(ast, expected_ast)
        pprint.pprint(ast)

    def test_boucle_for(self):
        code = """
        for(int i = 0; i < 5; i-=1) {
            myCursor.drawLine(10);
        }
        """
        syntax_tree = self.parse_code(code)
        pprint.pprint(syntax_tree)



            

        
        
        
        
        
        
        

        
    

if __name__ == "__main__":
    unittest.main()