from enum import Enum

# Enumeration of all possible token types in Draw++
class TokenType(Enum):
    # Keywords for cursor operations
    CURSOR = "CURSOR"                # Declares a cursor
    SET_POSITION = "SET_POSITION"    # Sets cursor position
    SET_COLOR = "SET_COLOR"          # Sets cursor color
    SET_THICKNESS = "SET_THICKNESS"  # Sets cursor line thickness
    MOVE = "MOVE"                    # Moves the cursor
    ROTATE = "ROTATE"                # Rotates the cursor
    DRAW_LINE = "DRAW_LINE"          # Draws a line
    DRAW_SQUARE = "DRAW_SQUARE"      # Draws a square
    DRAW_CIRCLE = "DRAW_CIRCLE"      # Draws a circle
    DRAW_POINT = "DRAW_POINT"        # Draws a point
    DRAW_ARC = "DRAW_ARC"            # Draws an arc
    ANIMATE = "ANIMATE"              # Animates a drawing
    
    # Control structures
    IF = "IF"                        # If condition
    ELSE = "ELSE"                    # Else condition
    FOR = "FOR"                      # For loop
    WHILE = "WHILE"                  # While loop
    BLOCK = "BLOCK"                  # Instruction block
    FUNCTION = "FUNCTION"            # Function definition
    REPEAT = "REPEAT"                # Repeats an instruction block
    
    # Data types
    INT = "INT"                      # Integer type
    FLOAT = "FLOAT"                  # Floating-point type
    IDENTIFIER = "IDENTIFIER"        # Variable or cursor name
    NUMBER = "NUMBER"                # Numeric value (int or float)
    COLOR = "COLOR"                  # Predefined color value
    
    # Operators and comparators
    ASSIGN = "ASSIGN"                # Assignment operator '='
    EQUAL = "EQUAL"                  # Equality operator '=='
    NOT_EQUAL = "NOT_EQUAL"          # Inequality operator '!='
    LESS_THAN = "LESS_THAN"          # Less than '<'
    GREATER_THAN = "GREATER_THAN"    # Greater than '>'
    LESS_EQUAL = "LESS_EQUAL"        # Less than or equal '<='
    GREATER_EQUAL = "GREATER_EQUAL"  # Greater than or equal '>='
    PLUS_PLUS = "PLUS_PLUS"          # Increment operator '++'
    MINUS_MINUS = "MINUS_MINUS"      # Decrement operator '--'
    PLUS_EQUAL = "PLUS_EQUAL"        # Increment assignment operator '+='
    MINUS_EQUAL = "MINUS_EQUAL"      # Decrement assignment operator '-='

    # Arithmetic operators
    PLUS = "PLUS"                    # Addition '+'
    MINUS = "MINUS"                  # Subtraction '-'
    MULTIPLY = "MULTIPLY"            # Multiplication '*'
    DIVIDE = "DIVIDE"                # Division '/'
    MODULO = "MODULO"                # Modulus '%'
    
    # Symbols
    LPAREN = "LPAREN"                # Left parenthesis '('
    RPAREN = "RPAREN"                # Right parenthesis ')'
    LBRACE = "LBRACE"                # Left brace '{'
    RBRACE = "RBRACE"                # Right brace '}'
    SEMICOLON = "SEMICOLON"          # Semicolon ';'
    COMMA = "COMMA"                  # Comma ','
    DOT = "DOT"                      # Dot '.'

# Representation of a token with type and value
class Token:
    def __init__(self, type, value):
        """
        Initializes a token with its type (from TokenType) and value.
        Args:
            type: TokenType enum representing the token's type.
            value: Actual value of the token (e.g., 'cursor', '100', '>').
        """
        self.type = type  # Token type
        self.value = value  # Token value
    
    def __repr__(self):
        """
        Returns a string representation of the token for debugging purposes.
        """
        return f"Token(type={self.type}, value={self.value})"
