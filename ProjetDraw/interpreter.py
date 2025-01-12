from lexer import Lexer
from utils.tokens import Token
from utils.tokens import TokenType
from parser import Parser

class Interpreter:
    def __init__(self, syntax_tree):
        """
        Initializes the Interpreter with the syntax tree (AST).
        Tracks declared variables, cursors, and detected errors.
        """
        self.syntax_tree = syntax_tree
        self.variables = {}  # Stores variables and their values
        self.cursors = {}    # Stores declared cursors
        self.errors = []     # List of detected errors

    def execute(self):
        """
        Iterates through the AST and processes each node.
        Accumulates errors encountered during execution.
        """
        for node in self.syntax_tree:
            try:
                self.execute_node(node)
            except Exception as e:
                self.errors.append(str(e))
        
        # Print errors if any were found
        if self.errors:
            print("Errors detected:")
            for error in self.errors:
                print(f" - {error}")
        else:
            print("No errors detected!")

    def execute_node(self, node):
        """
        Executes a node based on its type.
        Each type is handled by its corresponding method.
        """
        if "type" not in node:
            raise ValueError(f"Missing 'type' in node: {node}")
    
        node_type = node["type"]
        
        if node_type == "CURSOR_DECLARATION":
            self.declare_cursor(node)
        elif node_type == "VARIABLE_DECLARATION":
            self.declare_variable(node)
        elif node_type == "SET_POSITION":
            self.check_set_position(node)
        elif node_type == "SET_COLOR":
            self.check_set_color(node)
        elif node_type == "SET_THICKNESS":
            self.check_set_thickness(node)
        elif node_type == "MOVE":
            self.check_move(node)
        elif node_type == "ROTATE":
            self.check_rotate(node)
        elif node_type == "DRAW_LINE":
            self.check_draw_line(node)
        elif node_type == "DRAW_CIRCLE":
            self.check_draw_circle(node)
        elif node_type == "DRAW_SQUARE":
            self.check_draw_square(node)
        elif node_type == "DRAW_TRIANGLE":
            self.check_draw_triangle(node)
        elif node_type == "DRAW_RECTANGLE":
            self.check_draw_rectangle(node)
        elif node_type == "CONDITION":
            self.check_condition(node)
        elif node_type == "DRAW_POINT":
            self.check_draw_point(node)
        elif node_type == "DRAW_ARC":
            self.check_draw_arc(node)
        elif node_type == "VARIABLE_UPDATE":
            self.update_variable(node)
        elif node_type == "FOR_LOOP":
            self.check_for_loop(node)
        elif node_type == "WHILE_LOOP":
            self.check_while_loop(node)
        elif node_type == "IF_STATEMENT":
            self.check_if_statement(node)
        elif node_type == "FUNCTION_CALL":
            self.check_function_call(node)
        elif node_type == "BLOCK":
            self.check_block(node)
        else:
            raise ValueError(f"Unknown node type: {node_type}")
        
    # --- Utility Functions ---
    def extract_numeric_value(self, value):
        """
        Extracts a numeric value from a 'VALUE' node in the AST.
        Converts the value to an integer if it is a string.
        """
        if isinstance(value, dict) and value.get("type") == "VALUE":
            raw_value = value.get("value")
            try:
                return int(raw_value)  # Convert to integer
            except ValueError:
                raise ValueError(f"Invalid numeric value: {raw_value}")
        else:
            raise ValueError(f"Expected a numeric value, got: {value}")
            
    def extract_value(self, value_node):
        """
        Extracts the value from a node.
        Handles both constants and variables.
        """
        if not isinstance(value_node, dict) or "type" not in value_node:
            self.errors.append(f"Invalid value node: {value_node}")
            print(f"Debug: Invalid value node encountered: {value_node}")
            return None

        if value_node["type"] == "VALUE":
            try:
                # Check if the value is a variable name
                if isinstance(value_node["value"], str) and value_node["value"].isalpha():
                    if value_node["value"] in self.variables:
                        return self.variables[value_node["value"]]
                    else:
                        self.errors.append(f"Variable '{value_node['value']}' is not declared.")
                        return None
                return int(value_node["value"])  # Convert to integer
            except ValueError:
                self.errors.append(f"Invalid value for VALUE type: {value_node['value']}")
                print(f"Debug: ValueError on converting value {value_node['value']} to int.")
                return None

        elif value_node["type"] == "VARIABLE" and value_node["name"] in self.variables:
            return self.variables[value_node["name"]]
        else:
            self.errors.append(f"Unknown value type: {value_node}")
            print(f"Debug: Unknown value type encountered: {value_node}")
            return None
            
    # --- Specific Validations ---
    def check_set_position(self, node):
        """
        Validates the 'setPosition' command for a cursor.
        Ensures the cursor exists and the coordinates are integers.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            x = self.extract_value(node["x"])
            y = self.extract_value(node["y"])
            if not isinstance(x, int) or not isinstance(y, int):
                self.errors.append(f"Position values for cursor '{cursor_name}' must be integers.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_point(self, node):
        """
        Validates the 'drawPoint' command.
        Ensures the cursor exists.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

    def check_rotate(self, node):
        """
        Validates the 'rotate' command for a cursor.
        Ensures the cursor exists and the angle is an integer.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            angle = self.extract_value(node["angle"])
            if not isinstance(angle, int):
                self.errors.append(f"Rotation angle for cursor '{cursor_name}' must be an integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_set_thickness(self, node):
        """
        Validates the 'setThickness' command for a cursor.
        Ensures the cursor exists and the thickness is a positive integer.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            thickness = self.extract_numeric_value(node["thickness"])
            if thickness <= 0:
                self.errors.append(f"Thickness for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def declare_cursor(self, node):
        """
        Handles the declaration of a cursor.
        Ensures the cursor name is unique and initializes its properties.
        """
        cursor_name = node.get("name")
        if not cursor_name:
            self.errors.append("Missing cursor name in CURSOR_DECLARATION.")
            return

        if cursor_name in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is already declared.")
        else:
            # Initialize default properties for the cursor
            self.cursors[cursor_name] = {
                "position": (0, 0),
                "color": (0, 0, 0, 255),  # Default color: black (RGBA)
                "thickness": 1           # Default thickness
            }

    def check_move(self, node):
        """
        Validates the 'move' command for a cursor.
        Ensures the cursor exists and the distance is a positive integer.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            distance = self.extract_value(node["distance"])
            if distance <= 0:
                self.errors.append(f"Distance for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))
            
    def check_condition(self, condition):
        """
        Validates a condition node.
        Compares left and right values using the specified operator.
        """
        left = self.extract_value(condition["left"])
        right = self.extract_value(condition["right"])
        operator = condition["operator"]

        # Map TokenType operators to Python operations
        if operator == TokenType.EQUAL:
            return left == right
        elif operator == TokenType.NOT_EQUAL:
            return left != right
        elif operator == TokenType.LESS_THAN:
            return left < right
        elif operator == TokenType.GREATER_THAN:
            return left > right
        elif operator == TokenType.LESS_EQUAL:
            return left <= right
        elif operator == TokenType.GREATER_EQUAL:
            return left >= right
        else:
            raise ValueError(f"Invalid operator in condition: {operator}")

    def validate_expression(self, expr, context=""):
        """
        Validates an expression node.
        Ensures the structure and values are correct.
        """
        if not isinstance(expr, dict):
            self.errors.append(f"{context} is not a valid expression: {expr}")
            return

        if expr["type"] == "VALUE":
            # Check if 'value' is a string or integer
            if not isinstance(expr["value"], (str, int)):
                self.errors.append(f"{context} contains an invalid VALUE: {expr}")
        elif expr["type"] == "EXPRESSION":
            # Handle nested expressions
            self.validate_expression(expr["left"], context="Left operand")
            self.validate_expression(expr["right"], context="Right operand")
        else:
            self.errors.append(f"{context} contains an unsupported expression type: {expr['type']}")

    def check_draw_line(self, node):
        """
        Validates the 'drawLine' command.
        Ensures the cursor exists and the length is a positive integer.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            length = self.extract_value(node["length"])
            if length <= 0:
                self.errors.append(f"Line length for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_circle(self, node):
        """
        Validates the 'drawCircle' command.
        Ensures the cursor exists and the radius is positive.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            radius = self.extract_value(node["radius"])
            if radius <= 0:
                self.errors.append(f"Circle radius for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_square(self, node):
        """
        Validates the 'drawSquare' command.
        Ensures the cursor exists and the size is positive.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            size = self.extract_value(node["side_length"])
            if size <= 0:
                self.errors.append(f"Square size for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_set_color(self, node):
        """
        Validates the 'setColor' command.
        Ensures the cursor exists and the color is valid.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
        else:
            color = node.get("color")
            if not isinstance(color, str):
                self.errors.append(f"Invalid color '{color}' for cursor '{cursor_name}'.")

    def check_draw_arc(self, node):
        """
        Validates the 'drawArc' command.
        Ensures the cursor exists, the radius is positive, and the angle is valid.
        """
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            radius = self.extract_value(node["radius"])
            angle = self.extract_value(node["angle"])
            if radius <= 0:
                self.errors.append(f"Arc radius for cursor '{cursor_name}' must be a positive integer.")
            if not isinstance(angle, int):
                self.errors.append(f"Arc angle for cursor '{cursor_name}' must be an integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def declare_variable(self, node):
        """
        Declares a new variable.
        Ensures the name is unique and the value is valid.
        """
        var_name = node.get("name")
        if not var_name:
            self.errors.append("Variable declaration missing variable name.")
            return

        if var_name in self.variables:
            self.errors.append(f"Variable '{var_name}' is already declared.")
            return

        var_value_node = node.get("value")
        if not var_value_node or var_value_node["type"] != "VALUE":
            self.errors.append(f"Invalid value in declaration of variable '{var_name}'.")
            return

        var_value = self.extract_value(var_value_node)
        if var_value is None:
            self.errors.append(f"Unable to extract value for variable '{var_name}'.")
            return

        self.variables[var_name] = var_value

    def update_variable(self, node):
        """
        Updates an existing variable.
        Handles increment, decrement, and assignment operations.
        """
        var_name = node.get("name")
        if not var_name:
            self.errors.append("Update step missing variable name.")
            return

        if var_name not in self.variables:
            self.errors.append(f"Variable '{var_name}' is not declared.")
            return

        current_value = self.variables.get(var_name)
        if current_value is None:
            self.errors.append(f"Variable '{var_name}' has no assigned value.")
            return

        operator = node.get("operator")
        value_node = node.get("value", {"type": "VALUE", "value": 1})  

        update_value = self.extract_value(value_node)
        if update_value is None:
            self.errors.append(f"Invalid update value for variable '{var_name}'.")
            return

        try:
            if operator == TokenType.PLUS_EQUAL:
                self.variables[var_name] += update_value
            elif operator == TokenType.MINUS_EQUAL:
                self.variables[var_name] -= update_value
            elif operator == TokenType.PLUS_PLUS:
                self.variables[var_name] += 1
            elif operator == TokenType.MINUS_MINUS:
                self.variables[var_name] -= 1
            else:
                self.errors.append(f"Unknown update operator '{operator}' for variable '{var_name}'.")
        except TypeError as e:
            self.errors.append(f"Error in update step of FOR_LOOP: {str(e)}")
            

    def check_block(self, node):
        """
        Validates a BLOCK node.
        Ensures it has a 'statements' key and that the statements are well-formed.
        """
        if "statements" not in node or not isinstance(node["statements"], list):
            self.errors.append("Each 'BLOCK' must have a 'statements' key as a list.")
            return

        # Check if each element in 'statements' is a list
        for statement_list in node["statements"]:
            if not isinstance(statement_list, list):
                self.errors.append("Each 'statements' entry in BLOCK must be a list.")
                return

            # Validate each instruction in the list
            for statement in statement_list:
                if not isinstance(statement, dict) or "type" not in statement:
                    self.errors.append(f"Invalid statement in BLOCK: {statement}")
                else:
                    # Execute or validate the statement
                    self.execute_node(statement)

    def check_while_loop(self, node):
        """
        Validates a WHILE_LOOP node.
        Ensures the condition and body are well-defined.
        """
        # Check the condition structure
        condition = node.get("condition")
        if not condition or "type" not in condition or condition["type"] != "CONDITION":
            self.errors.append("Missing or invalid condition in WHILE_LOOP.")
            return
        
        left = self.extract_value(condition["left"])
        right = self.extract_value(condition["right"])
        operator = condition["operator"]

        # Ensure the operator is a valid TokenType
        if not isinstance(operator, TokenType):
            self.errors.append(f"Invalid operator in condition: {operator}")
            return
        
        # Check the loop body
        body = node.get("body", {})
        if body.get("type") != "BLOCK":
            self.errors.append("WHILE_LOOP body must be a BLOCK.")
            return
        
        for statement in body.get("statements", []):
            if not isinstance(statement, list):
                self.errors.append("Each 'statements' entry in BLOCK must be a list.")
            else:
                for stmt in statement:
                    self.execute_node(stmt)

    def check_for_loop(self, node):
        """
        Validates a FOR_LOOP node.
        Ensures initialization, condition, update, and body are properly defined.
        """
        init = node.get("init")
        if not init or init["type"] != "VARIABLE_DECLARATION":
            self.errors.append("Invalid or missing initialization in FOR_LOOP.")
            return
        self.declare_variable(init)

        condition = node.get("condition")
        if not condition or condition["type"] != "CONDITION":
            self.errors.append("Missing or invalid condition in FOR_LOOP.")
            return

        left = self.extract_value(condition["left"])
        right = self.extract_value(condition["right"])
        operator = condition["operator"]

        if left is None or right is None:
            self.errors.append("Invalid condition in FOR_LOOP.")
            return

        if not isinstance(operator, TokenType):
            self.errors.append(f"Invalid operator in condition: {operator}")
            return

        update = node.get("update")
        if not update or update["type"] != "VARIABLE_UPDATE":
            self.errors.append("Invalid or missing update in FOR_LOOP.")
            return

        self.update_variable(update)

        body = node.get("body", {})
        if body.get("type") != "BLOCK":
            self.errors.append("FOR_LOOP body must be a BLOCK.")
            return

        for statement in body.get("statements", []):
            if not isinstance(statement, list):
                self.errors.append("Each 'statements' entry in BLOCK must be a list.")
            else:
                for stmt in statement:
                    self.execute_node(stmt)

    def check_if_statement(self, node):
        """
        Validates an IF_STATEMENT node.
        Ensures the condition, true_block, and false_block (if present) are valid.
        """
        # Ensure the condition field is present and is of type CONDITION
        if "condition" not in node or node["condition"]["type"] != "CONDITION":
            self.errors.append(f"Missing or invalid condition in IF_STATEMENT: {node}")
            return
        
        # Validate the condition
        self.check_condition(node["condition"])
        
        # Validate the true_block and false_block if they exist
        if "true_block" in node and node["true_block"]:
            self.check_block(node["true_block"])
        if "false_block" in node and node["false_block"]:
            self.check_block(node["false_block"])

            
ast_1 = [
    {"type": "CURSOR_DECLARATION", "name": "mainCursor"},
    {
        "type": "SET_POSITION",
        "cursor": "mainCursor",
        "x": {"type": "VALUE", "value": "10"},
        "y": {"type": "VALUE", "value": "20"}
    }
]

ast_2 = [
    {
        "type": "VARIABLE_DECLARATION",
        "var_type": "int",
        "name": "i",
        "value": {"type": "VALUE", "value": "10"}
    },
    {"type": "VARIABLE_UPDATE", "name": "i", "operator": "+=", "value": {"type": "VALUE", "value": "10"}},
    {"type": "VARIABLE_UPDATE", "name": "i", "operator": "-=", "value": {"type": "VALUE", "value": "3"}}
]

ast_3 = [
    {
        "type": "VARIABLE_DECLARATION",
        "var_type": "int",
        "name": "counter",
        "value": {"type": "VALUE", "value": "0"}
    },
    {
    "type": "CURSOR_DECLARATION",
    "name": "myCursor"
    },
    {
        "type": "WHILE_LOOP",
        "condition": {
            "type": "CONDITION",
            "left": {"type": "VALUE", "value": "12"},
            "operator": TokenType.LESS_THAN,
            "right": {"type": "VALUE", "value": "10"}
        },
        "body": {
            "type": "BLOCK",
            "statements": [
                [
                    {
                        "type": "DRAW_LINE",
                        "cursor": "myCursor",
                        "length": {"type": "VALUE", "value": "5"}
                    },
                    {
                        "type": "VARIABLE_UPDATE",
                        "name": "counter",
                        "operator": TokenType.PLUS_PLUS,
                        "value": {"type": "VALUE", "value": "1"}
                    }
                ]
            ]
        }
    }
]

complex_ast = [
    {
        "type": "IF_STATEMENT",
        "condition": {
            "type": "CONDITION",
            "left": {"type": "VALUE", "value": "i"},
            "operator": "EQUAL",  # Remplacement par une chaîne simple
            "right": {"type": "VALUE", "value": "15"}
        },
        "true_block": {
            "type": "BLOCK",
            "statements": [
            [
                {"type": "CURSOR_DECLARATION", "name": "myCursor"}
            ]
            ]
        },
        "false_block": None
    }
]



interpreter = Interpreter(ast_3)
interpreter.execute()