#!/usr/bin/env python
"""Run pytest tests to verify the changes."""

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_books.py", "-v"],
    cwd="C:\\Users\\yoshida.aiko\\吉田\\コパイロット\\Copilot CLI for beginners\\samples\\book-app-project",
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

sys.exit(result.returncode)
