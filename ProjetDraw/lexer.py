# lexer.py
import re
from utils.tokens import Token, TokenType

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code  # Le code source à analyser
        self.tokens = []  # Liste pour stocker les tokens générés
        
    
    TOKEN_MAP = {
        TokenType.CURSOR: "cursor",
        TokenType.SET_POSITION: "setPosition",
        TokenType.SET_COLOR: "setColor",
        TokenType.SET_THICKNESS: "setThickness",
        TokenType.MOVE: "move",
        TokenType.ROTATE: "rotate",
        TokenType.DRAW_LINE: "drawLine",
        TokenType.DRAW_SQUARE: "drawSquare",
        TokenType.DRAW_CIRCLE: "drawCircle",
        TokenType.DRAW_POINT: "drawPoint",
        TokenType.DRAW_ARC: "drawArc",
        TokenType.ANIMATE: "animate",
        TokenType.IF: "if",
        TokenType.ELSE: "else",
        TokenType.FOR: "for",
        TokenType.WHILE: "while",
        TokenType.INT: "int",
        TokenType.FLOAT: "float",
        TokenType.LBRACE: "{",
        TokenType.RBRACE: "}",
        TokenType.LPAREN: "(",
        TokenType.RPAREN: ")",
        TokenType.COMMA: ",",
        TokenType.SEMICOLON: ";",
        TokenType.ASSIGN: "=",
        TokenType.DOT: ".",
        TokenType.PLUS: "+",
        TokenType.MINUS: "-",
        TokenType.MULTIPLY: "*",
        TokenType.DIVIDE: "/",
        TokenType.MODULO: "%",
        TokenType.PLUS_PLUS: "++",
        TokenType.MINUS_MINUS: "--",
        TokenType.PLUS_EQUAL: "+=",
        TokenType.MINUS_EQUAL: "-=",
        TokenType.NUMBER: "number",
        TokenType.IDENTIFIER: "identifier",
        TokenType.LESS_THAN: "<",
        TokenType.GREATER_THAN: ">",
        TokenType.EQUAL: "==",
        TokenType.NOT_EQUAL: "!=",
        TokenType.LESS_EQUAL: "<=",
        TokenType.GREATER_EQUAL: ">=",
    }

    @staticmethod
    def translate_token_type(token_type):
        return Lexer.TOKEN_MAP.get(token_type, str(token_type))


    def tokenize(self):
        # Mots-clés et symboles spécifiques associés à leurs types
        patterns = {
            "cursor": TokenType.CURSOR,
            "setPosition": TokenType.SET_POSITION,
            "setColor": TokenType.SET_COLOR,
            "setThickness": TokenType.SET_THICKNESS,
            "move": TokenType.MOVE,
            "rotate": TokenType.ROTATE,
            "drawLine": TokenType.DRAW_LINE,
            "drawSquare": TokenType.DRAW_SQUARE,
            "drawCircle": TokenType.DRAW_CIRCLE,
            "drawPoint": TokenType.DRAW_POINT,
            "drawArc": TokenType.DRAW_ARC,
            "animate": TokenType.ANIMATE,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "for": TokenType.FOR,
            "while": TokenType.WHILE,
            "block": TokenType.BLOCK,
            "function": TokenType.FUNCTION,
            "repeat": TokenType.REPEAT,
            "++": TokenType.PLUS_PLUS,
            "--": TokenType.MINUS_MINUS,
            "int": TokenType.INT,
            "float": TokenType.FLOAT,
        }
        
        # Expressions régulières pour détecter les différents types de tokens
        token_specs = [
            ("PLUS_PLUS", r'\+\+'),               # ++
            ("MINUS_MINUS", r'--'),
            ("PLUS_EQUAL", r'\+='),               # +=
            ("MINUS_EQUAL", r'-='),  
            ("PLUS", r'\+'),                     # +
            ("MINUS", r'-'),                     # -
            ("MULTIPLY", r'\*'),                 # *
            ("DIVIDE", r'/'),                    # /
            ("MODULO", r'%'),                    # %
            ("NUMBER", r'-?\d+(\.\d*)?'),        # Nombres (entiers, flottants, et négatifs)
            ("IDENTIFIER", r'[a-zA-Z_]\w*'),
            ("EQUAL", r'\=\='),
            ("NOT_EQUAL", r'\!\='),
            ("LESS_EQUAL", r'\<\='),
            ("GREATER_EQUAL", r'\>\='),
            ("SYMBOL", r'[;(),{}=.<>!]'),        # Symboles spécifiques ponctuels
            ("SKIP", r'[ \t]+'),                 # Ignore les espaces et tabulations
            ("NEWLINE", r'\n'),                  # Ignore les nouvelles lignes
        ]
        
        # Compilation de l'expression régulière unique
        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
        get_token = re.compile(token_regex).match

        # Initialisation de la position
        pos = 0
        length = len(self.source_code)

        # Boucle de tokenisation avec vérification caractère par caractère
        while pos < length:
            match = get_token(self.source_code, pos)
            if match:
                kind = match.lastgroup
                value = match.group(kind)

                if kind == "NUMBER":
                    token_type = TokenType.NUMBER
                elif kind in ("PLUS_EQUAL", "MINUS_EQUAL","EQUAL", "NOT_EQUAL", "LESS_EQUAL", "GREATER_EQUAL", "PLUS_PLUS", "MINUS_MINUS", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO"):
                    token_type = TokenType[kind]

                elif kind == "IDENTIFIER" and value in patterns:
                    token_type = patterns[value]  # Mot-clé ou symbole spécifique
                elif kind == "IDENTIFIER":
                    if value in patterns:
                        token_type = patterns[value]  # Mot-clé ou symbole spécifique
                    else:
                        token_type = TokenType.IDENTIFIER  # Identifiant utilisateur
                elif kind == "SYMBOL":
                    symbol_types = {
                        ";": TokenType.SEMICOLON,
                        "(": TokenType.LPAREN,
                        ")": TokenType.RPAREN,
                        "{": TokenType.LBRACE,
                        "}": TokenType.RBRACE,
                        ",": TokenType.COMMA,
                        "=": TokenType.ASSIGN,
                        ".": TokenType.DOT,
                        "<": TokenType.LESS_THAN,
                        ">": TokenType.GREATER_THAN,
                    }
                    token_type = symbol_types.get(value)
                    if token_type is None:
                        raise SyntaxError(f"Unknown symbol '{value}' at position {pos}")
            
                elif kind in ("SKIP", "NEWLINE"):
                    pos = match.end()
                    continue  # Ignore les espaces, tabulations et nouvelles lignes
                else:
                    raise SyntaxError(f"Unknown token '{value}' at position {pos}")

                # Ajouter le token généré
                self.tokens.append(Token(token_type, value))
                pos = match.end()
            else:
                # Aucun motif ne correspond, caractère inconnu
                raise SyntaxError(f"Unknown token '{self.source_code[pos]}' at position {pos}")

        return self.tokens
