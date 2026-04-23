"""Quick test for unread command - simulates CLI usage."""

import json
import os
import sys

# Change to the book-app directory
book_app_dir = r"C:\Users\yoshida.aiko\吉田\コパイロット\Copilot CLI for beginners\samples\book-app-project"
os.chdir(book_app_dir)
sys.path.insert(0, book_app_dir)

from books import BookCollection

# Create a test collection with known data
print("Creating test collection...")
collection = BookCollection()

print(f"\nTotal books in collection: {len(collection.books)}")

# Test 1: List all books
all_books = collection.list_books()
print(f"\n✓ Test 1 - All books: {len(all_books)} books")
for book in all_books:
    print(f"  - {book.title} (read={book.read})")

# Test 2: List unread books (the new feature)
unread_books = collection.list_unread_books()
print(f"\n✓ Test 2 - Unread books: {len(unread_books)} books")
for book in unread_books:
    print(f"  - {book.title} (read={book.read})")

# Test 3: Verify filtering is correct
print("\n✓ Test 3 - Verify filtering:")
expected_unread = [b for b in all_books if not b.read]
assert len(unread_books) == len(expected_unread), "Filtering mismatch!"
assert all(not b.read for b in unread_books), "Some unread books are marked as read!"
print("  Filtering is correct! ✅")

# Test 4: Test with CLI simulation
print("\n✓ Test 4 - Simulate CLI command 'python book_app.py unread':")
from io import StringIO

# Capture stdout
old_stdout = sys.stdout
sys.stdout = StringIO()

try:
    # Import book_app module
    from book_app import handle_unread
    handle_unread()
    output = sys.stdout.getvalue()
finally:
    sys.stdout = old_stdout

print("  Output from handle_unread():")
print(output)

print("\n✅ All tests passed!")
print("\nSummary:")
print(f"  - Total books: {len(all_books)}")
print(f"  - Unread books: {len(unread_books)}")
print(f"  - Read books: {len(all_books) - len(unread_books)}")
