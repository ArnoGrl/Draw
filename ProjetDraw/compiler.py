import subprocess
import unittest
import sys
import os


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

# Function to generate C code from the AST
def generate_c_code(ast):
    """
    Generates C code from the provided AST.
    - Sets up SDL for rendering.
    - Processes each AST node into C instructions.
    """
    # Required headers and SDL initialization
    code = [
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#include \"C/include/draw_cursor.h\"",
        "#include \"C/src/draw_cursor.c\"",
        "#include <SDL2/SDL.h>\n"
    ]

    # Main function setup with SDL initialization
    code.append(
        "int main() {\n"
        "    SDL_Init(SDL_INIT_VIDEO);\n"
        "    SDL_Window *window = SDL_CreateWindow(\"Draw++ Test\", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);\n"
        "    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);\n"
    )

    # Translate AST instructions into C code
    for node in ast:
        code.append(gerer_instruction(node))

    # Finalize rendering and cleanup
    code.append("    SDL_RenderPresent(renderer);")
    code.append("    SDL_Delay(3000);")
    code.append("    SDL_DestroyRenderer(renderer);")
    code.append("    SDL_DestroyWindow(window);")
    code.append("    SDL_Quit();")
    code.append("    return 0;")
    code.append("}")

    return "\n".join(code)


# Function to handle individual AST instructions
def gerer_instruction(instruction):
    """
    Translates an AST instruction into C code.
    Handles lists, variable declarations, and conditions.
    """
    # Process lists of instructions
    if isinstance(instruction, list):
        code = ""
        for instr in instruction:
            code += gerer_instruction(instr) + "\n"
        return code

    # Handle variable declarations
    if instruction["type"] == "VARIABLE_DECLARATION":
        var_type = "int" if instruction["var_type"] == "INT" else "float"
        code_value = (
            instruction["value"]["value"]
            if isinstance(instruction["value"], dict) and instruction["value"]["type"] == "VALUE"
            else instruction["value"]
        )
        return f"    {var_type} {instruction['name']} = {code_value};"

    # Handle condition expressions
    elif instruction["type"] == "CONDITION":
        return gerer_condition(instruction)
    
    # Variable update (e.g., increment, decrement, addition assignment)
    elif instruction["type"] == "VARIABLE_UPDATE":
        var_name = instruction["name"]  # Name of the variable
        operator = instruction["operator"]  # Operator type (e.g., ++, --)
        if operator == TokenType.PLUS_PLUS:  # Increment operator
            return f"    {var_name}++;"
        elif operator == TokenType.MINUS_MINUS:  # Decrement operator
            return f"    {var_name}--;"
        elif operator == TokenType.PLUS_EQUAL:  # Add and assign
            value = instruction["value"]["value"]
            return f"    {var_name} += {value};"
        elif operator == TokenType.MINUS_EQUAL:  # Subtract and assign
            value = instruction["value"]["value"]
            return f"    {var_name} -= {value};"

    # While loop
    elif instruction["type"] == "WHILE_LOOP":
        condition = gerer_condition(instruction["condition"])  # Translate condition to C
        code = f"    while ({condition}) {{\n"
        for statement in instruction["body"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"  # Process each statement in the loop
        code += "    }"
        return code

    # If statement
    elif instruction["type"] == "IF_STATEMENT":
        condition = gerer_condition(instruction["condition"])  # Translate condition to C
        code = f"    if ({condition}) {{\n"
        for statement in instruction["true_block"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"  # Process "if" block statements
        code += "    }"
        if instruction["false_block"]:  # Handle optional "else" block
            code += "    else {\n"
            for statement in instruction["false_block"]["statements"]:
                code += f"{gerer_instruction(statement)}\n"  # Process "else" block statements
            code += "    }"
        return code

    # For loop
    elif instruction["type"] == "FOR_LOOP":
        init = gerer_instruction(instruction["init"]).strip(";")  # Initialization
        condition = gerer_condition(instruction["condition"])  # Loop condition
        update = gerer_instruction(instruction["update"]).strip(";")  # Update operation
        code = f"    for ({init}; {condition}; {update}) {{\n"
        for statement in instruction["body"]["statements"]:
            code += f"{gerer_instruction(statement)}\n"  # Process statements inside the loop
        code += "    }"
        return code

    # Cursor position setting
    elif instruction["type"] == "SET_POSITION":
        return f"    setPosition(&{instruction['cursor']}, {instruction['x']['value']}, {instruction['y']['value']});"

    # Cursor color setting
    elif instruction["type"] == "SET_COLOR":
        color_name = instruction["color"]  # Color name (e.g., "red")
        color_value = COLOR_MAP.get(color_name, "(SDL_Color){0, 0, 0, 255}")  # Default to black if not found
        return f"    setColor(&{instruction['cursor']}, {color_value});"

    # Set line thickness for the cursor
    elif instruction["type"] == "SET_THICKNESS":
        return f"    setThickness(&{instruction['cursor']}, {instruction['thickness']});"

    # Rotate the cursor by a specified angle
    elif instruction["type"] == "ROTATE":
        return f"    rotate(&{instruction['cursor']}, {instruction['angle']['value']});"

    # Draw a line
    elif instruction["type"] == "DRAW_LINE":
        return f"    drawLine(renderer, &{instruction['cursor']}, {instruction['length']['value']});"

    # Cursor declaration
    elif instruction["type"] == "CURSOR_DECLARATION":
        return f"    Cursor {instruction['name']} = createCursor();"  

    # Draw a point
    elif instruction["type"] == "DRAW_POINT":
        return f"    drawPoint(renderer, &{instruction['cursor']});"

    # Draw an arc
    elif instruction["type"] == "DRAW_ARC":
        return f"    drawArc(renderer, &{instruction['cursor']}, {instruction['radius']['value']}, {instruction['angle']['value']});"

    # Draw a circle
    elif instruction["type"] == "DRAW_CIRCLE":
        return f"    drawCircle(renderer, &{instruction['cursor']}, {instruction['radius']['value']});"

    # Draw a square
    elif instruction["type"] == "DRAW_SQUARE":
        return f"    drawSquare(renderer, &{instruction['cursor']}, {instruction['side_length']['value']});"

    # Handle unknown instructions
    raise ValueError(f"Unknown instruction: {instruction}")



# Process conditional expressions
def gerer_condition(condition):
    """
    Converts a Draw++ condition into a C-compatible logical expression.
    Example: "x > 10" → "x > 10"
    """
    left = condition["left"]["value"]  # Left operand
    right = condition["right"]["value"]  # Right operand
    operator = condition["operator"].name  # Operator type
    operators_map = {
        "GREATER_THAN": ">",
        "LESS_THAN": "<",
        "GREATER_EQUAL": ">=",
        "LESS_EQUAL": "<=",
        "EQUAL": "==",
        "NOT_EQUAL": "!=",
    }
    return f"{left} {operators_map[operator]} {right}"

# Save the generated C code to a file
def save_to_file(filename, content):
    """Saves the generated C code to the specified file."""
    with open(filename, "w") as f:
        f.write(content)

# Compile the C code into an executable using GCC
def compile_c_to_exe(c_file, exe_file):
    """
    Compiles the generated C code into an executable using GCC.
    - Links against the SDL2 library for rendering.
    """
    try:
        subprocess.run(["gcc", c_file, "-o", exe_file, "-lSDL2", "-lm"], check=True)
        print(f"Compilation successful: {exe_file}")
    except subprocess.CalledProcessError as e:
        print("Compilation error:", e)