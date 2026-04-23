#!/usr/bin/env python
import subprocess
import sys
import os

# Change to the project directory
os.chdir(r'C:\Users\yoshida.aiko\吉田\コパイロット\Copilot CLI for beginners\samples\book-app-project')

# Run pytest with verbose output
result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_books.py', '-v'], 
                       capture_output=False, text=True)

sys.exit(result.returncode)
