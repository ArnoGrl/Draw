# Draw Project

## Description
Draw++ est un langage de programmation spécialement conçu pour la création
graphique, visant à rendre l’interaction avec des éléments visuels simple et intuitive.
Grâce à un ensemble d’instructions claires et accessibles, il permet aux utilisateurs de
dessiner facilement des formes et de créer des illustrations graphiques.

Le projet comprend une grammaire écrite sous le format .Json, un analyseur lexical et syntaxique, un fichier contenant une liste de "Tokens", ainsi qu'un compilateur et un interpréteur. Il propose également une interface de développement (IDE) pour créer et tester des fichiers `.draw++`. Tout les fichier sont écrits en Python, le compilateur génère un fichier .c, qui est ensuite compiler en un fichier éxécutable : "output.exe".

Pour des raisons de faciliter, nous vous conseillons fortement d'installer ce logiciel sur Ubuntu.
,

## Objectifs 

- Créer un environnement de développement intégré (IDE) pour développer des fichiers `.draw++`
- Fournir un interpréteur et un compilateur capables de lire et d'exécuter des scripts `.draw++`
- Fournir une grammaire, un analyseur syntaxique, un analyseur Lexicale, basé sur une liste de tokens.
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
   python3 -m venv venv
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
souvent deja installer, mais si ce n'est pas le cas, installer : SDL2, et Tkinter
```
   sudo apt update
   sudo apt install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   sudo apt install python3-tk -y
```

## Exécution du projet
Pour lancer l'IDE, et manipluer le language Draw++ :
```
python main.py
```
Vous pouvez tester des fichier pré-enregistré en appuyant sur open en haut à gauche de l'IDE.

Il est possible d'ouvrir un fichier, d'en enregistrer, d'en créer un nouveau.

Les fichier Draw on l'extension .draw++

## Fichiers de test
- **demo.draw++** : Un exemple de fichier script Draw++.
- **fractale.draw++** : Un autre exemple illustrant des formes fractales.
- **Teste.draw++**

## Livrables
- Langage de programmation Draw++.
- Interface utilisateur : IDE 
- Structure modulaire : Composants séparés (lexer, parser, interpréteur, compiler, Tokens, grammar)
- Des fichier de teste : que nous avons décider de laisser dans le projet.
- Documentation détaillée concernant le code source et les fonctionnalités.
- Vidéo de présentation 

