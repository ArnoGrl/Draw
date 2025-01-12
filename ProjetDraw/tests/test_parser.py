from lexer import Lexer
from parser import Parser

def test_parser():
    # Échantillons de code Draw++ à tester
    tests = [
        {
            "description": "Déclaration de curseur",
            "code": "cursor myCursor;",
            "expected_ast": [{"type": "CURSOR_DECLARATION", "name": "myCursor"}],
        },
        {
            "description": "Positionnement du curseur",
            "code": "myCursor.setPosition(10, 20);",
            "expected_ast": [
                {
                    "type": "SET_POSITION",
                    "cursor": "myCursor",
                    "x": {"type": "VALUE", "value": "10"},
                    "y": {"type": "VALUE", "value": "20"},
                }
            ],
        },
        {
            "description": "Déclaration de variable",
            "code": "int i = 10;",
            "expected_ast": [
                {
                    "type": "VARIABLE_DECLARATION",
                    "var_type": "int",
                    "name": "i",
                    "value": {"type": "VALUE", "value": "10"},
                }
            ],
        },
        {
            "description": "Boucle for simple",
            "code": """
            for (int i = 0; i <= 10; i++) {
                myCursor.drawCircle(10);
            }
            """,
            "expected_ast": [
                {
                    "type": "FOR_LOOP",
                    "init": {
                        "type": "VARIABLE_DECLARATION",
                        "var_type": "int",
                        "name": "i",
                        "value": {"type": "VALUE", "value": "0"},
                    },
                    "condition": {
                        "type": "CONDITION",
                        "left": {"type": "VALUE", "value": "i"},
                        "operator": "LESS_EQUAL",
                        "right": {"type": "VALUE", "value": "10"},
                    },
                    "update": {
                        "type": "VARIABLE_UPDATE",
                        "name": "i",
                        "operator": "PLUS_PLUS",
                    },
                    "body": {
                        "type": "BLOCK",
                        "statements": [
                            [
                                {
                                    "type": "DRAW_CIRCLE",
                                    "cursor": "myCursor",
                                    "radius": {"type": "VALUE", "value": "10"},
                                }
                            ]
                        ],
                    },
                }
            ],
        },
    ]

    # Exécution des tests
    for test in tests:
        print(f"Running test: {test['description']}")
        code = test["code"]
        expected_ast = test["expected_ast"]

        try:
            # Étape 1 : Lexer
            lexer = Lexer(source_code=code)
            tokens = lexer.tokenize()
            print("Tokens generated successfully.")

            # Étape 2 : Parser
            parser = Parser(tokens=tokens)
            ast = parser.parse()
            print("AST generated successfully:")
            print(ast)

            # Comparaison avec l'AST attendu
            if ast == expected_ast:
                print("Test passed: Generated AST matches expected AST.")
            else:
                print("Test failed: Generated AST does not match expected AST.")
                print("Expected:")
                print(expected_ast)
                print("Got:")
                print(ast)

        except Exception as e:
            print(f"Test failed with an error: {e}")

        print("-" * 50)


if __name__ == "__main__":
    test_parser()