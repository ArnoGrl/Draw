# parser.py
from src.commands.cursor import CursorCommand
from src.commands.shapes import ShapeCommand
from src.commands.animation import AnimateCommand

class Parser:
    def parse(self, code: str):
        commands = []
        lines = code.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith("cursor"):
                commands.append(CursorCommand(line))
            elif "draw" in line:
                commands.append(ShapeCommand(line))
            elif "animate" in line:
                commands.append(AnimateCommand(line))
        
        return commands
