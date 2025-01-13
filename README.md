# Draw Project

## Description
Draw ++ est une application qui permet d'interpréter des fichiers personnalisés au format `.draw++`. Le projet comprend un compilateur et un interpréteur écrit en Python, ainsi que des modules additionnels en C pour gérer certaines fonctions bas niveau. Il propose également une interface de développement (IDE) minimaliste pour créer et tester des fichiers `.draw++`.


## Objectifs 

- Créer une interface utilisateur minimaliste (IDE) pour développer des fichiers `.draw++`
- Fournir un interpréteur et un compilateur capables de lire et d'exécuter des scripts `.draw++`
- Assurer une extensibilité du projet grâce à une architecture modulaire.
  
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

Il est possible d'ouvrir un fichier, d'en enregistrer, d'en créer un nouveau.

Les fichier Draw on l'extension .draw++

## Fichiers de test
- **demo.draw++** : Un exemple de fichier script Draw++.
- **fractale.draw++** : Un autre exemple illustrant des formes fractales.

## Livrables
- Langage de programmation graphique de A à Z.
- Interface utilisateur : IDE minimaliste (lancé via python IDE/ide.py)
- Structure modulaire : Composants séparés (lexer, parser, interpréteur)
- Documentation détaillée concernant le code source et les fonctionnalités.
- Vidéo de présentation 

