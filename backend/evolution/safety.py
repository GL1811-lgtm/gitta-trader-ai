import ast
import builtins

class CodeSafetySanitizer:
    """
    Ensures that generated code is safe to execute by analyzing its AST.
    Blocks dangerous imports and functions.
    """
    
    FORBIDDEN_IMPORTS = {
        'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests', 'urllib', 'http',
        'pickle', 'marshal', 'importlib', 'inspect', 'ftplib', 'telnetlib'
    }
    
    FORBIDDEN_FUNCTIONS = {
        'eval', 'exec', 'compile', 'open', 'input', 'globals', 'locals', 'getattr', 'setattr', 'delattr'
    }

    @classmethod
    def validate(cls, code: str) -> tuple[bool, str]:
        """
        Validates the code string.
        Returns (True, "OK") if safe, or (False, error_message) if unsafe.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

        for node in ast.walk(tree):
            # Check imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.Import):
                    names = [n.name.split('.')[0] for n in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        names = [node.module.split('.')[0]]
                
                for name in names:
                    if name in cls.FORBIDDEN_IMPORTS:
                        return False, f"Forbidden import detected: {name}"

            # Check function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in cls.FORBIDDEN_FUNCTIONS:
                        return False, f"Forbidden function call detected: {node.func.id}"
                # Check for __import__
                if isinstance(node.func, ast.Name) and node.func.id == '__import__':
                     return False, "Forbidden function call detected: __import__"

        return True, "OK"

if __name__ == "__main__":
    # Test
    unsafe_code = "import os; os.system('echo hack')"
    safe_code = "import math; x = math.sqrt(16)"
    
    print(f"Unsafe Check: {CodeSafetySanitizer.validate(unsafe_code)}")
    print(f"Safe Check: {CodeSafetySanitizer.validate(safe_code)}")
