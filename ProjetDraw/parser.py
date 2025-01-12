# parser.py
from lexer import Lexer
from utils.tokens import Token
from utils.tokens import TokenType

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser with a list of tokens and sets the initial position.
        """
        self.tokens = tokens
        self.position = 0
        self.errors = []
    
    def parse(self):
        """
        Main parse function to build the syntax tree by processing tokens sequentially.
        """
        syntax_tree = []  # List to store syntax nodes

        while self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            print(f"Current token at position {self.position}/{len(self.tokens)}: {current_token}")
            try:
                # Determine token type and delegate parsing to the appropriate method
                if current_token.type == TokenType.CURSOR:
                    syntax_tree.append(self.parse_cursor_declaration())
                elif current_token.type == TokenType.IDENTIFIER:
                    if self.position + 1 < len(self.tokens) and self.tokens[self.position + 1].type in {
                        TokenType.MINUS_MINUS, TokenType.PLUS_PLUS, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL
                    }:
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
                elif current_token.type == TokenType.LBRACE:
                    syntax_tree.append(self.parse_block())
                elif current_token.type == TokenType.RBRACE:
                    # Handle closing braces; they belong to parse_block
                    print(f"Detected RBRACE at position {self.position}")
                    break
                else:
                    raise SyntaxError(f"Unexpected token {current_token.type} at position {self.position}")
            except SyntaxError as e:
                self.errors.append(str(e))
                self.position += 1  # Skip the problematic token
        if self.errors:
            print("Parsing completed with errors:")
            for error in self.errors:
                print(f" - {error}")
        return syntax_tree
    

    def parse_cursor_declaration(self):
        """
        Parses a cursor declaration like `cursor myCursor;`.
        - Expects the keyword `cursor`, followed by an identifier (cursor name), 
        and ends with a semicolon (`;`).
        - Returns a dictionary representing the cursor declaration.
        """
        try:
            self.expect(TokenType.CURSOR)  # Ensure the token is 'cursor'.
            cursor_name = self.expect(TokenType.IDENTIFIER).value  # Get the cursor name.
            self.expect(TokenType.SEMICOLON)  # Ensure the declaration ends with a semicolon.
            return {"type": "CURSOR_DECLARATION", "name": cursor_name}
        except SyntaxError:
            self.errors.append("Invalid cursor declaration syntax.")  # Log the error.
            raise


    def parse_cursor_method(self):
        """
        Parses cursor methods like `cursorName.method(...)`.
        - Validates the cursor name, the method separator (`.`), and the method type.
        - Delegates parsing to the specific method handlers based on the method type.
        - Returns a dictionary representing the method call.
        """
        cursor_name = self.expect(TokenType.IDENTIFIER).value  # Get the cursor name.
        self.expect(TokenType.DOT)  # Ensure there's a `.` after the cursor name.
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
        ).type  # Identify the method being called.

        # Delegate parsing based on the method type.
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
        # Parses the `setPosition(x, y)` method call.
        # Ensures proper syntax and returns a dictionary with x and y values.
        self.expect(TokenType.LPAREN)  
        x_value = self.parse_expression()  
        self.expect(TokenType.COMMA)  
        y_value = self.parse_expression()  
        self.expect(TokenType.RPAREN)  
        self.expect(TokenType.SEMICOLON)  
        return {"type": "SET_POSITION", "cursor": cursor_name, "x": x_value, "y": y_value}

    def parse_draw_line(self, cursor_name):
        # Parses the `drawLine(length)` method call.
        # Ensures proper syntax and returns a dictionary with the line's length.
        self.expect(TokenType.LPAREN)  
        length_value = self.parse_expression()  
        self.expect(TokenType.RPAREN)  
        self.expect(TokenType.SEMICOLON)  
        return {"type": "DRAW_LINE", "cursor": cursor_name, "length": length_value}

    def parse_set_color(self, cursor_name):
        # Parses the `setColor(color)` method call.
        # Ensures proper syntax and returns a dictionary with the color value.
        self.expect(TokenType.LPAREN)  
        color_value = self.expect(TokenType.COLOR, TokenType.IDENTIFIER).value  
        self.expect(TokenType.RPAREN)  
        self.expect(TokenType.SEMICOLON)  
        return {"type": "SET_COLOR", "cursor": cursor_name, "color": color_value}

    def parse_move(self, cursor_name):
        # Parses the `move(distance)` method call.
        # Ensures proper syntax and returns a dictionary with the move distance.
        self.expect(TokenType.LPAREN)  
        distance_value = self.parse_expression()  
        self.expect(TokenType.RPAREN)  
        self.expect(TokenType.SEMICOLON)  
        return {"type": "MOVE", "cursor": cursor_name, "distance": distance_value}
    
    def parse_rotate(self, cursor_name):
        # Parses the `rotate(angle)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        angle_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "ROTATE", "cursor": cursor_name, "angle": angle_value}

    def parse_draw_square(self, cursor_name):
        # Parses the `drawSquare(side_length)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        side_length = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_SQUARE", "cursor": cursor_name, "side_length": side_length}

    def parse_draw_point(self, cursor_name):
        # Parses the `drawPoint()` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_POINT", "cursor": cursor_name}

    def parse_draw_arc(self, cursor_name):
        # Parses the `drawArc(radius, angle)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        radius_value = self.parse_expression()
        self.expect(TokenType.COMMA)
        angle_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_ARC", "cursor": cursor_name, "radius": radius_value, "angle": angle_value}

    def parse_animate(self, cursor_name):
        # Parses the `animate(steps)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        animation_steps = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "ANIMATE", "cursor": cursor_name, "steps": animation_steps}

    def parse_set_thickness(self, cursor_name):
        # Parses the `setThickness(value)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        thickness_value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "SET_THICKNESS", "cursor": cursor_name, "thickness": thickness_value}

    def parse_draw_circle(self, cursor_name):
        # Parses the `drawCircle(radius)` method call and returns the corresponding action dictionary.
        self.expect(TokenType.LPAREN)
        radius = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return {"type": "DRAW_CIRCLE", "cursor": cursor_name, "radius": radius}

    def parse_if_statement(self):
        # Parses an `if` statement.
        # Extracts the condition, true block, and optional false block.
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_condition()
        self.expect(TokenType.RPAREN)
        true_block = self.parse_block()

        false_block = None
        if self.match(TokenType.ELSE):  # Checks for an optional `else` block.
            self.expect(TokenType.ELSE)
            false_block = self.parse_block()

        return {"type": "IF_STATEMENT", "condition": condition, "true_block": true_block, "false_block": false_block}

    def parse_while_loop(self):
        # Parses a `while` loop.
        # Extracts the condition and body block.
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_condition()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return {"type": "WHILE_LOOP", "condition": condition, "body": body}

    def parse_for_loop(self):
        # Parses a `for` loop.
        # Extracts initialization, condition, update, and body block.
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
        # Parses a mathematical or logical expression.
        left = self.expect(TokenType.IDENTIFIER, TokenType.NUMBER)

        while self.match(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.expect(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO).type
            right = self.expect(TokenType.IDENTIFIER, TokenType.NUMBER)
            left = {
                "type": "EXPRESSION",
                "left": left.value if isinstance(left, Token) else left,
                "operator": operator,
                "right": right.value
            }

        if isinstance(left, Token):
            return {"type": "VALUE", "value": left.value}  # Single value case.

        return left  # Complex expression case.

    def parse_condition(self):
        # Parses a conditional expression with operators like ==, <, >, etc.
        try:
            print(f"Parsing condition at position {self.position}, token: {self.tokens[self.position]}")
            left_expr = self.parse_expression()
            operator = self.expect(
                TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN, TokenType.GREATER_THAN
            ).type
            right_expr = self.parse_expression()
            return {"type": "CONDITION", "left": left_expr, "operator": operator, "right": right_expr}
        except SyntaxError:
            self.errors.append("Invalid condition syntax.")
            raise

    def parse_variable_declaration(self):
        # Parses a variable declaration (`int x = 5;` or `float y = 3.14;`).
        var_type = self.expect(TokenType.INT, TokenType.FLOAT).type
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)  # Expects '='.
        var_value_token = self.expect(TokenType.NUMBER)
        var_value = {"type": "VALUE", "value": var_value_token.value}

        self.expect(TokenType.SEMICOLON)  # Expects the declaration to end with a semicolon.
        return {
            "type": "VARIABLE_DECLARATION",
            "var_type": var_type,
            "name": var_name,
            "value": var_value
        }

    def parse_variable_update(self):
        """
        Parses a variable update statement (e.g., i++, i--, i += 2, i -= 2).
        - Extracts the variable name and the operator (++/--/+=/-=).
        - For += or -=, also extracts the value to update.
        - Returns a dictionary representing the `VARIABLE_UPDATE` action.
        """
        var_name = self.expect(TokenType.IDENTIFIER).value
        update_op = self.expect(
            TokenType.PLUS_PLUS, 
            TokenType.MINUS_MINUS, 
            TokenType.PLUS_EQUAL, 
            TokenType.MINUS_EQUAL
        ).type

        if update_op in (TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL):  # Handle += or -= with a value.
            value = self.expect(TokenType.NUMBER).value
            return {
                "type": "VARIABLE_UPDATE",
                "name": var_name,
                "operator": update_op,
                "value": {"type": "VALUE", "value": value}
            }

        return {  # Handle ++ or -- without a value.
            "type": "VARIABLE_UPDATE",
            "name": var_name,
            "operator": update_op
        }

    def parse_block(self):
        """
        Parses a block of statements enclosed in `{}`.
        - Processes each statement within the block recursively.
        - Returns a dictionary representing the `BLOCK` with its statements.
        """
        try:
            self.expect(TokenType.LBRACE)  # Expect opening brace.
            statements = []

            while True:
                if self.match(TokenType.RBRACE):  # Check for closing brace.
                    self.expect(TokenType.RBRACE)  # Consume the closing brace.
                    break
                if self.position >= len(self.tokens):  # Ensure input doesn't end unexpectedly.
                    raise SyntaxError("Unexpected end of input. Missing closing '}' for block.")

                statements.append(self.parse())  # Parse nested statements.

            return {"type": "BLOCK", "statements": statements}
        except SyntaxError:
            self.errors.append("Invalid block structure.")
            raise

    def expect(self, *token_types):
        """
        Checks if the current token matches one of the expected types.
        - Advances the position if the token matches.
        - Raises a `SyntaxError` if the token doesn't match.
        """
        if self.position >= len(self.tokens):  # Ensure position is within range.
            expected_readable = ", ".join(Lexer.translate_token_type(t) for t in token_types)
            raise SyntaxError(f"Unexpected end of input. Expected one of: {expected_readable}.")

        current_token = self.tokens[self.position]
        if current_token.type in token_types:
            self.position += 1  # Advance to the next token.
            return current_token
        else:
            expected_readable = ", ".join(Lexer.translate_token_type(t) for t in token_types)
            found_readable = Lexer.translate_token_type(current_token.type)
            raise SyntaxError(
                f"Syntax error at position {self.position}: Expected one of ({expected_readable}), but found '{found_readable}'."
            )

    def match(self, *token_types):
        """
        Checks if the current token matches one of the specified types.
        - Does not advance the position.
        - Returns `True` if a match is found, `False` otherwise.
        """
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            return current_token.type in token_types
        return False