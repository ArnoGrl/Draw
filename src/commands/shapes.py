# shapes.py
class ShapeCommand:
    def __init__(self, line):
        self.line = line

    def execute(self):
        print(f"Executing shape command: {self.line}")
