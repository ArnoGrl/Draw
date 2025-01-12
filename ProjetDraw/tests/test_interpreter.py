from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def parse_and_interpret(code):
    """
    Takes a Draw++ code snippet, parses it, and passes it to the interpreter for execution.
    Includes detailed debug output for tokens, AST, and errors.
    """
    print("Parsing and interpreting the following code:")
    print(code)
    print("=" * 50)

    # Step 1: Tokenize the code using the Lexer
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token in tokens:  # Display each token for debugging purposes
        print(token)
    print("=" * 50)

    # Step 2: Parse the tokens to generate an Abstract Syntax Tree (AST)
    parser = Parser(tokens)
    syntax_tree = parser.parse()
    print("Generated AST:")
    from pprint import pprint
    pprint(syntax_tree)  # Use pprint for a clearer hierarchical view of the AST
    print("=" * 50)

    # Step 3: Execute the AST using the Interpreter
    interpreter = Interpreter(syntax_tree)
    interpreter.execute()

    # Step 4: Display any interpreter errors
    if interpreter.errors:
        print("Errors detected:")
        for error in interpreter.errors:
            print(f" - {error}")  # Print each error for clarity
    else:
        print("No errors detected!")  # Confirm successful execution if no errors

# Example Draw++ code snippet to test
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