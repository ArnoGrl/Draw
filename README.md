# Draw Project

## Description
Draw ++ est une application qui permet d'interpréter des fichiers personnalisés au format `.draw++`. Le projet comprend un compilateur et un interpréteur écrit en Python, ainsi que des modules additionnels en C pour gérer certaines fonctions bas niveau. Il propose également une interface de développement (IDE) minimaliste pour créer et tester des fichiers `.draw++`.

## Structure du projet
Voici la structure principale du projet :

```
Draw-master/
├── ProjetDraw/
│   ├── main.py          # Point d'entrée principal du projet
│   ├── lexer.py         # Analyseur lexical
│   ├── parser.py        # Analyseur syntaxique
│   ├── interpreter.py   # Interpréteur des commandes draw++
│   ├── compiler.py
│   ├── tests/           # Scripts de tests unitaires
│   ├── IDE/             # Interface de développement minimaliste
│   └── utils/           # Modules utilitaires (grammar, tokens)
├── requirements.txt     # Liste des dépendances Python
└── Draw.txt             # Exemple de fichier de test
```

## Installation
### Étape 1 : Créer un environnement virtuel
Pour éviter les conflits de dépendances, il est recommandé de créer un environnement virtuel Python.

1. Créez l'environnement virtuel :
   ```
   python -m venv venv
   ```

2. Activez l'environnement virtuel :
   - **Sous Windows** :
     ```
     venv\Scripts\activate
     ```
   - **Sous macOS/Linux** :
     ```
     source venv/bin/activate
     ```

### Étape 2 : Installer les dépendances
Une fois l'environnement virtuel activé, installez les dépendances requises à partir du fichier `requirements.txt` :
```
   pip install -r requirements.txt
```

## Exécution du projet
Pour lancer l'interpréteur principal :
```
python main.py
```
Vous pouvez tester des fichier pré-enregistré en appuyant sur open en haut à gauche de l'IDE.
Les fichier Draw on l'extension .draw++

## Fichiers importants
- **demo.draw++** : Un exemple de fichier script Draw++.
- **fractale.draw++** : Un autre exemple illustrant des formes fractales.
- **tests/** : Contient les tests unitaires pour vérifier la validité du lexer, parser et interpreter.


