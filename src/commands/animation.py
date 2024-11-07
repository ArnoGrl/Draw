# animation.py
class AnimateCommand:
    def __init__(self, line):
        self.line = line

    def execute(self):
        print(f"Executing animation command: {self.line}")
