from enum import Enum

class TokenType(Enum):
    # Mots-clés
    CURSOR = "CURSOR"
    SET_POSITION = "SET_POSITION"
    SET_COLOR = "SET_COLOR"
    SET_THICKNESS = "SET_THICKNESS"
    MOVE = "MOVE"
    ROTATE = "ROTATE"
    DRAW_LINE = "DRAW_LINE"
    DRAW_SQUARE = "DRAW_SQUARE"
    DRAW_CIRCLE = "DRAW_CIRCLE"
    DRAW_POINT = "DRAW_POINT"
    DRAW_ARC = "DRAW_ARC"
    ANIMATE = "ANIMATE"
    
    # Structures de contrôle
    IF = "IF"
    ELSE = "ELSE"
    FOR = "FOR"
    WHILE = "WHILE"
    BLOCK = "BLOCK"
    FUNCTION = "FUNCTION"
    REPEAT = "REPEAT"
    
    # Types de données
    INT = "INT"
    FLOAT = "FLOAT"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    COLOR = "COLOR"
    
    # Opérateurs et comparateurs
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"
    
    # Symboles
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"

class Token:
    def __init__(self, type, value):
        self.type = type  # Type de token (TokenType)
        self.value = value  # Valeur du token (par exemple, 'cursor', '100', '>', etc.)
    
    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"
