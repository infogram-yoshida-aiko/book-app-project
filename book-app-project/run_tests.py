#!/usr/bin/env python3
"""Run pytest on test_books.py and show results."""

import subprocess
import sys
import os

os.chdir(r'C:\Users\yoshida.aiko\吉田\コパイロット\Copilot CLI for beginners\samples\book-app-project')

print("=" * 80)
print("Running: pytest tests/test_books.py -v")
print("=" * 80)
print()

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_books.py", "-v", "--tb=short"],
    capture_output=False,
    text=True
)

sys.exit(result.returncode)
