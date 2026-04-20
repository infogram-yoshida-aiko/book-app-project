"""Comprehensive test suite for BookCollection class.

This module provides extensive testing for the BookCollection class,
including integration tests, fixture-based setup, and parametrized tests
for various scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection, ValidationError, Book


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    """Create a temporary data file for testing."""
    temp_file = tmp_path / "test_data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    return str(temp_file)


@pytest.fixture
def empty_collection(temp_data_file):
    """Create an empty BookCollection."""
    return BookCollection()


@pytest.fixture
def sample_collection(temp_data_file):
    """Create a BookCollection with sample books.
    
    Books:
    - 1984 by George Orwell (1949)
    - Dune by Frank Herbert (1965)
    - Foundation by Isaac Asimov (1951)
    - Animal Farm by George Orwell (1945)
    """
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    return collection


@pytest.fixture
def collection_with_read_books(temp_data_file):
    """Create a collection with some books marked as read."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    
    collection.mark_as_read("1984")
    collection.mark_as_read("Dune")
    
    return collection


# =============================================================================
# BookCollection Initialization Tests
# =============================================================================

class TestBookCollectionInitialization:
    """Test BookCollection initialization and loading."""
    
    def test_init_creates_empty_collection(self, empty_collection):
        """Test that __init__ creates an empty collection when no data exists.
        
        Why: Collection should start empty if data file is empty.
        """
        assert empty_collection.books == []
        assert isinstance(empty_collection.books, list)
    
    def test_init_type_of_books_attribute(self, empty_collection):
        """Test that books attribute is a list."""
        assert hasattr(empty_collection, 'books')
        assert isinstance(empty_collection.books, list)
    
    def test_load_books_empty_file(self, empty_collection):
        """Test loading from an empty JSON file."""
        assert len(empty_collection.books) == 0
    
    def test_load_books_persists_on_init(self, temp_data_file):
        """Test that books are loaded on initialization.
        
        Why: Books added by one instance should be available to new instances.
        """
        # First instance: add a book
        collection1 = BookCollection()
        collection1.add_book("Test Book", "Test Author", 2020)
        
        # Second instance: books should be loaded
        collection2 = BookCollection()
        assert len(collection2.books) == 1
        assert collection2.books[0].title == "Test Book"


# =============================================================================
# Add Book Tests
# =============================================================================

class TestAddBook:
    """Test add_book() method."""
    
    def test_add_book_success(self, empty_collection):
        """Test adding a valid book.
        
        Why: Basic functionality - should add book and return Book object.
        """
        book = empty_collection.add_book("Test Book", "Test Author", 2020)
        
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.year == 2020
        assert book.read is False
        assert book in empty_collection.books
    
    def test_add_book_multiple(self, empty_collection):
        """Test adding multiple books.
        
        Why: Collection should handle multiple additions without loss.
        """
        book1 = empty_collection.add_book("Book 1", "Author 1", 2019)
        book2 = empty_collection.add_book("Book 2", "Author 2", 2020)
        book3 = empty_collection.add_book("Book 3", "Author 3", 2021)
        
        assert len(empty_collection.books) == 3
        assert book1 in empty_collection.books
        assert book2 in empty_collection.books
        assert book3 in empty_collection.books
    
    def test_add_book_persists_to_disk(self, temp_data_file):
        """Test that added books are persisted to disk.
        
        Why: Data must survive session reload.
        """
        collection1 = BookCollection()
        collection1.add_book("Persisted Book", "Author", 2020)
        
        # New instance loads from disk
        collection2 = BookCollection()
        assert len(collection2.books) == 1
        assert collection2.books[0].title == "Persisted Book"
    
    @pytest.mark.parametrize("title,author,year", [
        ("Title 1", "Author 1", 1949),
        ("Title 2", "Author 2", 1965),
        ("Title 3", "Author 3", 2026),
        ("Very Long Title" * 10, "Very Long Author", 1000),
    ])
    def test_add_book_various_valid_inputs(self, empty_collection, title, author, year):
        """Test adding books with various valid inputs.
        
        Why: Ensure function handles various input patterns.
        """
        book = empty_collection.add_book(title, author, year)
        assert book.title == title
        assert book.author == author
        assert book.year == year
        assert book in empty_collection.books
    
    def test_add_book_empty_title_raises_error(self, empty_collection):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            empty_collection.add_book("", "Author", 2020)
    
    def test_add_book_empty_author_raises_error(self, empty_collection):
        """Test that empty author raises ValidationError."""
        with pytest.raises(ValidationError, match="Author cannot be empty"):
            empty_collection.add_book("Title", "", 2020)
    
    def test_add_book_whitespace_only_title_raises_error(self, empty_collection):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            empty_collection.add_book("   ", "Author", 2020)
    
    def test_add_book_invalid_year_too_old(self, empty_collection):
        """Test that year < 1000 raises ValidationError."""
        with pytest.raises(ValidationError, match="Year must be between"):
            empty_collection.add_book("Title", "Author", 999)
    
    def test_add_book_invalid_year_future(self, empty_collection):
        """Test that future year raises ValidationError.
        
        Why: We don't allow books published in the future.
        """
        from datetime import datetime
        future_year = datetime.now().year + 1
        
        with pytest.raises(ValidationError, match="Year must be between"):
            empty_collection.add_book("Title", "Author", future_year)
    
    def test_add_book_year_not_integer(self, empty_collection):
        """Test that non-integer year raises ValidationError."""
        with pytest.raises(ValidationError, match="Year must be an integer"):
            empty_collection.add_book("Title", "Author", "2020")
    
    def test_add_book_boundary_year_1000(self, empty_collection):
        """Test that year 1000 (minimum valid) is accepted.
        
        Why: Ensures lower boundary is inclusive.
        """
        book = empty_collection.add_book("Ancient Book", "Author", 1000)
        assert book.year == 1000
        assert book in empty_collection.books
    
    def test_add_book_boundary_year_current(self, empty_collection):
        """Test that current year is accepted.
        
        Why: Recently published books should be valid.
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        book = empty_collection.add_book("This Year Book", "Author", current_year)
        assert book.year == current_year
        assert book in empty_collection.books


# =============================================================================
# Find Book Tests
# =============================================================================

class TestFindBookByTitle:
    """Test find_book_by_title() method."""
    
    def test_find_book_exact_match(self, sample_collection):
        """Test finding book with exact title match."""
        book = sample_collection.find_book_by_title("1984")
        assert book is not None
        assert book.title == "1984"
        assert book.author == "George Orwell"
    
    def test_find_book_case_insensitive(self, sample_collection):
        """Test finding book with case-insensitive match.
        
        Why: Users should find books regardless of capitalization.
        """
        assert sample_collection.find_book_by_title("dune") is not None
        assert sample_collection.find_book_by_title("DUNE") is not None
        assert sample_collection.find_book_by_title("DuNe") is not None
    
    def test_find_book_with_whitespace(self, sample_collection):
        """Test finding book when input has whitespace.
        
        Why: Users might add accidental spaces when searching.
        """
        assert sample_collection.find_book_by_title("  Dune  ") is not None
        assert sample_collection.find_book_by_title("Dune  ") is not None
        assert sample_collection.find_book_by_title("  Dune") is not None
    
    def test_find_book_nonexistent(self, sample_collection):
        """Test finding nonexistent book returns None."""
        book = sample_collection.find_book_by_title("Nonexistent Book")
        assert book is None
    
    def test_find_book_empty_collection(self, empty_collection):
        """Test finding book in empty collection returns None."""
        book = empty_collection.find_book_by_title("Any Book")
        assert book is None
    
    def test_find_book_partial_match_not_found(self, sample_collection):
        """Test that partial matches are not found.
        
        Why: find_book_by_title should match exact titles only.
        """
        # "198" should not match "1984"
        book = sample_collection.find_book_by_title("198")
        assert book is None
    
    def test_find_book_returns_correct_object_reference(self, sample_collection):
        """Test that found book is the actual object from collection."""
        book = sample_collection.find_book_by_title("1984")
        assert book is sample_collection.books[0]


# =============================================================================
# Mark as Read Tests
# =============================================================================

class TestMarkAsRead:
    """Test mark_as_read() method."""
    
    def test_mark_as_read_success(self, sample_collection):
        """Test marking a book as read.
        
        Why: Should change read status and persist to disk.
        """
        result = sample_collection.mark_as_read("1984")
        
        assert result is True
        book = sample_collection.find_book_by_title("1984")
        assert book.read is True
    
    def test_mark_as_read_case_insensitive(self, sample_collection):
        """Test marking book as read with case variations."""
        result = sample_collection.mark_as_read("dune")
        
        assert result is True
        book = sample_collection.find_book_by_title("Dune")
        assert book.read is True
    
    def test_mark_as_read_with_whitespace(self, sample_collection):
        """Test marking book as read with whitespace in input."""
        result = sample_collection.mark_as_read("  Foundation  ")
        
        assert result is True
        book = sample_collection.find_book_by_title("Foundation")
        assert book.read is True
    
    def test_mark_as_read_nonexistent_book(self, sample_collection):
        """Test marking nonexistent book returns False."""
        result = sample_collection.mark_as_read("Nonexistent Book")
        assert result is False
    
    def test_mark_as_read_empty_collection(self, empty_collection):
        """Test marking book as read in empty collection returns False."""
        result = empty_collection.mark_as_read("Any Book")
        assert result is False
    
    def test_mark_as_read_persists_to_disk(self, temp_data_file):
        """Test that read status persists to disk.
        
        Why: Read status must survive session reload.
        """
        collection1 = BookCollection()
        collection1.add_book("Test Book", "Author", 2020)
        collection1.mark_as_read("Test Book")
        
        # New instance loads from disk
        collection2 = BookCollection()
        book = collection2.find_book_by_title("Test Book")
        assert book.read is True
    
    def test_mark_as_read_multiple_books(self, sample_collection):
        """Test marking multiple books as read."""
        sample_collection.mark_as_read("1984")
        sample_collection.mark_as_read("Dune")
        sample_collection.mark_as_read("Foundation")
        
        assert sample_collection.find_book_by_title("1984").read is True
        assert sample_collection.find_book_by_title("Dune").read is True
        assert sample_collection.find_book_by_title("Foundation").read is True
        assert sample_collection.find_book_by_title("Animal Farm").read is False


# =============================================================================
# Remove Book Tests
# =============================================================================

class TestRemoveBook:
    """Test remove_book() method."""
    
    def test_remove_book_success(self, sample_collection):
        """Test removing an existing book.
        
        Why: Should remove book and return True.
        """
        assert len(sample_collection.books) == 4
        result = sample_collection.remove_book("1984")
        
        assert result is True
        assert len(sample_collection.books) == 3
        assert sample_collection.find_book_by_title("1984") is None
    
    def test_remove_book_case_insensitive(self, sample_collection):
        """Test removing book with case variations."""
        result = sample_collection.remove_book("dune")
        
        assert result is True
        assert sample_collection.find_book_by_title("Dune") is None
    
    def test_remove_book_with_whitespace(self, sample_collection):
        """Test removing book with whitespace in input."""
        result = sample_collection.remove_book("  Foundation  ")
        
        assert result is True
        assert sample_collection.find_book_by_title("Foundation") is None
    
    def test_remove_book_nonexistent(self, sample_collection):
        """Test removing nonexistent book returns False."""
        initial_count = len(sample_collection.books)
        result = sample_collection.remove_book("Nonexistent Book")
        
        assert result is False
        assert len(sample_collection.books) == initial_count
    
    def test_remove_book_empty_collection(self, empty_collection):
        """Test removing book from empty collection returns False."""
        result = empty_collection.remove_book("Any Book")
        assert result is False
    
    def test_remove_book_empty_title_raises_error(self, sample_collection):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            sample_collection.remove_book("")
    
    def test_remove_book_whitespace_only_raises_error(self, sample_collection):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            sample_collection.remove_book("   ")
    
    def test_remove_book_persists_to_disk(self, temp_data_file):
        """Test that removal persists to disk.
        
        Why: Removed books must stay removed after reload.
        """
        collection1 = BookCollection()
        collection1.add_book("Test Book", "Author", 2020)
        collection1.remove_book("Test Book")
        
        # New instance loads from disk
        collection2 = BookCollection()
        assert len(collection2.books) == 0
        assert collection2.find_book_by_title("Test Book") is None
    
    def test_remove_book_prints_message_on_not_found(self, sample_collection, capsys):
        """Test that helpful message is printed when book not found.
        
        Why: Users should see why the operation failed.
        """
        result = sample_collection.remove_book("Nonexistent")
        
        assert result is False
        captured = capsys.readouterr()
        assert "Book not found" in captured.out
        assert "Nonexistent" in captured.out


# =============================================================================
# List Books Tests
# =============================================================================

class TestListBooks:
    """Test list_books() method."""
    
    def test_list_books_empty_collection(self, empty_collection):
        """Test listing books in empty collection."""
        books_list = empty_collection.list_books()
        
        assert books_list == []
        assert isinstance(books_list, list)
    
    def test_list_books_returns_all_books(self, sample_collection):
        """Test that list_books returns all books in collection."""
        books_list = sample_collection.list_books()
        
        assert len(books_list) == 4
        titles = {book.title for book in books_list}
        assert titles == {"1984", "Dune", "Foundation", "Animal Farm"}
    
    def test_list_books_returns_internal_list(self, sample_collection):
        """Test that list_books returns the internal list reference.
        
        Why: Modifications to returned list affect collection.
        """
        books_list = sample_collection.list_books()
        assert books_list is sample_collection.books
    
    def test_list_books_includes_all_attributes(self, sample_collection):
        """Test that returned books have all attributes."""
        books_list = sample_collection.list_books()
        
        for book in books_list:
            assert hasattr(book, 'title')
            assert hasattr(book, 'author')
            assert hasattr(book, 'year')
            assert hasattr(book, 'read')


# =============================================================================
# Find by Author Tests
# =============================================================================

class TestFindByAuthor:
    """Test find_by_author() method."""
    
    def test_find_by_author_exact_match(self, sample_collection):
        """Test finding books by exact author name match."""
        books_list = sample_collection.find_by_author("George Orwell")
        
        assert len(books_list) == 2
        titles = {book.title for book in books_list}
        assert titles == {"1984", "Animal Farm"}
    
    def test_find_by_author_case_insensitive(self, sample_collection):
        """Test finding books by author with case variations."""
        books1 = sample_collection.find_by_author("george orwell")
        books2 = sample_collection.find_by_author("GEORGE ORWELL")
        books3 = sample_collection.find_by_author("George Orwell")
        
        assert len(books1) == 2
        assert len(books2) == 2
        assert len(books3) == 2
    
    def test_find_by_author_partial_match(self, sample_collection):
        """Test finding books by partial author name.
        
        Why: Users might search for last name only.
        """
        books_list = sample_collection.find_by_author("Orwell")
        assert len(books_list) == 2
    
    def test_find_by_author_no_match(self, sample_collection):
        """Test finding books with nonexistent author."""
        books_list = sample_collection.find_by_author("Unknown Author")
        assert books_list == []
    
    def test_find_by_author_empty_collection(self, empty_collection):
        """Test finding by author in empty collection."""
        books_list = empty_collection.find_by_author("Any Author")
        assert books_list == []
    
    def test_find_by_author_single_match(self, sample_collection):
        """Test finding books when only one matches."""
        books_list = sample_collection.find_by_author("Frank Herbert")
        
        assert len(books_list) == 1
        assert books_list[0].title == "Dune"


# =============================================================================
# Load/Save Persistence Tests
# =============================================================================

class TestLoadSavePersistence:
    """Test load_books() and save_books() methods."""
    
    def test_load_books_from_existing_file(self, temp_data_file):
        """Test loading books from existing data file.
        
        Why: Collection should load persisted data on init.
        """
        collection1 = BookCollection()
        collection1.add_book("Book 1", "Author 1", 2020)
        collection1.add_book("Book 2", "Author 2", 2021)
        
        # Load in new instance
        collection2 = BookCollection()
        assert len(collection2.books) == 2
    
    def test_save_books_updates_file(self, temp_data_file):
        """Test that save_books updates the data file."""
        collection = BookCollection()
        collection.add_book("Test Book", "Test Author", 2020)
        
        # Verify file was updated
        import json
        with open(temp_data_file, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]['title'] == "Test Book"
    
    def test_reload_books_after_external_change(self, temp_data_file):
        """Test reloading books after external file modification.
        
        Why: load_books can be called manually to sync external changes.
        """
        collection = BookCollection()
        collection.add_book("Book 1", "Author", 2020)
        
        # Manually add to file
        import json
        with open(temp_data_file, 'w') as f:
            json.dump([
                {"title": "Book 1", "author": "Author", "year": 2020, "read": False},
                {"title": "Book 2", "author": "Author", "year": 2021, "read": False}
            ], f)
        
        # Reload
        collection.load_books()
        assert len(collection.books) == 2


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for BookCollection workflows."""
    
    def test_workflow_add_find_mark_remove(self, empty_collection):
        """Test complete workflow: add, find, mark, remove.
        
        Why: Ensures all operations work together correctly.
        """
        # Add books
        book1 = empty_collection.add_book("1984", "Orwell", 1949)
        book2 = empty_collection.add_book("Dune", "Herbert", 1965)
        assert len(empty_collection.books) == 2
        
        # Find book
        found = empty_collection.find_book_by_title("1984")
        assert found == book1
        assert found.read is False
        
        # Mark as read
        result = empty_collection.mark_as_read("1984")
        assert result is True
        assert found.read is True
        
        # Remove book
        result = empty_collection.remove_book("Dune")
        assert result is True
        assert len(empty_collection.books) == 1
    
    def test_workflow_multiple_authors_same_book(self, empty_collection):
        """Test handling books with same title by different authors.
        
        Why: Multiple authors may write books with same title.
        """
        empty_collection.add_book("Frankenstein", "Mary Shelley", 1818)
        empty_collection.add_book("Frankenstein", "Dean Koontz", 2004)
        
        assert len(empty_collection.books) == 2
        
        # find_book_by_title returns first match
        book = empty_collection.find_book_by_title("Frankenstein")
        assert book.author == "Mary Shelley"
        
        # find_by_author returns both
        books = empty_collection.find_by_author("Frankenstein")
        # Should return empty (not an author name)
        assert books == []
    
    def test_workflow_persistence_across_sessions(self, temp_data_file):
        """Test data persistence across multiple instances.
        
        Why: Collection should preserve state between sessions.
        """
        # Session 1
        collection1 = BookCollection()
        collection1.add_book("Book 1", "Author 1", 2019)
        collection1.add_book("Book 2", "Author 2", 2020)
        collection1.mark_as_read("Book 1")
        
        # Session 2
        collection2 = BookCollection()
        assert len(collection2.books) == 2
        
        book1 = collection2.find_book_by_title("Book 1")
        assert book1.read is True
        
        book2 = collection2.find_book_by_title("Book 2")
        assert book2.read is False
        
        # Session 3: remove and add
        collection2.remove_book("Book 2")
        collection2.add_book("Book 3", "Author 3", 2021)
        
        # Session 4: verify
        collection3 = BookCollection()
        assert len(collection3.books) == 2
        assert collection3.find_book_by_title("Book 2") is None
        assert collection3.find_book_by_title("Book 3") is not None
    
    def test_workflow_statistics(self, collection_with_read_books):
        """Test generating statistics from collection.
        
        Why: Real applications need to query collection state.
        """
        all_books = collection_with_read_books.list_books()
        read_count = sum(1 for book in all_books if book.read)
        unread_count = sum(1 for book in all_books if not book.read)
        
        assert len(all_books) == 3
        assert read_count == 2
        assert unread_count == 1
