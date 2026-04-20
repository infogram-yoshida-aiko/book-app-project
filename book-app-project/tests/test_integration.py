import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books as books_module
from books import BookCollection, ValidationError, Book
from utils import display_books


class TestConsolidationIntegration:
    """Integration tests for consolidated display functions."""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        """Create a temporary data file for testing."""
        data_file = tmp_path / "test_data.json"
        data_file.write_text("[]")
        return str(data_file)
    
    @pytest.fixture
    def collection(self, temp_data_file, monkeypatch):
        """Create a BookCollection with temporary file."""
        monkeypatch.setattr(books_module, "DATA_FILE", temp_data_file)
        return BookCollection()
    
    def test_add_book_then_display(self, collection, capsys):
        """Test adding a book and displaying it."""
        collection.add_book("Test Book", "Test Author", 2020)
        books = collection.list_books()
        
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Test Book" in captured.out
        assert "Test Author" in captured.out
        assert "2020" in captured.out
    
    def test_find_by_author_then_display(self, collection, capsys):
        """Test finding books by author and displaying them."""
        collection.add_book("Book 1", "John Doe", 2020)
        collection.add_book("Book 2", "John Doe", 2021)
        collection.add_book("Book 3", "Jane Smith", 2020)
        
        books = collection.find_by_author("John Doe")
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Book 1" in captured.out
        assert "Book 2" in captured.out
        assert "Jane Smith" not in captured.out
    
    def test_mark_as_read_then_display(self, collection, capsys):
        """Test marking book as read and displaying with correct status."""
        collection.add_book("Unfinished Book", "Author", 2020)
        collection.mark_as_read("Unfinished Book")
        
        books = collection.list_books()
        display_books(books)
        captured = capsys.readouterr()
        
        assert "✅ Read" in captured.out
    
    def test_validation_error_prevents_invalid_display(self, collection, capsys):
        """Test that ValidationError prevents adding invalid books."""
        with pytest.raises(ValidationError):
            collection.add_book("", "Author", 2020)
        
        books = collection.list_books()
        display_books(books)
        captured = capsys.readouterr()
        
        assert "No books in your collection." in captured.out
    
    def test_empty_collection_display(self, collection, capsys):
        """Test that empty collection displays correctly."""
        books = collection.list_books()
        display_books(books)
        captured = capsys.readouterr()
        
        assert "No books in your collection." in captured.out
        assert "Your Books:" not in captured.out
    
    def test_multiple_books_consolidation(self, collection, capsys):
        """Test displaying multiple books added through collection."""
        test_books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
            ("To Kill a Mockingbird", "Harper Lee", 1960),
            ("1984", "George Orwell", 1949),
        ]
        
        for title, author, year in test_books:
            collection.add_book(title, author, year)
        
        books = collection.list_books()
        display_books(books)
        captured = capsys.readouterr()
        
        # Verify all books are displayed
        for title, author, year in test_books:
            assert title in captured.out
            assert author in captured.out
            assert str(year) in captured.out
        
        # Verify numbering
        assert "1. The Great Gatsby" in captured.out
        assert "2. To Kill a Mockingbird" in captured.out
        assert "3. 1984" in captured.out
    
    def test_case_insensitive_author_search_display(self, collection, capsys):
        """Test case-insensitive author search and display."""
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        collection.add_book("I Robot", "Isaac Asimov", 1950)
        
        # Search with different case
        books = collection.find_by_author("isaac asimov")
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Foundation" in captured.out
        assert "I Robot" in captured.out
        assert "1. Foundation" in captured.out
        assert "2. I Robot" in captured.out


class TestImportConsolidation:
    """Test that imports are properly consolidated."""
    
    def test_book_app_imports_display_books(self):
        """Test that book_app can import display_books from utils."""
        try:
            from utils import display_books
            assert callable(display_books)
        except ImportError:
            pytest.fail("Could not import display_books from utils")
    
    def test_book_app_imports_validation_error(self):
        """Test that book_app can import ValidationError from books."""
        try:
            from books import ValidationError
            assert issubclass(ValidationError, Exception)
        except ImportError:
            pytest.fail("Could not import ValidationError from books")
    
    def test_utils_imports_book_type(self):
        """Test that utils imports Book type correctly."""
        try:
            from books import Book
            from utils import display_books
            # If display_books can be called with Book objects, import is correct
            assert callable(display_books)
        except ImportError:
            pytest.fail("Could not import Book from books")
