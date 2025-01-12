import unittest
from utils.tokens import Token, TokenType
from parser import Parser

class TestMatchMethod(unittest.TestCase):

    def setUp(self):
        """Prépare les tokens pour les tests."""
        self.tokens = [
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENTIFIER, "myCursor"),
            Token(TokenType.DOT, "."),
            Token(TokenType.SET_COLOR, "setColor"),
            Token(TokenType.RBRACE, "}"),
        ]
        self.parser = Parser(self.tokens)

    def test_match_success(self):
        """Teste si match retourne True pour un type correct."""
        self.assertTrue(self.parser.match(TokenType.LBRACE), "Expected match to return True for LBRACE")

    def test_match_failure(self):
        """Teste si match retourne False pour un type incorrect."""
        self.parser.position = 1 
        self.assertFalse(self.parser.match(TokenType.LBRACE), "Expected match to return False for LBRACE at position 1")

    def test_match_out_of_range(self):
        """Teste si match retourne False pour une position hors des limites."""
        self.parser.position = len(self.tokens)  
        self.assertFalse(self.parser.match(TokenType.LBRACE), "Expected match to return False for out-of-range position")

    def test_match_multiple_types(self):
        """Teste si match fonctionne avec plusieurs types."""
        self.parser.position = 1  
        self.assertTrue(
            self.parser.match(TokenType.IDENTIFIER, TokenType.DOT),
            "Expected match to return True for IDENTIFIER or DOT at position 1"
        )
        self.parser.position = 2  
        self.assertTrue(
            self.parser.match(TokenType.IDENTIFIER, TokenType.DOT),
            "Expected match to return True for IDENTIFIER or DOT at position 2"
        )
        self.parser.position = 3  
        self.assertFalse(
            self.parser.match(TokenType.IDENTIFIER, TokenType.LBRACE),
            "Expected match to return False for IDENTIFIER or LBRACE at position 3"
        )

if __name__ == "__main__":
    unittest.main()