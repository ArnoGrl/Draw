# cursor.py
class CursorCommand:
    def __init__(self, line):
        self.line = line

    def execute(self):
        print(f"Executing cursor command: {self.line}")
