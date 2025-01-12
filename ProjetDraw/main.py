import os
import sys

def main():
    print("\n========== Draw Project ==========")
    print("1. Lancer l'IDE (Interface de développement)")
    print("2. Exécuter un fichier .draw++")
    print("3. Quitter")

    choice = input("\nChoisissez une option : ")

    if choice == "1":
        launch_ide()
    elif choice == "2":
        execute_draw_file()
    elif choice == "3":
        print("\nMerci d'avoir utilisé Draw Project ! À bientôt.")
        sys.exit(0)
    else:
        print("\nChoix invalide. Veuillez réessayer.")
        main()

def launch_ide():
    ide_path = os.path.join("IDE", "ide.py")
    if os.path.exists(ide_path):
        print("\nLancement de l'IDE...")
        os.system(f"python {ide_path}")
    else:
        print("\nErreur : Le fichier IDE/ide.py est introuvable.")


def execute_draw_file():
    file_path = input("\nEntrez le chemin du fichier .draw++ à exécuter : ")
    if os.path.exists(file_path) and file_path.endswith(".draw++"):
        print(f"\nExécution du fichier {file_path}...")
        # Ajoutez ici l'appel à votre interpréteur ou parser
        os.system(f"python ProjetDraw/main.py {file_path}")
    else:
        print("\nErreur : Fichier invalide ou introuvable.")

if __name__ == "__main__":
    main()
