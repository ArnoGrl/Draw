import subprocess
import unittest
import sys
import os

# Ajoute le chemin du répertoire parent pour trouver lexer.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from parser import Parser
from utils.tokens import TokenType
from lexer import Lexer

#Fonction de génération de code C à partir de l'AST
def generate_c_code(ast):
    """Génère le code C à partir de l'AST fourni."""
    code = ["#include <stdio.h>", "#include <stdbool.h>", "\n"]
    code.append("int main() {")

    for node in ast:
        code.append(gerer_instruction(node))  # Génère chaque ligne d'instruction

    code.append("    return 0;")
    code.append("}")
    return "\n".join(code)


# Fonction pour gérer toutes les instructions du parser
def gerer_instruction(instruction):
    # Déclaration de variable
    if instruction["type"] == "VARIABLE_DECLARATION":
        var_type = "int" if instruction["var_type"] == "INT" else "float"
        return f"    {var_type} {instruction['name']} = {instruction['value']};"
    
    # Condition
    elif instruction["type"] == "CONDITION":
        return gerer_condition(instruction)
    
    # Mise à jour de variable
    elif instruction["type"] == "VARIABLE_UPDATE":
        var_name = instruction["name"]
        operator = instruction["operator"]
        if operator == "PLUS_PLUS":
            return f"    {var_name}++;"
        elif operator == "MINUS_MINUS":
            return f"    {var_name}--;"
        elif operator == "PLUS_EQUAL":
            value = instruction["value"]["value"]
            return f"    {var_name} += {value};"
        elif operator == "MINUS_EQUAL":
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

    # Instructions non gérées
    raise ValueError(f"Instruсtion inconnue : {instruction}")


# Fonction pour gérer les conditions
def gerer_condition(condition):
    left = condition["left"]["value"]   
    right = condition["right"]["value"]
    operator = condition["operator"]
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
        subprocess.run(["gcc", c_file, "-o", exe_file], check=True)
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
        int i = 5;
        if(i < 5){
            i++
        } 
        """
        syntax_tree = self.parse_code(code)
        return syntax_tree


# Programme principal
if __name__ == "__main__":
    # Étape 1 : Parser le code pour générer l'AST
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

