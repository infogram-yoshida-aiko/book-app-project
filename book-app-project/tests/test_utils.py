import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from io import StringIO
from books import Book
from utils import display_books, print_menu, get_book_details


class TestDisplayBooks:
    """Test suite for display_books function."""
    
    def test_display_books_empty_list(self, capsys):
        """Test display_books with empty list."""
        display_books([])
        captured = capsys.readouterr()
        assert "No books in your collection." in captured.out
    
    def test_display_books_single_book_unread(self, capsys):
        """Test display_books with single unread book."""
        books = [Book("1984", "George Orwell", 1949, read=False)]
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Your Books:" in captured.out
        assert "1984" in captured.out
        assert "George Orwell" in captured.out
        assert "1949" in captured.out
        assert "📖 Unread" in captured.out
    
    def test_display_books_single_book_read(self, capsys):
        """Test display_books with single read book."""
        books = [Book("Dune", "Frank Herbert", 1965, read=True)]
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Your Books:" in captured.out
        assert "Dune" in captured.out
        assert "Frank Herbert" in captured.out
        assert "1965" in captured.out
        assert "✅ Read" in captured.out
    
    def test_display_books_multiple_books_mixed_status(self, capsys):
        """Test display_books with multiple books of mixed read status."""
        books = [
            Book("The Hobbit", "J.R.R. Tolkien", 1937, read=True),
            Book("The Fellowship", "J.R.R. Tolkien", 1954, read=False),
            Book("The Two Towers", "J.R.R. Tolkien", 1954, read=True),
        ]
        display_books(books)
        captured = capsys.readouterr()
        
        assert "Your Books:" in captured.out
        assert "1. The Hobbit" in captured.out
        assert "2. The Fellowship" in captured.out
        assert "3. The Two Towers" in captured.out
        assert captured.out.count("✅ Read") == 2
        assert captured.out.count("📖 Unread") == 1
    
    def test_display_books_formatting(self, capsys):
        """Test that display_books formats output correctly."""
        books = [
            Book("Book A", "Author A", 2000, read=False),
            Book("Book B", "Author B", 2010, read=True),
        ]
        display_books(books)
        captured = capsys.readouterr()
        
        lines = captured.out.strip().split("\n")
        # Should have header, 2 book lines, and trailing newline
        assert "Your Books:" in lines[0]
        assert "1. Book A" in lines[1]
        assert "2. Book B" in lines[2]
    
    def test_display_books_with_special_characters(self, capsys):
        """Test display_books handles special characters in titles."""
        books = [Book("O'Brien's 1984 (2nd ed.)", "George Orwell", 1949, read=False)]
        display_books(books)
        captured = capsys.readouterr()
        
        assert "O'Brien's 1984 (2nd ed.)" in captured.out


class TestPrintMenu:
    """Test suite for print_menu function."""
    
    def test_print_menu_output(self, capsys):
        """Test print_menu displays all menu options."""
        print_menu()
        captured = capsys.readouterr()
        
        assert "📚 Book Collection App" in captured.out
        assert "1. Add a book" in captured.out
        assert "2. List books" in captured.out
        assert "3. Mark book as read" in captured.out
        assert "4. Remove a book" in captured.out
        assert "5. Exit" in captured.out


class TestGetBookDetails:
    """Test suite for get_book_details function."""
    
    def test_get_book_details_valid_input(self, monkeypatch):
        """Test get_book_details with valid input."""
        inputs = ["Test Book", "Test Author", "2020"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        
        title, author, year = get_book_details()
        
        assert title == "Test Book"
        assert author == "Test Author"
        assert year == 2020
    
    def test_get_book_details_with_spaces(self, monkeypatch):
        """Test get_book_details strips whitespace."""
        inputs = ["  Book Title  ", "  Author Name  ", "  2020  "]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        
        title, author, year = get_book_details()
        
        assert title == "Book Title"
        assert author == "Author Name"
        assert year == 2020
    
    def test_get_book_details_invalid_year_defaults_to_zero(self, monkeypatch, capsys):
        """Test get_book_details defaults to 0 for invalid year."""
        inputs = ["Title", "Author", "not_a_number"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        
        title, author, year = get_book_details()
        captured = capsys.readouterr()
        
        assert title == "Title"
        assert author == "Author"
        assert year == 0
        assert "Invalid year. Defaulting to 0." in captured.out
    
    def test_get_book_details_empty_year_defaults_to_zero(self, monkeypatch):
        """Test get_book_details handles empty year input."""
        inputs = ["Title", "Author", ""]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        
        title, author, year = get_book_details()
        
        assert year == 0
    
    def test_get_book_details_negative_year(self, monkeypatch):
        """Test get_book_details with negative year."""
        inputs = ["Title", "Author", "-100"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        
        title, author, year = get_book_details()
        
        assert year == -100


class TestDisplayBooksIntegration:
    """Integration tests for display_books function."""
    
    def test_display_books_preserves_book_data(self, capsys):
        """Test that display_books doesn't modify book data."""
        original_book = Book("Original Title", "Original Author", 2020, read=False)
        books = [original_book]
        
        display_books(books)
        
        # Verify book data wasn't modified
        assert original_book.title == "Original Title"
        assert original_book.author == "Original Author"
        assert original_book.year == 2020
        assert original_book.read is False
    
    def test_display_books_consistent_output_format(self, capsys):
        """Test that display_books produces consistent output format."""
        books = [Book("Test", "Author", 2020, read=True)]
        
        display_books(books)
        captured1 = capsys.readouterr()
        
        display_books(books)
        captured2 = capsys.readouterr()
        
        # Output should be identical for same input
        assert captured1.out == captured2.out
    
    def test_display_books_numbering_sequential(self, capsys):
        """Test that display_books numbers books sequentially."""
        books = [
            Book("Book 1", "Author", 2000, read=False),
            Book("Book 2", "Author", 2010, read=False),
            Book("Book 3", "Author", 2020, read=False),
            Book("Book 4", "Author", 2030, read=False),
        ]
        
        display_books(books)
        captured = capsys.readouterr()
        
        for i in range(1, 5):
            assert f"{i}. Book {i}" in captured.out
