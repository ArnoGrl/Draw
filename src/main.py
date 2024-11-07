# main.py
from src.parser import Parser
from src.interpreter import Interpreter

def main():
    # Exemple d'instructions draw++ à analyser
    instructions = """
    cursor myCursor;
    myCursor.setPosition(100, 200);
    myCursor.setColor("blue");
    myCursor.drawLine(100);
    animate(myCursor);
    """
    
    parser = Parser()
    commands = parser.parse(instructions)
    
    interpreter = Interpreter()
    interpreter.execute(commands)

if __name__ == "__main__":
    main()
