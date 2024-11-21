# grammar.py

# Grammaire de Draw++ définie en Python

grammar = {
    "programme": {
        "description": "Un programme Draw++ est une séquence d'instructions.",
        "rule": ["instruction*"]
    },
    
    "instruction": {
        "description": "Une instruction peut être une déclaration de curseur, une position, un dessin, une condition, une boucle, etc.",
        "rule": [
            "declaration_curseur",
            "positionnement_curseur",
            "couleur_curseur",
            "epaisseur_curseur",
            "deplacement_curseur",
            "rotation_curseur",
            "dessin_ligne",
            "dessin_carre",
            "dessin_cercle",
            "dessin_point",
            "dessin_arc",
            "declaration_variable",
            "affectation_variable",
            "conditionnelle",
            "boucle_for",
            "boucle_while",
            "bloc_instructions",
            "appel_bloc",
            "fonction",
            "appel_fonction"
        ]
    },
    
    "declaration_curseur": {
        "description": "Déclaration d'un curseur avec un nom spécifique.",
        "rule": ["'cursor'", "identifiant", "';'"]
    },
    
    "positionnement_curseur": {
        "description": "Positionne le curseur à des coordonnées spécifiques.",
        "rule": ["identifiant", "'.setPosition'", "'('", "entier", "','", "entier", "')'", "';'"]
    },
    
    "couleur_curseur": {
        "description": "Change la couleur du curseur.",
        "rule": ["identifiant", "'.setColor'", "'('", "couleur", "')'", "';'"]
    },
    
    "epaisseur_curseur": {
        "description": "Change l'épaisseur du trait du curseur.",
        "rule": ["identifiant", "'.setThickness'", "'('", "entier", "')'", "';'"]
    },
    
    "deplacement_curseur": {
        "description": "Déplace le curseur d'une distance spécifique.",
        "rule": ["identifiant", "'.move'", "'('", "entier", "')'", "';'"]
    },
    
    "rotation_curseur": {
        "description": "Fait pivoter le curseur d'un angle donné.",
        "rule": ["identifiant", "'.rotate'", "'('", "entier", "')'", "';'"]
    },
    
    "dessin_ligne": {
        "description": "Dessine une ligne depuis la position actuelle du curseur.",
        "rule": ["identifiant", "'.drawLine'", "'('", "entier", "')'", "';'"]
    },
    
    "dessin_carre": {
        "description": "Dessine un carré de côté donné.",
        "rule": ["identifiant", "'.drawSquare'", "'('", "entier", "')'", "';'"]
    },
    
    "dessin_cercle": {
        "description": "Dessine un cercle avec un rayon donné.",
        "rule": ["identifiant", "'.drawCircle'", "'('", "entier", "')'", "';'"]
    },
    
    "dessin_point": {
        "description": "Dessine un point à la position actuelle du curseur.",
        "rule": ["identifiant", "'.drawPoint'", "'()'", "';'"]
    },
    
    "dessin_arc": {
        "description": "Dessine un arc de cercle avec un rayon et un angle spécifiques.",
        "rule": ["identifiant", "'.drawArc'", "'('", "entier", "','", "entier", "')'", "';'"]
    },
    
    "declaration_variable": {
        "description": "Déclare une variable entière ou flottante.",
        "rule": [
            ["'int'", "identifiant", "'='", "valeur", "';'"],
            ["'float'", "identifiant", "'='", "valeur", "';'"]
        ]
    },
    
    "affectation_variable": {
        "description": "Affecte une nouvelle valeur à une variable existante.",
        "rule": ["identifiant", "'='", "valeur", "';'"]
    },
    
    "conditionnelle": {
        "description": "Conditionnelle if-else pour contrôler le flux d'instructions.",
        "rule": [
            "'if'", "'('", "condition", "')'", "'{'", "instructions", "'}'",
            ["'else'", "'{'", "instructions", "'}'"]
        ]
    },
    
    "condition": {
        "description": "Condition pour une instruction conditionnelle.",
        "rule": ["expression", "operateur_conditionnel", "expression"]
    },
    
    "operateur_conditionnel": {
        "description": "Opérateur pour une condition (égalité, inégalité, etc.).",
        "rule": ["'=='", "'!='", "'<'", "'>'", "'<='", "'>='"]
    },
    
    "boucle_for": {
    "description": "Boucle for pour répéter des instructions un nombre fixe de fois.",
    "rule": [
        "'for'", "'('", "'int'", "identifiant", "'='", "entier", "';'",
        "condition", "';'",
        "identifiant", ["'++'", "'--'"], "')'", "'{'", "instructions", "'}'"
    ]
    },

    
    "boucle_while": {
        "description": "Boucle while pour répéter des instructions tant qu'une condition est vraie.",
        "rule": ["'while'", "'('", "condition", "')'", "'{'", "instructions", "'}'"]
    },
    
    "bloc_instructions": {
        "description": "Bloc d'instructions pour regrouper plusieurs commandes.",
        "rule": ["'block'", "identifiant", "'{'", "instructions", "'}'"]
    },
    
    "appel_bloc": {
        "description": "Appelle un bloc d'instructions un nombre donné de fois.",
        "rule": ["'repeat'", "'('", "identifiant", "','", "entier", "')'", "';'"]
    },
    
    "fonction": {
        "description": "Définit une fonction personnalisée.",
        "rule": ["'function'", "identifiant", "'('", "parametres", "')'", "'{'", "instructions", "'}'"]
    },
    
    "parametres": {
        "description": "Liste des paramètres pour une fonction.",
        "rule": ["identifiant", [ "','", "identifiant" ]]
    },
    
    "appel_fonction": {
        "description": "Appelle une fonction définie précédemment.",
        "rule": ["identifiant", "'('", "valeurs_parametres", "')'", "';'"]
    },
    
    "entier": {
        "description": "Nombre entier, pouvant être négatif.",
        "rule": [["'-'", "chiffre"], "chiffre"]
    },
    
    "valeur": {
        "description": "Valeur pouvant être un entier, un flottant, ou un identifiant.",
        "rule": ["entier", "flottant", "identifiant"]
    },
    
    "flottant": {
        "description": "Nombre flottant avec une partie décimale.",
        "rule": [["'-'", "chiffre", "'.'", "chiffre"], ["chiffre", "'.'", "chiffre"]]
    },
    
    "identifiant": {
        "description": "Identifiant pour les curseurs, variables, et fonctions.",
        "rule": ["lettre", ["lettre", "chiffre", "'_'"]]
    },
    
    "instructions": {
        "description": "Une séquence d'instructions.",
        "rule": ["instruction*"]
    },
    
    "valeurs_parametres": {
        "description": "Liste des valeurs passées en paramètres à une fonction.",
        "rule": ["valeur", [ "','", "valeur" ]]
    },

    "variable_update": {
    "description": "Met à jour une variable (exemple : i++ ou i--).",
    "rule": ["identifiant", ["'++'", "'--'"]]
    }

}

