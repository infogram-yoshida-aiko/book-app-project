"""Test the unread command functionality."""

import sys
import os
from io import StringIO

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from books import BookCollection
from utils import display_books

def test_unread_command_basic():
    """Test basic unread command filtering."""
    collection = BookCollection()
    
    # Add some books
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    
    # Mark some as read
    collection.mark_as_read("1984")
    
    # Get unread books
    unread = collection.list_unread_books()
    
    # Verify results
    assert len(unread) == 2, f"Expected 2 unread books, got {len(unread)}"
    assert unread[0].title == "Dune"
    assert unread[1].title == "The Great Gatsby"
    
    print("✅ test_unread_command_basic passed")

def test_unread_command_all_read():
    """Test when all books are read."""
    collection = BookCollection()
    
    # Add and mark all as read
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")
    collection.mark_as_read("Dune")
    
    # Get unread books
    unread = collection.list_unread_books()
    
    # Verify empty
    assert len(unread) == 0, f"Expected 0 unread books, got {len(unread)}"
    
    print("✅ test_unread_command_all_read passed")

def test_unread_command_empty_collection():
    """Test with empty collection."""
    collection = BookCollection()
    
    # Get unread books
    unread = collection.list_unread_books()
    
    # Verify empty
    assert len(unread) == 0, f"Expected 0 unread books, got {len(unread)}"
    
    print("✅ test_unread_command_empty_collection passed")

def test_unread_command_all_unread():
    """Test when all books are unread."""
    collection = BookCollection()
    
    # Add books without marking any as read
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    
    # Get unread books
    unread = collection.list_unread_books()
    
    # Verify all returned
    assert len(unread) == 3, f"Expected 3 unread books, got {len(unread)}"
    assert all(not book.read for book in unread), "All books should be unread"
    
    print("✅ test_unread_command_all_unread passed")

def test_display_unread_books():
    """Test display_books function with unread books."""
    collection = BookCollection()
    
    # Add books
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")
    
    # Get unread and capture output
    unread = collection.list_unread_books()
    
    # Capture display output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display_books(unread)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    # Verify output contains unread book
    assert "Dune" in output, "Output should contain Dune"
    assert "📖 Unread" in output, "Output should show unread status"
    
    print("✅ test_display_unread_books passed")

if __name__ == "__main__":
    test_unread_command_basic()
    test_unread_command_all_read()
    test_unread_command_empty_collection()
    test_unread_command_all_unread()
    test_display_unread_books()
    
    print("\n✅ All unread command tests passed!")
