from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def parse_and_interpret(code):
    """
    Prend un code Draw++, le parse et le transmet à l'interpréteur pour le vérifier.
    """
    print("Parsing and interpreting the following code:")
    print(code)
    print("=" * 50)

    # Étape 1 : Tokenize le code
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(token)
    print("=" * 50)

    # Étape 2 : Parse les tokens pour générer un AST
    parser = Parser(tokens)
    syntax_tree = parser.parse()
    print("Generated AST:")
    from pprint import pprint
    pprint(syntax_tree)
    print("=" * 50)

    # Étape 3 : Vérifie l'AST avec l'interpréteur
    interpreter = Interpreter(syntax_tree)
    interpreter.execute()

    # Étape 4 : Afficher les erreurs
    if interpreter.errors:
        print("Errors detected:")
        for error in interpreter.errors:
            print(f" - {error}")
    else:
        print("No errors detected!")

# Exemple de code à tester
code = """
cursor myCursor;
myCursor.setPosition(10, 20);
myCursor.setColor(red);
myCursor.setThickness(10);

int i = 10;

for(int j = 0; i <= 10; i++){
    myCursor.setColor(red);
    myCursor.setThickness(5);
}

while(i  10){
    myCursor.setPosition(10, 20);
    myCursor.setColor(red);
    myCursor.setThickness(10);
}

"""

# Appel de la fonction
parse_and_interpret(code)