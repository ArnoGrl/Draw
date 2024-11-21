# parser.py
from utils.tokens import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def parse(self):
        syntax_tree = []  # Liste pour stocker les nœuds syntaxiques
        
        while self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            
            # Vérification du type de l'instruction
            if current_token.type == TokenType.CURSOR:
                syntax_tree.append(self.parse_cursor_declaration())
            elif current_token.type == TokenType.IDENTIFIER:
                syntax_tree.append(self.parse_cursor_method())
            elif current_token.type == TokenType.IF:
                syntax_tree.append(self.parse_if_statement())
            elif current_token.type == TokenType.FOR:
                syntax_tree.append(self.parse_for_loop())
            else:
                raise SyntaxError(f"Unexpected token {current_token.type} at position {self.position}")
        
        return syntax_tree

    def parse_cursor_declaration(self):
        # Analyse de la déclaration d'un curseur
        self.expect(TokenType.CURSOR)  # Assure que le token est bien un 'cursor'
        cursor_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)  # Assure que la déclaration finit par un ';'
        return {"type": "CURSOR_DECLARATION", "name": cursor_name}

    def parse_cursor_method(self):
        # Analyse des méthodes sur le curseur, par exemple setPosition, drawLine
        cursor_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.DOT)  # Assure qu'il y a un point après le curseur
        method_token = self.expect(TokenType.SET_POSITION, TokenType.DRAW_LINE).type  # Détecte la méthode

        if method_token == TokenType.SET_POSITION:
            return self.parse_set_position(cursor_name)
        elif method_token == TokenType.DRAW_LINE:
            return self.parse_draw_line(cursor_name)
        else:
            raise SyntaxError(f"Unexpected cursor method {method_token} at position {self.position}")

        
    def parse_set_position(self, cursor_name):
        # Analyse pour setPosition(x, y)
        self.expect(TokenType.LPAREN)
        x_value = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.COMMA)
        y_value = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "SET_POSITION", "cursor": cursor_name, "x": x_value, "y": y_value}

    def parse_draw_line(self, cursor_name):
        # Analyse pour drawLine(length)
        self.expect(TokenType.LPAREN)
        length_value = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_LINE", "cursor": cursor_name, "length": length_value}

    def parse_if_statement(self):
        # Analyse de la structure conditionnelle if
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_condition()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        true_block = self.parse_block()
        self.expect(TokenType.RBRACE)

        # Gère le bloc 'else' optionnel
        false_block = None
        if self.match(TokenType.ELSE):
            self.expect(TokenType.LBRACE)
            false_block = self.parse_block()
            self.expect(TokenType.RBRACE)

        return {"type": "IF_STATEMENT", "condition": condition, "true_block": true_block, "false_block": false_block}

    def parse_for_loop(self):
        # Analyse de la boucle for
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init = self.parse_variable_declaration()
        self.expect(TokenType.SEMICOLON)
        condition = self.parse_condition()
        self.expect(TokenType.SEMICOLON)
        update = self.parse_variable_update()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        return {"type": "FOR_LOOP", "init": init, "condition": condition, "update": update, "body": body}

    def parse_condition(self):
        # Analyse de la condition dans une structure conditionnelle ou une boucle
        left_expr = self.expect(TokenType.IDENTIFIER).value
        operator = self.expect(TokenType.GREATER_THAN, TokenType.LESS_THAN, 
                       TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                       TokenType.EQUAL, TokenType.NOT_EQUAL).type
        # Attend un opérateur conditionnel
        right_expr = self.expect(TokenType.NUMBER).value
        return {"left": left_expr, "operator": operator, "right": right_expr}

    def parse_variable_declaration(self):
        # Analyse pour la déclaration de variable
        var_type = self.expect(TokenType.INT, TokenType.FLOAT).type  # Type int ou float
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        var_value = self.expect(TokenType.NUMBER).value
        return {"type": "VARIABLE_DECLARATION", "var_type": var_type, "name": var_name, "value": var_value}

    def parse_variable_update(self):
        # Analyse pour la mise à jour d'une variable (par exemple, identifiant++)
        var_name = self.expect(TokenType.IDENTIFIER).value
        update_op = self.expect(TokenType.PLUS_PLUS, TokenType.MINUS_MINUS).type  # Opérateur ++ ou --
        return {"type": "VARIABLE_UPDATE", "name": var_name, "operator": update_op}

    def parse_block(self):
        # Analyse d'un bloc d'instructions
        statements = []
        while not self.match(TokenType.RBRACE):
            statements.append(self.parse())
        return statements

    def expect(self, *token_types):
        # Vérifie si le token courant est du type attendu et avance
        if self.position < len(self.tokens) and self.tokens[self.position].type in token_types:
            current_token = self.tokens[self.position]
            self.position += 1
            return current_token
        else:
            raise SyntaxError(f"Expected {token_types} at position {self.position}")

    def match(self, token_type):
        # Vérifie si le token courant correspond au type spécifié sans avancer
        if self.position < len(self.tokens) and self.tokens[self.position].type == token_type:
            return True
        return False
