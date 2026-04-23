#!/usr/bin/env python3
"""Execute tests and display results."""

import subprocess
import sys
import os

os.chdir(r'C:\Users\yoshida.aiko\吉田\コパイロット\Copilot CLI for beginners\samples\book-app-project')

print("=" * 80)
print("RUNNING: python test_list_unread_all.py")
print("=" * 80)
print()

# Run the verification script
result = subprocess.run([sys.executable, "test_list_unread_all.py"])

sys.exit(result.returncode)
