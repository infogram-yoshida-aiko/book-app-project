#!/usr/bin/env python3
"""Verify list_unread_books implementation with direct test."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from books import BookCollection

def main():
    print("=" * 70)
    print("Testing: test_list_unread_books_returns_only_unread")
    print("=" * 70)
    
    try:
        # Arrange
        print("\n[Arrange] Setting up collection...")
        collection = BookCollection()
        print("  ✓ Created BookCollection")
        
        print("  Adding books...")
        book1 = collection.add_book("1984", "George Orwell", 1949)
        print(f"    ✓ Added: {book1.title} (read={book1.read})")
        
        book2 = collection.add_book("Dune", "Frank Herbert", 1965)
        print(f"    ✓ Added: {book2.title} (read={book2.read})")
        
        book3 = collection.add_book("Foundation", "Isaac Asimov", 1951)
        print(f"    ✓ Added: {book3.title} (read={book3.read})")
        
        print("  Marking one book as read...")
        result = collection.mark_as_read("Dune")
        print(f"    ✓ mark_as_read('Dune') returned: {result}")
        
        book_dune = collection.find_book_by_title("Dune")
        print(f"    ✓ Dune.read is now: {book_dune.read}")
        
        # Act
        print("\n[Act] Calling list_unread_books()...")
        unread = collection.list_unread_books()
        print(f"  ✓ Got result: {len(unread)} unread books")
        for i, book in enumerate(unread, 1):
            print(f"    {i}. {book.title} (read={book.read})")
        
        # Assert
        print("\n[Assert] Verifying results...")
        
        # Check 1: Length
        print(f"  1. Length check: {len(unread)} == 2")
        assert len(unread) == 2, f"Expected 2 unread books, got {len(unread)}"
        print("     ✅ PASS")
        
        # Check 2: 1984 in unread
        print(f"  2. '1984' in unread: {collection.find_book_by_title('1984') in unread}")
        assert collection.find_book_by_title("1984") in unread, "1984 should be in unread"
        print("     ✅ PASS")
        
        # Check 3: Foundation in unread
        print(f"  3. 'Foundation' in unread: {collection.find_book_by_title('Foundation') in unread}")
        assert collection.find_book_by_title("Foundation") in unread, "Foundation should be in unread"
        print("     ✅ PASS")
        
        # Check 4: Dune NOT in unread
        print(f"  4. 'Dune' NOT in unread: {collection.find_book_by_title('Dune') not in unread}")
        assert collection.find_book_by_title("Dune") not in unread, "Dune should NOT be in unread (it's marked as read)"
        print("     ✅ PASS")
        
        print("\n" + "=" * 70)
        print("✅ ALL ASSERTIONS PASSED!")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ ASSERTION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
