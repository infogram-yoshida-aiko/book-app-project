#!/usr/bin/env python3
"""
Comprehensive test verification for list_unread_books functionality.
This script simulates pytest behavior and validates all test scenarios.
"""

import sys
import os

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from books import BookCollection

class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, name):
        self.passed += 1
        self.tests.append(("✅ PASSED", name))
        print(f"✅ {name}")
    
    def add_fail(self, name, error):
        self.failed += 1
        self.tests.append(("❌ FAILED", name, str(error)))
        print(f"❌ {name}")
        print(f"   Error: {error}")
    
    def print_summary(self):
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        for test in self.tests:
            if len(test) == 2:
                status, name = test
                print(f"{status}: {name}")
            else:
                status, name, error = test
                print(f"{status}: {name}")
                print(f"        {error}")
        
        print("\n" + "-" * 80)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {self.passed + self.failed}")
        print("=" * 80)
        return self.failed == 0

def test_list_unread_books_returns_only_unread(results: TestResults):
    """Test that list_unread_books returns only unread books."""
    test_name = "test_list_unread_books_returns_only_unread"
    try:
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        
        # Mark one book as read
        collection.mark_as_read("Dune")
        
        # Get unread books
        unread = collection.list_unread_books()
        
        # Assertions
        assert len(unread) == 2, f"Expected 2 unread, got {len(unread)}"
        assert collection.find_book_by_title("1984") in unread, "1984 should be unread"
        assert collection.find_book_by_title("Foundation") in unread, "Foundation should be unread"
        assert collection.find_book_by_title("Dune") not in unread, "Dune should not be in unread (it's read)"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_all_books_unread(results: TestResults):
    """Test list_unread_books when all books are unread."""
    test_name = "test_list_unread_books_all_books_unread"
    try:
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 3, f"Expected 3 unread, got {len(unread)}"
        assert len(unread) == len(collection.list_books()), "All books should be unread"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_all_books_read(results: TestResults):
    """Test list_unread_books when all books are read."""
    test_name = "test_list_unread_books_all_books_read"
    try:
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        
        collection.mark_as_read("1984")
        collection.mark_as_read("Dune")
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 0, f"Expected 0 unread, got {len(unread)}"
        assert unread == [], "Should return empty list"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_empty_collection(results: TestResults):
    """Test list_unread_books on empty collection."""
    test_name = "test_list_unread_books_empty_collection"
    try:
        collection = BookCollection()
        unread = collection.list_unread_books()
        
        assert len(unread) == 0, f"Expected 0 unread, got {len(unread)}"
        assert unread == [], "Should return empty list"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_single_unread_book(results: TestResults):
    """Test list_unread_books with exactly one unread book."""
    test_name = "test_list_unread_books_single_unread_book"
    try:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 1, f"Expected 1 unread, got {len(unread)}"
        assert unread[0].title == "Dune", "Should be Dune"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_single_read_book(results: TestResults):
    """Test list_unread_books with exactly one read book."""
    test_name = "test_list_unread_books_single_read_book"
    try:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("Dune")
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 0, f"Expected 0 unread, got {len(unread)}"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_returns_list_type(results: TestResults):
    """Test that list_unread_books returns a list."""
    test_name = "test_list_unread_books_returns_list_type"
    try:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        
        unread = collection.list_unread_books()
        
        assert isinstance(unread, list), f"Expected list, got {type(unread)}"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_does_not_modify_collection(results: TestResults):
    """Test that calling list_unread_books doesn't modify the collection."""
    test_name = "test_list_unread_books_does_not_modify_collection"
    try:
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("Dune")
        
        initial_count = len(collection.books)
        initial_unread_count = len([b for b in collection.books if not b.read])
        
        unread = collection.list_unread_books()
        
        assert len(collection.books) == initial_count, "Collection size changed"
        assert len([b for b in collection.books if not b.read]) == initial_unread_count, "Unread count changed"
        assert collection.find_book_by_title("1984").read is False, "1984 read status changed"
        assert collection.find_book_by_title("Dune").read is True, "Dune read status changed"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_preserves_order(results: TestResults):
    """Test that list_unread_books preserves order of unread books."""
    test_name = "test_list_unread_books_preserves_order"
    try:
        collection = BookCollection()
        titles = ["A Book", "B Book", "C Book", "D Book"]
        for i, title in enumerate(titles, start=1900):
            collection.add_book(title, "Author", i)
        
        # Mark 2nd and 4th as read
        collection.mark_as_read("B Book")
        collection.mark_as_read("D Book")
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 2, f"Expected 2 unread, got {len(unread)}"
        assert unread[0].title == "A Book", "First unread should be A Book"
        assert unread[1].title == "C Book", "Second unread should be C Book"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def test_list_unread_books_mixed_large_collection(results: TestResults):
    """Test list_unread_books with many books in mixed states."""
    test_name = "test_list_unread_books_mixed_large_collection"
    try:
        collection = BookCollection()
        titles = [
            ("1984", "George Orwell", 1949),
            ("Dune", "Frank Herbert", 1965),
            ("Foundation", "Isaac Asimov", 1951),
            ("The Hobbit", "J.R.R. Tolkien", 1937),
            ("Neuromancer", "William Gibson", 1984),
        ]
        
        for title, author, year in titles:
            collection.add_book(title, author, year)
        
        # Mark alternating books as read
        collection.mark_as_read("1984")
        collection.mark_as_read("Foundation")
        collection.mark_as_read("Neuromancer")
        
        unread = collection.list_unread_books()
        
        assert len(unread) == 2, f"Expected 2 unread, got {len(unread)}"
        assert collection.find_book_by_title("Dune") in unread, "Dune should be unread"
        assert collection.find_book_by_title("The Hobbit") in unread, "The Hobbit should be unread"
        
        results.add_pass(test_name)
    except Exception as e:
        results.add_fail(test_name, e)

def main():
    print("=" * 80)
    print("RUNNING LIST_UNREAD_BOOKS TESTS")
    print("=" * 80)
    print()
    
    results = TestResults()
    
    # Run all tests
    test_list_unread_books_returns_only_unread(results)
    test_list_unread_books_all_books_unread(results)
    test_list_unread_books_all_books_read(results)
    test_list_unread_books_empty_collection(results)
    test_list_unread_books_single_unread_book(results)
    test_list_unread_books_single_read_book(results)
    test_list_unread_books_returns_list_type(results)
    test_list_unread_books_does_not_modify_collection(results)
    test_list_unread_books_preserves_order(results)
    test_list_unread_books_mixed_large_collection(results)
    
    print()
    success = results.print_summary()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
