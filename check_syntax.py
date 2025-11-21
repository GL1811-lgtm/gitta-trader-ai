import os
import ast

def check_syntax(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        source = f.read()
                    ast.parse(source)
                    print(f"OK: {path}")
                except SyntaxError as e:
                    print(f"ERROR: {path} - {e}")
                except Exception as e:
                    print(f"ERROR: {path} - {e}")

if __name__ == "__main__":
    check_syntax("backend")
