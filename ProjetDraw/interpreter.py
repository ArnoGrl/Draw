from lexer import Lexer
from utils.tokens import Token
from utils.tokens import TokenType
from parser import Parser



class Interpreter:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        self.variables = {}  # Stocker les variables et leurs valeurs
        self.cursors = {}    # Stocker les curseurs définis
        self.errors = []     # Liste des erreurs détectées

    def execute(self):
        """
        Parcourt l'AST et vérifie chaque nœud.
        """
        for node in self.syntax_tree:
            try:
                self.execute_node(node)
            except Exception as e:
                self.errors.append(str(e))
        
        # Affiche les erreurs à la fin
        if self.errors:
            print("Errors detected:")
            for error in self.errors:
                print(f" - {error}")
        else:
            print("No errors detected!")

    def execute_node(self, node):
        """
        Vérifie un nœud en fonction de son type.
        """
        if "type" not in node:
            raise ValueError(f"Missing 'type' in node: {node}")
    
        node_type = node["type"]
        
        if node_type == "CURSOR_DECLARATION":
            self.declare_cursor(node)
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
        elif node_type == "VARIABLE_DECLARATION":
            self.declare_variable(node)
        elif node_type == "CURSOR_DECLARATION":
            self.declare_cursor(node)
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


    # --- Fonctions utilitaires ---
    def extract_numeric_value(self, value):
        """
        Extrait une valeur numérique des nœuds de type 'VALUE' dans l'AST.
        Si la valeur est une chaîne, elle est convertie en entier.
        """
        if isinstance(value, dict) and value.get("type") == "VALUE":
            raw_value = value.get("value")
            try:
                return int(raw_value)  # Convertir en entier
            except ValueError:
                raise ValueError(f"Invalid numeric value: {raw_value}")
        else:
            raise ValueError(f"Expected a numeric value, got: {value}")

    # --- Vérifications spécifiques ---
    def check_set_position(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            x = self.extract_numeric_value(node["x"])
            y = self.extract_numeric_value(node["y"])
            if not isinstance(x, int) or not isinstance(y, int):
                self.errors.append(f"Position values for cursor '{cursor_name}' must be integers.")
        except ValueError as e:
            self.errors.append(str(e))


    def check_set_thickness(self, node):
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
        Gère la déclaration d'un curseur.
        """
        cursor_name = node.get("name")
        if not cursor_name:
            self.errors.append("Missing cursor name in CURSOR_DECLARATION.")
            return

        if cursor_name in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is already declared.")
        else:
            # Initialisez les propriétés par défaut du curseur
            self.cursors[cursor_name] = {
                "position": (0, 0),
                "color": (0, 0, 0, 255),  # Couleur noire par défaut (RGBA)
                "thickness": 1           # Épaisseur par défaut
            }

    def check_move(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            distance = self.extract_numeric_value(node["distance"])
            if distance <= 0:
                self.errors.append(f"Distance for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_condition(self, node):
        """
        Valide une condition dans un IF_STATEMENT ou une boucle.
        """
        if "left" not in node or "operator" not in node or "right" not in node:
            self.errors.append(f"Invalid condition node: {node}")
            return
        
        # Validez les parties gauche et droite
        self.validate_expression(node["left"], context="Condition left operand")
        self.validate_expression(node["right"], context="Condition right operand")

        # Validez l'opérateur
        if node["operator"] not in {"EQUAL", "LESS_THAN", "GREATER_THAN", "LESS_EQUAL", "GREATER_EQUAL", "NOT_EQUAL"}:
            self.errors.append(f"Invalid operator in condition: {node['operator']}")

    def validate_expression(self, expr, context=""):
        """
        Valide une expression dans le nœud CONDITION ou ailleurs.
        """
        if not isinstance(expr, dict):
            self.errors.append(f"{context} is not a valid expression: {expr}")
            return

        if expr["type"] == "VALUE":
            # Vérifiez si 'value' est une chaîne ou un entier
            if not isinstance(expr["value"], (str, int)):
                self.errors.append(f"{context} contains an invalid VALUE: {expr}")
        elif expr["type"] == "EXPRESSION":
            # Gérer les expressions complexes
            self.validate_expression(expr["left"], context="Left operand")
            self.validate_expression(expr["right"], context="Right operand")
        else:
            self.errors.append(f"{context} contains an unsupported expression type: {expr['type']}")

    def check_draw_line(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            length = self.extract_numeric_value(node["length"])
            if length <= 0:
                self.errors.append(f"Line length for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_circle(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            radius = self.extract_numeric_value(node["radius"])
            if radius <= 0:
                self.errors.append(f"Circle radius for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_square(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            size = self.extract_numeric_value(node["size"])
            if size <= 0:
                self.errors.append(f"Square size for cursor '{cursor_name}' must be a positive integer.")
        except ValueError as e:
            self.errors.append(str(e))

    def check_draw_arc(self, node):
        cursor_name = node["cursor"]
        if cursor_name not in self.cursors:
            self.errors.append(f"Cursor '{cursor_name}' is not declared.")
            return

        try:
            radius = self.extract_numeric_value(node["radius"])
            angle = self.extract_numeric_value(node["angle"])
            if radius <= 0:
                self.errors.append(f"Arc radius for cursor '{cursor_name}' must be a positive integer.")
            if not isinstance(angle, int):
                self.errors.append(f"Arc angle for cursor '{cursor_name}' must be an integer.")
        except ValueError as e:
            self.errors.append(str(e))
    def declare_variable(self, node):
        var_name = node["name"]
        value = self.extract_value(node["value"])
        if var_name in self.variables:
            self.errors.append(f"Variable '{var_name}' is already declared.")
        else:
            self.variables[var_name] = value

    def update_variable(self, node):
        var_name = node["name"]
        if var_name not in self.variables:
            self.errors.append(f"Variable '{var_name}' is not declared.")
        else:
            operator = node["operator"]
            value = self.extract_value(node["value"])
            if operator == "+=":
                self.variables[var_name] += value
            elif operator == "-=":
                self.variables[var_name] -= value
            else:
                self.errors.append(f"Unknown operator '{operator}' for variable '{var_name}'.")

    def check_for_loop(self, node):
        init = node["init"]
        condition = node["condition"]
        update = node["update"]
        body = node["body"]["statements"]

        # Vérifie la déclaration de la variable
        if init["name"] not in self.variables:
            raise ValueError(f"Variable '{init['name']}' is not declared.")

        # Vérifie le corps de la boucle
        for statement in body:
            self.execute_node(statement)

    def check_block(self, node):
        """
        Vérifie qu'un bloc (BLOCK) est correctement formé.
        """
        if "statements" not in node or not isinstance(node["statements"], list):
            self.errors.append("Each 'BLOCK' must have a 'statements' key as a list.")
            return

        # Vérifie que chaque élément dans 'statements' est une liste
        for statement_list in node["statements"]:
            if not isinstance(statement_list, list):
                self.errors.append("Each 'statements' entry in BLOCK must be a list.")
                return

            # Vérifie chaque instruction dans la liste
            for statement in statement_list:
                if not isinstance(statement, dict) or "type" not in statement:
                    self.errors.append(f"Invalid statement in BLOCK: {statement}")
                else:
                    # Exécute ou vérifie chaque instruction
                    self.execute_node(statement)

    def check_for_loop(self, node):
        """
        Vérifie un nœud de type FOR_LOOP.
        """
        init = node["init"]
        condition = node["condition"]
        update = node["update"]
        body = node["body"]

        # Vérifie la déclaration de la variable
        self.execute_node(init)

        # Vérifie la condition
        if "left" not in condition or "operator" not in condition or "right" not in condition:
            self.errors.append("Invalid condition in FOR_LOOP.")
        
        # Vérifie le corps de la boucle (le bloc)
        if body["type"] == "BLOCK":
            self.execute_node(body)
        else:
            self.errors.append("FOR_LOOP body must be a BLOCK.")

    def check_if_statement(self, node):
        """
        Valide un nœud IF_STATEMENT.
        """
        # Vérifie que le champ condition est présent et de type CONDITION
        if "condition" not in node or node["condition"]["type"] != "CONDITION":
            self.errors.append(f"Missing or invalid condition in IF_STATEMENT: {node}")
            return
        
        # Vérifie la condition
        self.check_condition(node["condition"])
        
        # Vérifie les blocs true_block et false_block
        if "true_block" in node and node["true_block"]:
            self.check_block(node["true_block"])
        if "false_block" in node and node["false_block"]:
            self.check_block(node["false_block"])

syntax_tree = [
    {"type": "CURSOR_DECLARATION", "name": "myCursor"},
    {"type": "SET_POSITION", "cursor": "myCursor", "x": {"type": "VALUE", "value": 10}, "y": {"type": "VALUE", "value": 20}},
    {"type": "SET_COLOR", "cursor": "myCursor", "color": "red"},
    {"type": "SET_THICKNESS", "cursor": "myCursor", "thickness": {"type": "VALUE", "value": 5}},
    {"type": "WHILE_LOOP",
     "condition": {"left": {"type": "VALUE", "value": "x"}, "operator": TokenType.GREATER_THAN, "right": {"type": "VALUE", "value": 0}},
     "body": {"statements": [{"type": "SET_POSITION", "cursor": "myCursor", "x": {"type": "VALUE", "value": 0}, "y": {"type": "VALUE", "value": 0}}]}
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



interpreter = Interpreter(complex_ast)
interpreter.execute()