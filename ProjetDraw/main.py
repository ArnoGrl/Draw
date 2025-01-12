import os
import sys

def main():
    launch_ide()

def launch_ide():
    ide_path = os.path.join("IDE", "ide.py")
    if os.path.exists(ide_path):
        print("\nLancement de l'IDE...")
        os.system(f"python {ide_path}")
    else:
        print("\nErreur : Le fichier IDE/ide.py est introuvable.")

if __name__ == "__main__":
    main()
