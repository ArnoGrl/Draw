# parser.py
from lexer import Lexer
from utils.tokens import Token
from utils.tokens import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def parse(self):
        syntax_tree = []  # Liste pour stocker les nœuds syntaxiques

        while self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            print(f"Current token at position {self.position}/{len(self.tokens)}: {current_token}")

            if current_token.type == TokenType.CURSOR:
                syntax_tree.append(self.parse_cursor_declaration())
            elif current_token.type == TokenType.IDENTIFIER:
                if self.position + 1 < len(self.tokens) and self.tokens[self.position + 1].type in {TokenType.MINUS_MINUS, TokenType.PLUS_PLUS, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL}:
                    syntax_tree.append(self.parse_variable_update())
                else:
                    syntax_tree.append(self.parse_cursor_method())
            elif current_token.type == TokenType.IF:
                syntax_tree.append(self.parse_if_statement())
            elif current_token.type == TokenType.FOR:
                syntax_tree.append(self.parse_for_loop())
            elif current_token.type == TokenType.WHILE:
                syntax_tree.append(self.parse_while_loop())
            elif current_token.type in (TokenType.INT, TokenType.FLOAT):
                syntax_tree.append(self.parse_variable_declaration())
            elif current_token.type == TokenType.LBRACE:  # Détecte un bloc
                syntax_tree.append(self.parse_block())
            elif current_token.type == TokenType.RBRACE:  # Détecte une accolade fermante
                # Passe l'accolade fermante à parse_block pour gérer la fin du bloc
                print(f"Detected RBRACE at position {self.position}")
                break  # On ne veut pas que parse analyse cela directement, c'est pour parse_block
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
        # Analyse des méthodes sur le curseur, par exemple setPosition, drawLine, setColor, etc.
        cursor_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.DOT)  # Assure qu'il y a un point après le curseur
        method_token = self.expect(
            TokenType.SET_POSITION,
            TokenType.SET_COLOR,
            TokenType.SET_THICKNESS,
            TokenType.MOVE,
            TokenType.ROTATE,
            TokenType.DRAW_LINE,
            TokenType.DRAW_SQUARE,
            TokenType.DRAW_CIRCLE,
            TokenType.DRAW_POINT,
            TokenType.DRAW_ARC,
            TokenType.ANIMATE
        ).type

        if method_token == TokenType.SET_POSITION:
            return self.parse_set_position(cursor_name)
        elif method_token == TokenType.SET_COLOR:
            return self.parse_set_color(cursor_name)
        elif method_token == TokenType.SET_THICKNESS:
            return self.parse_set_thickness(cursor_name)
        elif method_token == TokenType.MOVE:
            return self.parse_move(cursor_name)
        elif method_token == TokenType.ROTATE:
            return self.parse_rotate(cursor_name)
        elif method_token == TokenType.DRAW_LINE:
            return self.parse_draw_line(cursor_name)
        elif method_token == TokenType.DRAW_SQUARE:
            return self.parse_draw_square(cursor_name)
        elif method_token == TokenType.DRAW_CIRCLE:
            return self.parse_draw_circle(cursor_name)
        elif method_token == TokenType.DRAW_POINT:
            return self.parse_draw_point(cursor_name)
        elif method_token == TokenType.DRAW_ARC:
            return self.parse_draw_arc(cursor_name)
        elif method_token == TokenType.ANIMATE:
            return self.parse_animate(cursor_name)
        else:
            raise SyntaxError(f"Unexpected cursor method {method_token} at position {self.position}")

        
    def parse_set_position(self, cursor_name):
        # Analyse pour setPosition(x, y)
        self.expect(TokenType.LPAREN)
        x_value = self.parse_expression()
        self.expect(TokenType.COMMA)
        y_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "SET_POSITION", "cursor": cursor_name, "x": x_value, "y": y_value}

    def parse_draw_line(self, cursor_name):
        # Analyse pour drawLine(length)
        self.expect(TokenType.LPAREN)
        length_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_LINE", "cursor": cursor_name, "length": length_value}
    
    def parse_set_color(self, cursor_name):
        self.expect(TokenType.LPAREN)
        color_value = self.expect(TokenType.COLOR, TokenType.IDENTIFIER).value
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "SET_COLOR", "cursor": cursor_name, "color": color_value}
    
    def parse_move(self, cursor_name):
        self.expect(TokenType.LPAREN)
        distance_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "MOVE", "cursor": cursor_name, "distance": distance_value}

    def parse_rotate(self, cursor_name):
        self.expect(TokenType.LPAREN)
        angle_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "ROTATE", "cursor": cursor_name, "angle": angle_value}
    
    def parse_draw_square(self, cursor_name):
        self.expect(TokenType.LPAREN)
        side_length = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_SQUARE", "cursor": cursor_name, "side_length": side_length}

    def parse_draw_point(self, cursor_name):
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_POINT", "cursor": cursor_name}

    def parse_draw_arc(self, cursor_name):
        self.expect(TokenType.LPAREN)
        radius_value = self.parse_expression()
        self.expect(TokenType.COMMA)
        angle_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_ARC", "cursor": cursor_name, "radius": radius_value, "angle": angle_value}

    def parse_animate(self, cursor_name):
        self.expect(TokenType.LPAREN)
        animation_steps = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "ANIMATE", "cursor": cursor_name, "steps": animation_steps}

    def parse_set_thickness(self, cursor_name):
        # Analyse pour setThickness(value)
        self.expect(TokenType.LPAREN)
        thickness_value = self.parse_expression()  # Utilise parse_expression
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "SET_THICKNESS", "cursor": cursor_name, "thickness": thickness_value}

    
    def parse_draw_circle(self, cursor_name):
        self.expect(TokenType.LPAREN)
        radius = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_CIRCLE", "cursor": cursor_name, "radius": radius}


    def parse_if_statement(self):
        # Analyse de la structure conditionnelle if
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_condition()
        self.expect(TokenType.RPAREN)
        true_block = self.parse_block()

        # Gère le bloc 'else' optionnel
        false_block = None
        if self.match(TokenType.ELSE):
            self.expect(TokenType.ELSE)
            false_block = self.parse_block()

        return {"type": "IF_STATEMENT", "condition": condition, "true_block": true_block, "false_block": false_block}

    def parse_while_loop(self):
        # Analyse d'une boucle while
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_condition()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return {"type": "WHILE_LOOP", "condition": condition, "body": body}

    def parse_for_loop(self):
        # Analyse de la boucle for
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init = self.parse_variable_declaration()
        condition = self.parse_condition()
        self.expect(TokenType.SEMICOLON)
        update = self.parse_variable_update()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return {"type": "FOR_LOOP", "init": init, "condition": condition, "update": update, "body": body}

    def parse_expression(self):
        # Début de l'analyse
        left = self.expect(TokenType.IDENTIFIER, TokenType.NUMBER)

        while self.match(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.expect(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO).type
            right = self.expect(TokenType.IDENTIFIER, TokenType.NUMBER)
            left = {"type": "EXPRESSION", "left": left.value if isinstance(left, Token) else left, 
                    "operator": operator, "right": right.value}

        # Si `left` est une valeur simple (pas une expression), formatez-la
        if isinstance(left, Token):
            return {"type": "VALUE", "value": left.value}

        return left
    
    def parse_condition(self):
        print(f"Parsing condition at position {self.position}, token: {self.tokens[self.position]}")
        left_expr = self.parse_expression()  # Analyser une expression complexe à gauche
        operator = self.expect(TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                            TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN, TokenType.GREATER_THAN 
                            ).type
        right_expr = self.parse_expression()  # Analyser une expression complexe à droite
        return {"left": left_expr, "operator": operator, "right": right_expr}



    
    def parse_variable_declaration(self):
        # Analyse pour la déclaration de variable
        var_type = self.expect(TokenType.INT, TokenType.FLOAT).type  # Type int ou float
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        var_value = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.SEMICOLON)
        return {"type": "VARIABLE_DECLARATION", "var_type": var_type, "name": var_name, "value": var_value}

    def parse_variable_update(self):
        # Analyse pour la mise à jour d'une variable (par exemple, i++, i--, i += 2, i -= 2)
        var_name = self.expect(TokenType.IDENTIFIER).value
        
        # Vérifie si l'opérateur est de type ++, --, += ou -=
        update_op = self.expect(
            TokenType.PLUS_PLUS, 
            TokenType.MINUS_MINUS, 
            TokenType.PLUS_EQUAL, 
            TokenType.MINUS_EQUAL
        ).type
        
        # Si l'opérateur est += ou -=, il doit y avoir une valeur à droite
        if update_op in (TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL):
            value = self.expect(TokenType.NUMBER).value  # Attend une valeur numérique après l'opérateur
            return {
                "type": "VARIABLE_UPDATE",
                "name": var_name,
                "operator": update_op,
                "value": {"type": "VALUE", "value": value}
            }
        
        # Pour ++ ou --, aucune valeur supplémentaire n'est attendue
        return {
            "type": "VARIABLE_UPDATE",
            "name": var_name,
            "operator": update_op
        }

    def parse_block(self):
        self.expect(TokenType.LBRACE)  # Vérifie et consomme l'ouverture du bloc
        print(f"Entering block at position {self.position - 1}, token: {self.tokens[self.position - 1]}")

        statements = []

        while True:
            if self.match(TokenType.RBRACE):  # Détecte l'accolade fermante
                print(f"Expecting RBRACE at position {self.position}, token: {self.tokens[self.position]}")
                self.expect(TokenType.RBRACE)  # Consomme l'accolade fermante
                break  # Terminer le bloc
            if self.position >= len(self.tokens):  # Si la fin des tokens est atteinte
                raise SyntaxError("Unexpected end of input. Missing closing '}' for block.")

            print(f"Parsing statement inside block at position {self.position}, token: {self.tokens[self.position]}")
            statements.append(self.parse())  # Appelle parse pour analyser les instructions internes

        print(f"Exiting block at position {self.position}")
        return {"type": "BLOCK", "statements": statements}


    def expect(self, *token_types):
        if self.position >= len(self.tokens):  # Vérifie explicitement si la position dépasse la longueur des tokens
            print(f"Error: Reached end of tokens at position {self.position}, expected {token_types}")
            raise SyntaxError(f"Unexpected end of input, expected {token_types}")

        current_token = self.tokens[self.position]
        if current_token.type in token_types:
            print(f"Consuming token at position {self.position}: {current_token}")
            self.position += 1
            return current_token
        else:
            # Ajout de débogage : Affiche ce qui était attendu et ce qui a été trouvé
            print(f"Error at position {self.position}: expected {token_types}, found {current_token}")
            raise SyntaxError(f"Expected {token_types} at position {self.position}, but found {current_token.type}")


    def match(self, *token_types):
        # Débogage : Vérification des tokens et des types attendus
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            print(f"Matching token at position {self.position}: {current_token} against {token_types}")
            return current_token.type in token_types
        print(f"Position {self.position} is out of range for matching token types: {token_types}")
        return False

