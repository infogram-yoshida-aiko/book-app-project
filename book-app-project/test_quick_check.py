#!/usr/bin/env python3
"""Quick test to verify list_unread_books implementation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from books import BookCollection

def test_list_unread_books_returns_only_unread():
    """Test that list_unread_books returns only unread books."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    
    # Mark one book as read
    collection.mark_as_read("Dune")
    
    # Get unread books
    unread = collection.list_unread_books()
    
    # Verify results
    assert len(unread) == 2, f"Expected 2 unread books, got {len(unread)}"
    assert collection.find_book_by_title("1984") in unread, "1984 should be in unread"
    assert collection.find_book_by_title("Foundation") in unread, "Foundation should be in unread"
    assert collection.find_book_by_title("Dune") not in unread, "Dune should NOT be in unread (it's marked as read)"
    
    print("✅ test_list_unread_books_returns_only_unread PASSED")

if __name__ == "__main__":
    try:
        test_list_unread_books_returns_only_unread()
        print("\n✅ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
