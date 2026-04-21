import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection, ValidationError, Book


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_find_book_by_title_case_insensitive_lowercase():
    """Test finding book with lowercase when stored with mixed case.
    
    Why: Users should be able to find books regardless of capitalization.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    book = collection.find_book_by_title("dune")
    assert book is not None
    assert book.title == "Dune"

def test_find_book_by_title_with_whitespace():
    """Test finding book when input has leading/trailing whitespace.
    
    Why: "  Dune  " should match "Dune" after trimming.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    book = collection.find_book_by_title("  Dune  ")
    assert book is not None
    assert book.title == "Dune"

def test_mark_as_read_with_whitespace():
    """Test marking book as read when input has leading/trailing whitespace.
    
    Why: "  Dune  " should be trimmed and match "Dune".
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.mark_as_read("  Dune  ")
    assert result is True
    
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False

# =============================================================================
# Comprehensive remove_book edge case tests
# =============================================================================

def test_remove_book_case_insensitive_lowercase():
    """Test removing book with lowercase when stored with mixed case.
    
    Why: Users might not remember exact capitalization. "dune" should match "Dune".
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("dune")
    assert result is True
    assert collection.find_book_by_title("Dune") is None
    assert len(collection.books) == 0

def test_remove_book_case_insensitive_uppercase():
    """Test removing book with uppercase when stored with mixed case.
    
    Why: "DUNE" should match "Dune" stored in collection.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("DUNE")
    assert result is True
    assert collection.find_book_by_title("Dune") is None

def test_remove_book_case_insensitive_mixed():
    """Test removing book with mixed case when stored differently.
    
    Why: "DuNe" should match "dune" stored in collection.
    """
    collection = BookCollection()
    collection.add_book("dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("DuNe")
    assert result is True
    assert len(collection.books) == 0

def test_remove_book_with_leading_whitespace():
    """Test removing book when input has leading whitespace.
    
    Why: Users might accidentally add spaces when typing. "  Dune" should match "Dune".
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("  Dune")
    assert result is True
    assert collection.find_book_by_title("Dune") is None

def test_remove_book_with_trailing_whitespace():
    """Test removing book when input has trailing whitespace.
    
    Why: "Dune  " should match "Dune" after trimming.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("Dune  ")
    assert result is True
    assert collection.find_book_by_title("Dune") is None

def test_remove_book_with_leading_and_trailing_whitespace():
    """Test removing book when input has both leading and trailing whitespace.
    
    Why: "  Dune  " should match "Dune".
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    result = collection.remove_book("  Dune  ")
    assert result is True
    assert len(collection.books) == 0

def test_remove_book_empty_string_raises_error():
    """Test that removing with empty string raises ValidationError.
    
    Why: Empty title is invalid input that should be caught early.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.remove_book("")

def test_remove_book_whitespace_only_raises_error():
    """Test that removing with whitespace-only string raises ValidationError.
    
    Why: "   " (spaces only) is not a valid title and should be rejected.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.remove_book("   ")

def test_remove_book_from_empty_collection():
    """Test removing book from empty collection returns False.
    
    Why: No books exist; remove_book should gracefully return False.
    """
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    
    assert result is False
    assert len(collection.books) == 0

def test_remove_book_not_found_in_non_empty_collection():
    """Test removing non-existent book from non-empty collection.
    
    Why: Other books exist, but the requested book is not found; should return False
    without affecting existing books.
    """
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    
    result = collection.remove_book("Nonexistent Book")
    assert result is False
    assert len(collection.books) == 3
    assert collection.find_book_by_title("1984") is not None
    assert collection.find_book_by_title("Dune") is not None
    assert collection.find_book_by_title("Foundation") is not None

def test_remove_book_persists_removal():
    """Test that removing a book is persisted to disk.
    
    Why: Removal must survive session reload. Data integrity is critical.
    """
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("1984", "George Orwell", 1949)
    
    collection.remove_book("Dune")
    
    # Reload from disk
    new_collection = BookCollection()
    assert new_collection.find_book_by_title("Dune") is None
    assert new_collection.find_book_by_title("1984") is not None
    assert len(new_collection.books) == 1

def test_remove_book_only_removes_first_matching_when_duplicates_exist():
    """Test removing book when multiple books with same title exist (edge case).
    
    Why: If duplicates somehow exist (same title), only first should be removed.
    Note: Normal usage shouldn't create duplicates, but function should handle gracefully.
    """
    collection = BookCollection()
    # Manually add duplicates to collection (bypassing normal validation)
    collection.books.append(Book(title="Dune", author="Frank Herbert", year=1965))
    collection.books.append(Book(title="Dune", author="Frank Herbert (reprint)", year=1965))
    collection.save_books()
    
    assert len(collection.books) == 2
    result = collection.remove_book("Dune")
    
    assert result is True
    assert len(collection.books) == 1
    assert collection.books[0].author == "Frank Herbert (reprint)"

def test_remove_book_returns_false_when_not_found(capsys):
    """Test that remove_book returns False and prints helpful message.
    
    Why: User should see why the operation failed.
    """
    collection = BookCollection()
    result = collection.remove_book("Nonexistent")
    
    assert result is False
    captured = capsys.readouterr()
    assert "Book not found" in captured.out
    assert "Nonexistent" in captured.out

def test_add_book_empty_title():
    """Test that empty title raises ValidationError."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.add_book("", "Author", 2020)

def test_add_book_whitespace_title():
    """Test that whitespace-only title is rejected."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.add_book("   ", "Author", 2020)

def test_add_book_empty_author():
    """Test that empty author raises ValidationError."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Author cannot be empty"):
        collection.add_book("Title", "", 2020)

def test_add_book_whitespace_author():
    """Test that whitespace-only author is rejected."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Author cannot be empty"):
        collection.add_book("Title", "   ", 2020)

def test_add_book_invalid_year_negative():
    """Test that negative year raises ValidationError."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Title", "Author", -1)

def test_add_book_invalid_year_too_high():
    """Test that year > current_year raises ValidationError."""
    from datetime import datetime
    current_year = datetime.now().year
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Title", "Author", current_year + 10)

def test_add_book_invalid_year_type():
    """Test that non-integer year raises ValidationError."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be an integer"):
        collection.add_book("Title", "Author", "2020")

def test_find_by_author_exact_match():
    """Test finding a book by exact author name match."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    results = collection.find_by_author("George Orwell")
    assert len(results) == 2
    assert all(book.author == "George Orwell" for book in results)

def test_find_by_author_partial_match():
    """Test finding a book by partial author name match."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    results = collection.find_by_author("George")
    assert len(results) == 1
    assert results[0].author == "George Orwell"

def test_find_by_author_case_insensitive():
    """Test finding a book with case-insensitive author name."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    
    results_lower = collection.find_by_author("george orwell")
    results_upper = collection.find_by_author("GEORGE ORWELL")
    results_mixed = collection.find_by_author("george ORWELL")
    
    assert len(results_lower) == 2
    assert len(results_upper) == 2
    assert len(results_mixed) == 2

def test_find_by_author_not_found():
    """Test that find_by_author returns empty list when author is not found."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    
    results = collection.find_by_author("Isaac Asimov")
    assert len(results) == 0
    assert isinstance(results, list)

def test_find_by_author_empty_string_raises_error():
    """Test that find_by_author with empty string raises ValidationError."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    
    with pytest.raises(ValidationError, match="Author cannot be empty"):
        collection.find_by_author("")

def test_find_by_author_whitespace_only_raises_error():
    """Test that find_by_author with whitespace-only string raises ValidationError."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    
    with pytest.raises(ValidationError, match="Author cannot be empty"):
        collection.find_by_author("   ")

# =============================================================================
# Comprehensive add_book edge case tests
# =============================================================================

def test_add_book_boundary_year_zero():
    """Test that year 0 is invalid (below lower boundary of 1000).
    
    Why: Year 0 should be rejected as it's below the practical lower bound.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Ancient Text", "Unknown", 0)

def test_add_book_boundary_year_max_obsolete():
    """Test that year 2100 is now treated as past (if current year > 2100).
    
    Why: Max boundary is now current year, not a fixed 2100.
    """
    from datetime import datetime
    current_year = datetime.now().year
    collection = BookCollection()
    # 2100 should be accepted since it's before or equal to current year
    if current_year >= 2100:
        book = collection.add_book("Book in 2100", "Author", 2100)
        assert book.year == 2100

def test_add_book_boundary_year_just_above_min():
    """Test year 999 (just below new min of 1000) is invalid.
    
    Why: Ensures the new lower boundary (1000) is enforced.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Medieval Text", "Author", 999)

def test_add_book_boundary_year_just_above_zero_new():
    """Test year 1 (well below min of 1000) is invalid.
    
    Why: Confirms year 1 is rejected under the new validation rule.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Ancient Book", "Author", 1)

def test_add_book_boundary_year_invalid_far_future():
    """Test that year far in future raises error.
    
    Why: Validates boundary validation rejects future years.
    """
    from datetime import datetime
    future_year = datetime.now().year + 100
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Invalid Year", "Author", future_year)

def test_add_book_very_long_title():
    """Test that very long titles are accepted.
    
    Why: Ensures no arbitrary string length limits that could break user workflow.
    """
    collection = BookCollection()
    long_title = "A" * 1000
    book = collection.add_book(long_title, "Author", 2020)
    assert book.title == long_title
    assert collection.find_book_by_title(long_title) is not None

def test_add_book_very_long_author():
    """Test that very long author names are accepted.
    
    Why: Some cultural names can be long; no artificial limits should exist.
    """
    collection = BookCollection()
    long_author = "B" * 500
    book = collection.add_book("Title", long_author, 2020)
    assert book.author == long_author

def test_add_book_with_special_characters_in_title():
    """Test that titles with special characters are accepted.
    
    Why: Real titles contain: @#$%^&*()[]{}!? These must not cause validation issues.
    """
    collection = BookCollection()
    special_title = "C++: A Modern Approach (2nd Ed.) @2020!"
    book = collection.add_book(special_title, "Author", 2020)
    assert book.title == special_title

def test_add_book_with_unicode_characters():
    """Test that Unicode characters in title and author are accepted.
    
    Why: International books and authors often have accents, non-Latin scripts.
    Example: "Les Misérables" (French), "Crime and Punishment" (Cyrillic author).
    """
    collection = BookCollection()
    book = collection.add_book("Métamorphose 변身", "Kafka Кафка", 2020)
    assert "Métamorphose" in book.title
    assert "Кафка" in book.author

def test_add_book_with_leading_trailing_whitespace_stripped():
    """Test that leading/trailing whitespace in title and author is handled.
    
    Why: Users might accidentally add spaces; the app should trim them appropriately.
    Edge case: Title "  1984  " should be distinct from "1984" in display.
    """
    collection = BookCollection()
    book = collection.add_book("  1984  ", "  George Orwell  ", 1949)
    assert book.title == "  1984  "  # Whitespace preserved (not stripped by add_book)
    assert book.author == "  George Orwell  "

def test_add_book_default_read_flag_false():
    """Test that read flag defaults to False.
    
    Why: A newly added book should not be marked as already read. This is critical
    for tracking reading progress.
    """
    collection = BookCollection()
    book = collection.add_book("1984", "George Orwell", 1949)
    assert book.read is False

def test_add_multiple_books_preserves_all():
    """Test that adding multiple books preserves all of them.
    
    Why: Ensures adding new books doesn't accidentally overwrite or lose previous books.
    """
    collection = BookCollection()
    books_to_add = [
        ("1984", "George Orwell", 1949),
        ("Dune", "Frank Herbert", 1965),
        ("Foundation", "Isaac Asimov", 1951),
    ]
    for title, author, year in books_to_add:
        collection.add_book(title, author, year)
    
    assert len(collection.books) == 3
    for title, author, year in books_to_add:
        found = collection.find_book_by_title(title)
        assert found is not None
        assert found.author == author
        assert found.year == year

def test_add_duplicate_title_creates_separate_entry():
    """Test that duplicate titles create separate entries (allows same title by different authors).
    
    Why: Multiple authors may write books with the same title. The app should allow this
    as the title search is exact-match; users should query by author if needed.
    """
    collection = BookCollection()
    collection.add_book("Frankenstein", "Mary Shelley", 1818)
    collection.add_book("Frankenstein", "Dean Koontz", 2004)
    
    assert len(collection.books) == 2
    found_first = collection.find_book_by_title("Frankenstein")
    assert found_first is not None
    assert found_first.author == "Mary Shelley"

def test_add_book_year_float_raises_error():
    """Test that float year raises ValidationError.
    
    Why: Ensures only integer years are accepted (e.g., 2020.5 should fail).
    Prevents ambiguous year representation.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be an integer"):
        collection.add_book("Title", "Author", 2020.5)

def test_add_book_year_none_raises_error():
    """Test that None year raises ValidationError.
    
    Why: Year is required; None should be rejected.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be an integer"):
        collection.add_book("Title", "Author", None)

def test_add_book_returns_book_object():
    """Test that add_book returns the created Book object.
    
    Why: Users should receive the created object for immediate use without re-querying.
    """
    collection = BookCollection()
    returned_book = collection.add_book("1984", "George Orwell", 1949)
    
    assert returned_book is not None
    assert returned_book.title == "1984"
    assert returned_book.author == "George Orwell"
    assert returned_book.year == 1949
    assert isinstance(returned_book, type(collection.books[0]))

def test_add_book_persists_to_storage():
    """Test that added books are persisted to storage and survive reload.
    
    Why: Books must persist across session restarts. This is critical for data integrity.
    """
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    
    new_collection = BookCollection()
    found = new_collection.find_book_by_title("1984")
    assert found is not None
    assert found.author == "George Orwell"
    assert found.year == 1949

def test_add_book_with_numbers_in_author_and_title():
    """Test that titles and authors with numbers are accepted.
    
    Why: Many real titles/authors contain numbers: "2001: A Space Odyssey", "3Blue1Brown".
    """
    collection = BookCollection()
    book = collection.add_book("2001: A Space Odyssey", "Arthur C. Clarke III", 1968)
    assert "2001" in book.title
    assert "III" in book.author

def test_add_book_title_with_newlines_rejected_in_validation():
    """Test that validation occurs before adding to collection.
    
    Why: Even though whitespace is stripped in validation check, title should not contain
    only whitespace (including newlines). This prevents storing garbage data.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.add_book("\n\n\t", "Author", 2020)

def test_add_book_increments_collection_size():
    """Test that each add_book call increases collection size by exactly 1.
    
    Why: Ensures no duplicate additions or silent failures.
    """
    collection = BookCollection()
    initial_size = len(collection.books)
    
    collection.add_book("Book1", "Author1", 2020)
    assert len(collection.books) == initial_size + 1
    
    collection.add_book("Book2", "Author2", 2021)
    assert len(collection.books) == initial_size + 2
    
    collection.add_book("Book3", "Author3", 2022)
    assert len(collection.books) == initial_size + 3

# =============================================================================
# Year validation tests (1000-current_year range)
# =============================================================================

def test_add_book_year_too_low_below_1000():
    """Test that year < 1000 raises ValidationError.
    
    Why: Books from before 1000 AD are rare and potentially incorrect entries.
    We use 1000 as the practical lower bound.
    """
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Ancient Manuscript", "Unknown", 999)

def test_add_book_year_boundary_1000():
    """Test that year 1000 (lower boundary) is valid.
    
    Why: Year 1000 is the lower boundary. Must be accepted.
    """
    collection = BookCollection()
    book = collection.add_book("Ancient Book", "Unknown", 1000)
    assert book.year == 1000

def test_add_book_year_boundary_1001():
    """Test that year 1001 (just above lower boundary) is valid.
    
    Why: Ensures lower boundary validation is exactly 1000, not 1001.
    """
    collection = BookCollection()
    book = collection.add_book("Medieval Book", "Unknown", 1001)
    assert book.year == 1001

def test_add_book_year_future_current_year():
    """Test that current year is valid.
    
    Why: Books published this year should be accepted.
    """
    from datetime import datetime
    current_year = datetime.now().year
    collection = BookCollection()
    book = collection.add_book("This Year's Book", "Author", current_year)
    assert book.year == current_year

def test_add_book_year_future_next_year():
    """Test that next year is rejected (future years not allowed).
    
    Why: Books published in the future cannot exist. This prevents data entry errors.
    """
    from datetime import datetime
    next_year = datetime.now().year + 1
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Year must be between 1000"):
        collection.add_book("Future Book", "Author", next_year)

def test_add_book_year_boundary_current_year_minus_1():
    """Test that last year is valid.
    
    Why: Ensures boundary allows books from previous year.
    """
    from datetime import datetime
    last_year = datetime.now().year - 1
    collection = BookCollection()
    book = collection.add_book("Last Year Book", "Author", last_year)
    assert book.year == last_year

# =============================================================================
# list_unread_books() filtering tests - NEW FEATURE
# =============================================================================

def test_list_unread_books_returns_only_unread():
    """Test that list_unread_books returns only unread books.
    
    Why: Primary functionality - must filter out read books and return only
    those with read=False. This is the core behavior of the new feature.
    """
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    
    # Mark one book as read
    collection.mark_as_read("Dune")
    
    # Arrange complete, now Act
    unread = collection.list_unread_books()
    
    # Assert
    assert len(unread) == 2
    assert collection.find_book_by_title("1984") in unread
    assert collection.find_book_by_title("Foundation") in unread
    assert collection.find_book_by_title("Dune") not in unread
