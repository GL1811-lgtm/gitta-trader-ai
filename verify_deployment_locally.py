import os
import sys
import pkgutil
import importlib
import traceback

# Add the current directory to sys.path
sys.path.append(os.getcwd())

# Set dummy environment variables to prevent runtime errors during import
os.environ['FLASK_ENV'] = 'production'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['OPENROUTER_API_KEY'] = 'dummy_key' # Prevent Multi-AI crash
os.environ['GROQ_API_KEY'] = 'dummy_key'
os.environ['ANGEL_API_KEY'] = 'dummy'
os.environ['ANGEL_CLIENT_ID'] = 'dummy'
os.environ['ANGEL_PASSWORD'] = 'dummy'
os.environ['ANGEL_TOTP_KEY'] = 'dummy'

def check_imports(start_dir):
    print(f"Scanning {start_dir}...")
    error_count = 0
    success_count = 0
    
    for root, dirs, files in os.walk(start_dir):
        # Skip archive directories
        if 'archive' in dirs:
            dirs.remove('archive')
            
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Construct module path
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                module_name = rel_path.replace(os.sep, ".").replace(".py", "")
                
                try:
                    importlib.import_module(module_name)
                    success_count += 1
                except Exception as e:
                    print(f"ERROR: {module_name}")
                    # traceback.print_exc() # Disable traceback to reduce noise/encoding issues
                    print(f"  {e}")
                    error_count += 1

    print(f"Results: Success={success_count}, Failed={error_count}")
    
    if error_count == 0:
        print("ALL PASSED")
        sys.exit(0)
    else:
        print("ERRORS FOUND")
        sys.exit(1)

if __name__ == "__main__":
    start_path = sys.argv[1] if len(sys.argv) > 1 else "backend"
    check_imports(start_path)
