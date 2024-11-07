# interpreter.py
class Interpreter:
    def execute(self, commands):
        for command in commands:
            command.execute()
