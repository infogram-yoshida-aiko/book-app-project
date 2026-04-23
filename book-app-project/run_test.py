#!/usr/bin/env python3
"""Quick test runner to verify find_by_author validation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from books import BookCollection, ValidationError
import tempfile
import json

def test_validation():
    """Test find_by_author validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file = os.path.join(tmpdir, "data.json")
        with open(temp_file, "w") as f:
            json.dump([], f)
        
        # Monkey patch the DATA_FILE
        import books
        original_data_file = books.DATA_FILE
        books.DATA_FILE = temp_file
        
        try:
            collection = BookCollection()
            collection.add_book("1984", "George Orwell", 1949)
            
            # Test 1: Empty string should raise ValidationError
            print("Test 1: Empty string...", end=" ")
            try:
                collection.find_by_author("")
                print("❌ FAILED - Should raise ValidationError")
                return False
            except ValidationError as e:
                if "Author cannot be empty" in str(e):
                    print("✅ PASSED")
                else:
                    print(f"❌ FAILED - Wrong error message: {e}")
                    return False
            
            # Test 2: Whitespace-only should raise ValidationError
            print("Test 2: Whitespace-only...", end=" ")
            try:
                collection.find_by_author("   ")
                print("❌ FAILED - Should raise ValidationError")
                return False
            except ValidationError as e:
                if "Author cannot be empty" in str(e):
                    print("✅ PASSED")
                else:
                    print(f"❌ FAILED - Wrong error message: {e}")
                    return False
            
            # Test 3: Valid author search still works
            print("Test 3: Valid search (exact match)...", end=" ")
            results = collection.find_by_author("George Orwell")
            if len(results) == 1 and results[0].title == "1984":
                print("✅ PASSED")
            else:
                print(f"❌ FAILED - Expected 1 result, got {len(results)}")
                return False
            
            # Test 4: Partial match still works
            print("Test 4: Partial match...", end=" ")
            results = collection.find_by_author("Orwell")
            if len(results) == 1:
                print("✅ PASSED")
            else:
                print(f"❌ FAILED - Expected 1 result, got {len(results)}")
                return False
            
            # Test 5: Case-insensitive still works
            print("Test 5: Case-insensitive...", end=" ")
            results = collection.find_by_author("george orwell")
            if len(results) == 1:
                print("✅ PASSED")
            else:
                print(f"❌ FAILED - Expected 1 result, got {len(results)}")
                return False
            
            # Test 6: Not found returns empty list
            print("Test 6: Not found (empty list)...", end=" ")
            results = collection.find_by_author("Isaac Asimov")
            if len(results) == 0 and isinstance(results, list):
                print("✅ PASSED")
            else:
                print(f"❌ FAILED - Expected empty list, got {results}")
                return False
            
            return True
            
        finally:
            books.DATA_FILE = original_data_file

if __name__ == "__main__":
    print("=" * 60)
    print("Testing find_by_author validation")
    print("=" * 60)
    success = test_validation()
    print("=" * 60)
    if success:
        print("✅ All validation tests PASSED!")
        sys.exit(0)
    else:
        print("❌ Some tests FAILED!")
        sys.exit(1)
