import subprocess
import unittest
import sys
import os

# Ajoute le chemin du répertoire parent pour trouver lexer.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from parser import Parser
from utils.tokens import TokenType
from lexer import Lexer



COLOR_MAP = {
    "aliceblue":           "(SDL_Color){240, 248, 255, 255}",
    "antiquewhite":        "(SDL_Color){250, 235, 215, 255}",
    "aqua":                "(SDL_Color){0, 255, 255, 255}",
    "aquamarine":          "(SDL_Color){127, 255, 212, 255}",
    "azure":               "(SDL_Color){240, 255, 255, 255}",
    "beige":               "(SDL_Color){245, 245, 220, 255}",
    "bisque":              "(SDL_Color){255, 228, 196, 255}",
    "black":               "(SDL_Color){0, 0, 0, 255}",
    "blanchedalmond":      "(SDL_Color){255, 235, 205, 255}",
    "blue":                "(SDL_Color){0, 0, 255, 255}",
    "blueviolet":          "(SDL_Color){138, 43, 226, 255}",
    "brown":               "(SDL_Color){165, 42, 42, 255}",
    "burlywood":           "(SDL_Color){222, 184, 135, 255}",
    "cadetblue":           "(SDL_Color){95, 158, 160, 255}",
    "chartreuse":          "(SDL_Color){127, 255, 0, 255}",
    "chocolate":           "(SDL_Color){210, 105, 30, 255}",
    "coral":               "(SDL_Color){255, 127, 80, 255}",
    "cornflowerblue":      "(SDL_Color){100, 149, 237, 255}",
    "cornsilk":            "(SDL_Color){255, 248, 220, 255}",
    "crimson":             "(SDL_Color){220, 20, 60, 255}",
    "cyan":                "(SDL_Color){0, 255, 255, 255}",
    "darkblue":            "(SDL_Color){0, 0, 139, 255}",
    "darkcyan":            "(SDL_Color){0, 139, 139, 255}",
    "darkgoldenrod":       "(SDL_Color){184, 134, 11, 255}",
    "darkgray":            "(SDL_Color){169, 169, 169, 255}",
    "darkgreen":           "(SDL_Color){0, 100, 0, 255}",
    "darkkhaki":           "(SDL_Color){189, 183, 107, 255}",
    "darkmagenta":         "(SDL_Color){139, 0, 139, 255}",
    "darkolivegreen":      "(SDL_Color){85, 107, 47, 255}",
    "darkorange":          "(SDL_Color){255, 140, 0, 255}",
    "darkorchid":          "(SDL_Color){153, 50, 204, 255}",
    "darkred":             "(SDL_Color){139, 0, 0, 255}",
    "darksalmon":          "(SDL_Color){233, 150, 122, 255}",
    "darkseagreen":        "(SDL_Color){143, 188, 143, 255}",
    "darkslateblue":       "(SDL_Color){72, 61, 139, 255}",
    "darkslategray":       "(SDL_Color){47, 79, 79, 255}",
    "darkturquoise":       "(SDL_Color){0, 206, 209, 255}",
    "darkviolet":          "(SDL_Color){148, 0, 211, 255}",
    "deeppink":            "(SDL_Color){255, 20, 147, 255}",
    "deepskyblue":         "(SDL_Color){0, 191, 255, 255}",
    "dimgray":             "(SDL_Color){105, 105, 105, 255}",
    "dodgerblue":          "(SDL_Color){30, 144, 255, 255}",
    "firebrick":           "(SDL_Color){178, 34, 34, 255}",
    "floralwhite":         "(SDL_Color){255, 250, 240, 255}",
    "forestgreen":         "(SDL_Color){34, 139, 34, 255}",
    "fuchsia":             "(SDL_Color){255, 0, 255, 255}",
    "gainsboro":           "(SDL_Color){220, 220, 220, 255}",
    "ghostwhite":          "(SDL_Color){248, 248, 255, 255}",
    "gold":                "(SDL_Color){255, 215, 0, 255}",
    "goldenrod":           "(SDL_Color){218, 165, 32, 255}",
    "gray":                "(SDL_Color){128, 128, 128, 255}",
    "green":               "(SDL_Color){0, 128, 0, 255}",
    "greenyellow":         "(SDL_Color){173, 255, 47, 255}",
    "honeydew":            "(SDL_Color){240, 255, 240, 255}",
    "hotpink":             "(SDL_Color){255, 105, 180, 255}",
    "indianred":           "(SDL_Color){205, 92, 92, 255}",
    "indigo":              "(SDL_Color){75, 0, 130, 255}",
    "ivory":               "(SDL_Color){255, 255, 240, 255}",
    "khaki":               "(SDL_Color){240, 230, 140, 255}",
    "lavender":            "(SDL_Color){230, 230, 250, 255}",
    "lavenderblush":       "(SDL_Color){255, 240, 245, 255}",
    "lawngreen":           "(SDL_Color){124, 252, 0, 255}",
    "lemonchiffon":        "(SDL_Color){255, 250, 205, 255}",
    "lightblue":           "(SDL_Color){173, 216, 230, 255}",
    "lightcoral":          "(SDL_Color){240, 128, 128, 255}",
    "lightcyan":           "(SDL_Color){224, 255, 255, 255}",
    "lightgoldenrodyellow":"(SDL_Color){250, 250, 210, 255}",
    "lightgreen":          "(SDL_Color){144, 238, 144, 255}",
    "lightgrey":           "(SDL_Color){211, 211, 211, 255}",
    "lightpink":           "(SDL_Color){255, 182, 193, 255}",
    "lightsalmon":         "(SDL_Color){255, 160, 122, 255}",
    "lightseagreen":       "(SDL_Color){32, 178, 170, 255}",
    "lightskyblue":        "(SDL_Color){135, 206, 250, 255}",
    "lightslategray":      "(SDL_Color){119, 136, 153, 255}",
    "lightsteelblue":      "(SDL_Color){176, 196, 222, 255}",
    "lightyellow":         "(SDL_Color){255, 255, 224, 255}",
    "lime":                "(SDL_Color){0, 255, 0, 255}",
    "limegreen":           "(SDL_Color){50, 205, 50, 255}",
    "linen":               "(SDL_Color){250, 240, 230, 255}",
    "magenta":             "(SDL_Color){255, 0, 255, 255}",
    "maroon":              "(SDL_Color){128, 0, 0, 255}",
    "mediumaquamarine":    "(SDL_Color){102, 205, 170, 255}",
    "mediumblue":          "(SDL_Color){0, 0, 205, 255}",
    "mediumorchid":        "(SDL_Color){186, 85, 211, 255}",
    "mediumpurple":        "(SDL_Color){147, 112, 219, 255}",
    "mediumseagreen":      "(SDL_Color){60, 179, 113, 255}",
    "mediumslateblue":     "(SDL_Color){123, 104, 238, 255}",
    "mediumspringgreen":   "(SDL_Color){0, 250, 154, 255}",
    "mediumturquoise":     "(SDL_Color){72, 209, 204, 255}",
    "mediumvioletred":     "(SDL_Color){199, 21, 133, 255}",
    "midnightblue":        "(SDL_Color){25, 25, 112, 255}",
    "mintcream":           "(SDL_Color){245, 255, 250, 255}",
    "mistyrose":           "(SDL_Color){255, 228, 225, 255}",
    "moccasin":            "(SDL_Color){255, 228, 181, 255}",
    "navajowhite":         "(SDL_Color){255, 222, 173, 255}",
    "navy":                "(SDL_Color){0, 0, 128, 255}",
    "oldlace":             "(SDL_Color){253, 245, 230, 255}",
    "olive":               "(SDL_Color){128, 128, 0, 255}",
    "olivedrab":           "(SDL_Color){107, 142, 35, 255}",
    "orange":              "(SDL_Color){255, 165, 0, 255}",
    "orangered":           "(SDL_Color){255, 69, 0, 255}",
    "orchid":              "(SDL_Color){218, 112, 214, 255}",
    "palegoldenrod":       "(SDL_Color){238, 232, 170, 255}",
    "palegreen":           "(SDL_Color){152, 251, 152, 255}",
    "paleturquoise":       "(SDL_Color){175, 238, 238, 255}",
    "palevioletred":       "(SDL_Color){219, 112, 147, 255}",
    "papayawhip":          "(SDL_Color){255, 239, 213, 255}",
    "peachpuff":           "(SDL_Color){255, 218, 185, 255}",
    "peru":                "(SDL_Color){205, 133, 63, 255}",
    "pink":                "(SDL_Color){255, 192, 203, 255}",
    "plum":                "(SDL_Color){221, 160, 221, 255}",
    "powderblue":          "(SDL_Color){176, 224, 230, 255}",
    "purple":              "(SDL_Color){128, 0, 128, 255}",
    "rebeccapurple":       "(SDL_Color){102, 51, 153, 255}",
    "red":                 "(SDL_Color){255, 0, 0, 255}",
    "rosybrown":           "(SDL_Color){188, 143, 143, 255}",
    "royalblue":           "(SDL_Color){65, 105, 225, 255}",
    "saddlebrown":         "(SDL_Color){139, 69, 19, 255}",
    "salmon":              "(SDL_Color){250, 128, 114, 255}",
    "sandybrown":          "(SDL_Color){244, 164, 96, 255}",
    "seagreen":            "(SDL_Color){46, 139, 87, 255}",
    "seashell":            "(SDL_Color){255, 245, 238, 255}",
    "sienna":              "(SDL_Color){160, 82, 45, 255}",
    "silver":              "(SDL_Color){192, 192, 192, 255}",
    "skyblue":             "(SDL_Color){135, 206, 235, 255}",
    "slateblue":           "(SDL_Color){106, 90, 205, 255}",
    "slategray":           "(SDL_Color){112, 128, 144, 255}",
    "snow":                "(SDL_Color){255, 250, 250, 255}",
    "springgreen":         "(SDL_Color){0, 255, 127, 255}",
    "steelblue":           "(SDL_Color){70, 130, 180, 255}",
    "tan":                 "(SDL_Color){210, 180, 140, 255}",
    "teal":                "(SDL_Color){0, 128, 128, 255}",
    "thistle":             "(SDL_Color){216, 191, 216, 255}",
    "tomato":              "(SDL_Color){255, 99, 71, 255}",
    "turquoise":           "(SDL_Color){64, 224, 208, 255}",
    "violet":              "(SDL_Color){238, 130, 238, 255}",
    "wheat":               "(SDL_Color){245, 222, 179, 255}",
    "white":               "(SDL_Color){255, 255, 255, 255}",
    "whitesmoke":          "(SDL_Color){245, 245, 245, 255}",
    "yellow":              "(SDL_Color){255, 255, 0, 255}",
    "yellowgreen":         "(SDL_Color){154, 205, 50, 255}"
}


#Fonction de génération de code C à partir de l'AST
def generate_c_code(ast):
    """Génère le code C à partir de l'AST fourni."""
    code = ["#include <stdio.h>", "#include <stdbool.h>", "#include \"C/include/draw_cursor.h\"","#include \"C/src/draw_cursor.c\"", "#include <SDL2/SDL.h>" "\n"]
    code.append("int main() { \n"
            "    SDL_Init(SDL_INIT_VIDEO);\n"
            "    SDL_Window *window = SDL_CreateWindow(\"Draw++ Test\", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);\n"
            "    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);\n")


    for node in ast:
        code.append(gerer_instruction(node))  # Génère chaque ligne d'instruction

    code.append("SDL_RenderPresent(renderer);")
    code.append("SDL_Delay(3000);")
    code.append("SDL_DestroyRenderer(renderer);")
    code.append("SDL_DestroyWindow(window);")
    code.append("SDL_Quit();")
    code.append("    return 0;")
    code.append("}")
    return "\n".join(code)


# Fonction pour gérer toutes les instructions du parser
# Fonction pour gérer toutes les instructions du parser
def gerer_instruction(instruction):

    #Gerer l'ast qui est sous forme de list 
    if isinstance(instruction, list):
        code = ""
        for instr in instruction:
            code += gerer_instruction(instr) + "\n"
        return code

    if instruction["type"] == "VARIABLE_DECLARATION":
        var_type = "int" if instruction["var_type"] == "INT" else "float"
        
        # instruction["value"] peut être un dict contenant "type" et "value"
        if isinstance(instruction["value"], dict) and instruction["value"]["type"] == "VALUE":
            code_value = instruction["value"]["value"]
        else:
            # Gérer d'autres cas selon la structure de 'instruction["value"]'
            code_value = instruction["value"] 
        
        return f"    {var_type} {instruction['name']} = {code_value};"
        
    # Condition
    elif instruction["type"] == "CONDITION":
        return gerer_condition(instruction)
    
    # Mise à jour de variable
    elif instruction["type"] == "VARIABLE_UPDATE":
        var_name = instruction["name"]
        operator = instruction["operator"]
        if operator == TokenType.PLUS_PLUS:  # Utilisation de TokenType
            return f"    {var_name}++;"
        elif operator == TokenType.MINUS_MINUS:  # Utilisation de TokenType
            return f"    {var_name}--;"
        elif operator == TokenType.PLUS_EQUAL:  # Utilisation de TokenType
            value = instruction["value"]["value"]
            return f"    {var_name} += {value};"
        elif operator == TokenType.MINUS_EQUAL:  # Utilisation de TokenType
            value = instruction["value"]["value"]
            return f"    {var_name} -= {value};"
    
    # Boucle while
    elif instruction["type"] == "WHILE_LOOP":
        condition = gerer_condition(instruction["condition"])
        code = f"    while ({condition}) {{\n"
        for statement in instruction["body"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"
        code += "    }"
        return code

    # Condition if
    elif instruction["type"] == "IF_STATEMENT":
        condition = gerer_condition(instruction["condition"])
        code = f"    if ({condition}) {{\n"
        for statement in instruction["true_block"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"
        code += "    }"
        if instruction["false_block"]:
            code += "    else {\n"
            for statement in instruction["false_block"]["statements"]:
                code += f"{gerer_instruction(statement)}\n"
            code += "    }"
        return code
    
    # Boucle for
    elif instruction["type"] == "FOR_LOOP":
        init = gerer_instruction(instruction["init"]).strip(";")
        condition = gerer_condition(instruction["condition"])
        update = gerer_instruction(instruction["update"]).strip(";")
        code = f"    for ({init}; {condition}; {update}) {{\n"
        for statement in instruction["body"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"
        code += "    }"
        return code

    # Dessin -- il faut prendre chaque instruction du parser pour la traiter et ensuite retourner la bonne fonction en C
    # Déclaration d'une position 
    elif instruction["type"] == "SET_POSITION":
        return f"    setPosition(&{instruction['cursor']}, {instruction['x']['value']}, {instruction['y']['value']});"

    elif instruction["type"] == "SET_COLOR":
        color_name = instruction["color"]  # par exemple "red", "blue", etc.

        # Récupérer la valeur C correspondante :
        if color_name in COLOR_MAP:
            color_value = COLOR_MAP[color_name]
        else:
            # Si la couleur n'est pas reconnue, on peut mettre une couleur par défaut
            color_value = "(SDL_Color){0, 0, 0, 255}"  # noir par défaut

        # Générer la ligne de code C
        return f"    setColor(&{instruction['cursor']}, {color_value});"
    
    # Déclaration d'une épaisseur
    elif instruction["type"] == "SET_THICKNESS":
        return f"    setThickness(&{instruction['cursor']}, {instruction['thickness']});"
    
    # Déclaration de la rotation 
    elif instruction["type"] == "ROTATE":
        return f"    rotate(&{instruction['cursor']}, {instruction['angle']['value']});"
    
    # Dessin d'une ligne
    elif instruction["type"] == "DRAW_LINE":
        return f"    drawLine(renderer, &{instruction['cursor']}, {instruction['length']['value']});"

    elif instruction["type"] == "CURSOR_DECLARATION":
        # Si c'est un curseur, on génère "Cursor monCurseur = createCursor();"
        return f"    Cursor {instruction['name']} = createCursor();"
    
    # Dessin d'un point
    elif instruction["type"] == "DRAW_POINT":
        return f"    drawPoint(renderer, &{instruction['cursor']});"
    
    # Dessin d'un arc
    elif instruction["type"] == "DRAW_ARC":
        return f"    drawArc(renderer, &{instruction['cursor']}, {instruction['radius']['value']}, {instruction['angle']['value']});"

    # Dessin d'un cercle
    elif instruction["type"] == "DRAW_CIRCLE":
        return f"    drawCircle(renderer, &{instruction['cursor']}, {instruction['radius']['value']});"
        
    # Dessin d'un carré
    elif instruction["type"] == "DRAW_SQUARE":
        return f"    drawSquare(renderer, &{instruction['cursor']}, {instruction['side_length']['value']});"
        
    # Instructions non gérées
    raise ValueError(f"Instruсtion inconnue : {instruction}")



    
# Fonction pour gérer les conditions
def gerer_condition(condition):
    left = condition["left"]["value"]   
    right = condition["right"]["value"]
    operator = condition["operator"].name
    operators_map = {
        "GREATER_THAN": ">",
        "LESS_THAN": "<",
        "GREATER_EQUAL": ">=",
        "LESS_EQUAL": "<=",
        "EQUAL": "==",
        "NOT_EQUAL": "!=",
    

        
    }
    return f"{left} {operators_map[operator]} {right}"


# Sauvegarde dans un fichier .c
def save_to_file(filename, content):
    """Sauvegarde le contenu dans un fichier."""
    with open(filename, "w") as f:
        f.write(content)


# Compilation en .exe avec GCC 
def compile_c_to_exe(c_file, exe_file):
    """Compile le fichier C en un exécutable avec GCC."""
    try:
        subprocess.run([
        "gcc", c_file, "-o", exe_file, "-lSDL2", "-lm"
        ], check=True)

        print(f"Compilation réussie : {exe_file}")
    except subprocess.CalledProcessError as e:
        print("Erreur de compilation :", e)


# Classe de test pour parser le code et générer l'AST 
class TestParser(unittest.TestCase):
    def parse_code(self, code):
        """Helper function to parse code and return the syntax tree."""
        lexer = Lexer(code)  # Instancie le Lexer
        tokens = lexer.tokenize()
        parser = Parser(tokens)  # Instancie le Parser
        return parser.parse()

    def test_block_with_two_statements(self):
        code = """
        cursor myCursor;
        cursor Cursor;
        int i = 0;
        int j = 50;
        int g = 100;
        int a = 25;
        int b = 50;
        while(i < 100){
            myCursor.setPosition(j,g);
            Cursor.setPosition(a,b);
            j += 5
            g += 2
            a += 3
            b += 8
            myCursor.setColor(red);
            Cursor.setColor(blue);

            myCursor.drawLine(10);

            myCursor.rotate(90);

            myCursor.drawPoint();

            myCursor.drawArc(50, 90);

            myCursor.drawCircle(50);

            myCursor.drawSquare(50);

            Cursor.drawLine(10);

            Cursor.rotate(90);

            Cursor.drawPoint();

            Cursor.drawArc(50, 90);

            Cursor.drawCircle(50);

            Cursor.drawSquare(50);
            
            i++
        }
        """
        syntax_tree = self.parse_code(code)
        return syntax_tree


# Programme principal
if __name__ == "__main__":
    # Étape 1 : Parser le code pour générer l'AST et l'afficher 
    parser = TestParser()
    ast = parser.test_block_with_two_statements()
    print("\nAST généré avec succès :")
    print(ast)



    # Étape 2 : Générer le code C
    c_code = generate_c_code(ast)
    print("\nCode C généré :")
    print(c_code)

    # Étape 3 : Sauvegarder dans un fichier
    c_filename = "output.c"
    save_to_file(c_filename, c_code)

    # Étape 4 : Compiler en exécutable
    exe_filename = "output.exe"
    compile_c_to_exe(c_filename, exe_filename)