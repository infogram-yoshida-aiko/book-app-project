import sys
import os

# Change to the project directory
project_dir = r'C:\Users\yoshida.aiko\吉田\コパイロット\Copilot CLI for beginners\samples\book-app-project'
os.chdir(project_dir)
sys.path.insert(0, project_dir)

# Import and run pytest programmatically
import pytest

# Run pytest with verbose output and capture the return code
exit_code = pytest.main(['tests/test_books.py', '-v', '-s'])

print(f"\n{'='*70}")
print(f"TEST RUN COMPLETED with exit code: {exit_code}")
print(f"{'='*70}")

sys.exit(exit_code)
