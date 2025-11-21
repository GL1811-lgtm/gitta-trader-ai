import os
import sys
import ast
import pkg_resources

def get_imports_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return set()
            
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def get_installed_packages():
    # Map common import names to package names if they differ
    mapping = {
        'sklearn': 'scikit-learn',
        'PIL': 'Pillow',
        'bs4': 'beautifulsoup4',
        'dotenv': 'python-dotenv',
        'googleapiclient': 'google-api-python-client',
        'smartapi': 'smartapi-python',
        'SmartApi': 'smartapi-python',
        'jwt': 'PyJWT',
        'yaml': 'PyYAML',
        'cv2': 'opencv-python',
        'flask_caching': 'Flask-Caching',
        'flask_cors': 'flask-cors',
        'flask_limiter': 'Flask-Limiter',
        'prometheus_client': 'prometheus-client',
        'apscheduler': 'APScheduler',
        'socketio': 'python-socketio',
        'engineio': 'python-engineio',
        'dns': 'dnspython',
        'pymongo': 'pymongo',
        'redis': 'redis',
        'celery': 'celery',
        'boto3': 'boto3',
        'botocore': 'botocore',
        'praw': 'praw',
        'yfinance': 'yfinance',
        'pythonjsonlogger': 'python-json-logger',
    }
    
    requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
    if not os.path.exists(requirements_path):
        print("requirements.txt not found!")
        return set(), mapping
        
    required_packages = set()
    with open(requirements_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Handle version specifiers like package>=1.0.0
                pkg_name = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                required_packages.add(pkg_name.lower())
                
    return required_packages, mapping

def check_dependencies(start_dir):
    print(f"Scanning {start_dir} for missing dependencies...")
    
    required_packages, mapping = get_installed_packages()
    
    # Standard library modules to ignore
    stdlib_modules = sys.builtin_module_names
    # Add some common stdlib modules that might not be in builtin_module_names
    stdlib_modules += (
        'os', 'sys', 'json', 'time', 'datetime', 'logging', 'threading', 
        'multiprocessing', 'subprocess', 're', 'math', 'random', 'uuid', 
        'typing', 'pathlib', 'shutil', 'glob', 'argparse', 'collections',
        'itertools', 'functools', 'copy', 'pickle', 'csv', 'io', 'base64',
        'hashlib', 'hmac', 'socket', 'ssl', 'urllib', 'http', 'email',
        'xml', 'html', 'unittest', 'doctest', 'pdb', 'traceback', 'inspect',
        'ast', 'pkgutil', 'importlib', 'platform', 'warnings', 'weakref',
        'abc', 'enum', 'signal', 'contextlib', 'asyncio', 'concurrent',
        'queue', 'tempfile', 'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma',
        'sqlite3', 'dbm', 'shelve', 'marshal', 'ctypes', 'struct', 'mmap',
        'pprint', 'textwrap', 'difflib', 'calendar', 'bisect', 'heapq',
        'array', 'sets', 'sched', 'mutex', 'getpass', 'curses', 'platform',
        'errno', 'fcntl', 'select', 'selectors', 'termios', 'tty', 'pty',
        'resource', 'nis', 'syslog', 'optparse', 'getopt', 'fileinput',
        'linecache', 'stat', 'configparser', 'netrc', 'xdrlib', 'plistlib',
        'shlex', 'tk', 'tkinter', 'turtle', 'cmd', 'code', 'codeop',
        'token', 'keyword', 'tokenize', 'tabnanny', 'pyclbr', 'symtable',
        'symbol', 'lib2to3', 'test', 'distutils', 'ensurepip', 'venv',
        'wsgiref', 'xmlrpc', 'smtpd', 'smtplib', 'ftplib', 'poplib',
        'imaplib', 'nntplib', 'telnetlib', 'uuid', 'socketserver',
        'http', 'cgi', 'cgitb', 'webbrowser', 'mimetypes', 'typing',
        'dataclasses', 'contextvars', 'zoneinfo', 'graphlib', 'tracemalloc'
    )
    stdlib_set = set(stdlib_modules)
    
    # Project internal modules - explicitly list known internal packages
    internal_modules = {
        'backend', 'src', 'tests', 'scripts', 
        'angel_one', 'base_collector', 'base_provider', 'base_tester', 
        'historical', 'market_data', 'news_events', 'order_book', 'technical',
        'config', 'configs', 'core', 'database', 'utils', 'agents', 'ai', 'ml'
    }
    
    missing_deps = set()
    
    for root, dirs, files in os.walk(start_dir):
        if 'venv' in root or '.git' in root or '__pycache__' in root or 'archive' in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                imports = get_imports_from_file(filepath)
                
                for imp in imports:
                    # Skip internal modules and stdlib
                    if imp in internal_modules or imp in stdlib_set or imp.startswith('.'):
                        continue
                        
                    # Check if it's a known mapping
                    pkg_name = mapping.get(imp, imp)
                    
                    # Check if it's in requirements (case insensitive)
                    if pkg_name.lower() not in required_packages:
                        # Check if it's a sub-package of a requirement (e.g. 'flask.views' -> 'flask')
                        found = False
                        for req in required_packages:
                            if req == pkg_name.lower() or pkg_name.lower().startswith(req + '-'):
                                found = True
                                break
                        
                        if not found:
                            # Double check if it's a local file in the same directory or project
                            if os.path.exists(os.path.join(root, imp + '.py')) or \
                               os.path.exists(os.path.join(os.getcwd(), 'backend', imp + '.py')) or \
                               os.path.exists(os.path.join(os.getcwd(), 'backend', 'agents', 'collectors', imp + '.py')):
                                continue

                            print(f"Missing dependency: {imp} (in {os.path.relpath(filepath)})")
                            missing_deps.add(pkg_name)

    print("\n" + "="*40)
    if missing_deps:
        print(f"❌ FOUND {len(missing_deps)} POTENTIALLY MISSING DEPENDENCIES:")
        for dep in sorted(missing_deps):
            print(f"  - {dep}")
        print("\nPlease add them to requirements.txt")
        sys.exit(1)
    else:
        print("✅ No missing dependencies found in requirements.txt")
        sys.exit(0)

if __name__ == "__main__":
    check_dependencies("backend")
