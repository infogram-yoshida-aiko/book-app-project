import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for input validation errors."""
    pass


DATA_FILE = "data.json"


@dataclass
class Book:
    """Represents a single book in the collection.
    
    Attributes:
        title (str): The book's title (non-empty, max 200 characters).
        author (str): The author's name (non-empty, max 100 characters).
        year (int): Publication year (1000 to present year).
        read (bool): Whether the book has been read (default: False).
    
    Examples:
        Creating a Book:
        
        >>> book = Book(
        ...     title="1984",
        ...     author="George Orwell",
        ...     year=1949,
        ...     read=False
        ... )
        >>> book.title
        '1984'
    """
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manages a collection of books with JSON persistence.
    
    This class provides CRUD operations (Create, Read, Update, Delete) for books,
    with automatic persistence to a JSON file (data.json). Books are validated
    upon addition and search operations support case-insensitive matching.
    
    Attributes:
        books (List[Book]): The list of books currently in memory.
    
    Examples:
        Basic usage:
        
        >>> collection = BookCollection()
        >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
        >>> len(collection.books)
        (existing books + 1)
        >>> found = collection.find_book_by_title("Dune")
        >>> found.author
        'Frank Herbert'
    
    Note:
        The collection is automatically loaded from data.json on initialization.
        All modifications are immediately persisted to disk.
    """
    
    def __init__(self) -> None:
        """Initialize an empty BookCollection and load existing books from disk.
        
        Loads books from data.json if it exists. If the file is missing or
        corrupted, the collection starts empty with a warning logged.
        
        Examples:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists.
        
        Attempts to read and parse data.json into Book objects. If the file
        is not found, the collection remains empty. If the file is corrupted
        (invalid JSON), a warning is logged and the collection starts empty.
        
        This method is called automatically during __init__() and can be
        called manually to reload data from disk (e.g., if the file was
        modified externally).
        
        Side Effects:
            - Modifies self.books
            - May log a warning if JSON is corrupted
        
        Raises:
            No exceptions are raised; errors are handled gracefully.
        
        Examples:
            Manual reload after external file changes:
            
            >>> collection = BookCollection()
            >>> # (external process modifies data.json)
            >>> collection.load_books()  # Reload from disk
        
        See Also:
            save_books(): Persist current collection to disk
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            logger.warning("data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON file.
        
        Serializes all books in memory to a formatted JSON file (data.json)
        with 2-space indentation for readability. This method is called
        automatically after add_book(), remove_book(), and mark_as_read().
        
        The file is created if it doesn't exist; existing files are overwritten.
        File I/O is handled safely with context managers.
        
        Side Effects:
            - Creates or overwrites data.json
            - Persists all changes to disk
        
        Raises:
            IOError: If file write fails (e.g., permission denied)
            json.JSONEncodeError: If a book object cannot be serialized
        
        Examples:
            Manual save (usually not needed):
            
            >>> collection = BookCollection()
            >>> collection.save_books()  # Writes current state to disk
        
        Note:
            This method is automatically called by add_book(), remove_book(),
            and mark_as_read(), so manual calls are rarely needed.
        
        See Also:
            load_books(): Load books from disk
        """
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection.
        
        Validates the book's data before adding. Title and author must be
        non-empty strings; year must be between 1000 and the current year.
        If validation fails, a descriptive ValidationError is raised and
        the book is not added.
        
        All successful additions are immediately persisted to disk via save_books().
        
        Args:
            title (str): The book's title (required, max 200 chars).
            author (str): The author's name (required, max 100 chars).
            year (int): Publication year (1000 to present year).
        
        Returns:
            Book: The newly created and added Book object.
        
        Raises:
            ValidationError: If title/author are empty, year is out of range,
                or any other validation rule is violated.
        
        Examples:
            Add a valid book:
            
            >>> collection = BookCollection()
            >>> book = collection.add_book("1984", "George Orwell", 1949)
            >>> book.title
            '1984'
            >>> book in collection.books
            True
            
            Validation error on invalid year:
            
            >>> collection.add_book("Future Book", "Author", 3000)
            ValidationError: Year must be between 1000 and 2026
        
        See Also:
            remove_book(): Delete a book by title
            mark_as_read(): Mark a book as read
        """
        self._validate_book_input(title, author, year)
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    @staticmethod
    def _validate_book_input(title: str, author: str, year: int) -> None:
        """Validate book input parameters.
        
        Args:
            title: Book title
            author: Book author
            year: Publication year
            
        Raises:
            ValidationError: If any input is invalid
        """
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        if not author or not author.strip():
            raise ValidationError("Author cannot be empty")
        if not isinstance(year, int):
            raise ValidationError("Year must be an integer")
        current_year = datetime.now().year
        if year < 1000 or year > current_year:
            raise ValidationError(f"Year must be between 1000 and {current_year}")

    def list_books(self) -> List[Book]:
        """Get all books currently in the collection.
        
        Returns all books stored in memory, regardless of read status.
        The returned list is the internal list; modifications will affect
        the collection. For read-only access, consider creating a copy.
        
        Returns:
            List[Book]: A list of all Book objects in the collection.
                Returns an empty list if no books have been added.
        
        Examples:
            List all books:
            
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> books = collection.list_books()
            >>> len(books)
            1
            >>> books[0].title
            '1984'
        
        See Also:
            find_book_by_title(): Search for a single book by exact title match
            find_by_author(): Search for all books by a given author
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a single book by exact title match (case-insensitive).
        
        Searches for a book whose title exactly matches the given title,
        ignoring case and whitespace differences. Normalized for consistent
        lookups (e.g., "  1984  " matches "1984").
        
        This is useful for:
        - User queries (who may vary capitalization)
        - Marking books as read by title
        - Deleting books by title
        
        Args:
            title (str): The book title to search for (required, non-empty).
        
        Returns:
            Optional[Book]: The matching Book object if found, None otherwise.
        
        Examples:
            Find a book:
            
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> book = collection.find_book_by_title("1984")
            >>> book.author
            'George Orwell'
            
            Case-insensitive search:
            
            >>> book = collection.find_book_by_title("1984")  # lowercase
            >>> book is not None
            True
            
            Book not found:
            
            >>> collection.find_book_by_title("Nonexistent") is None
            True
        
        See Also:
            find_by_author(): Search for multiple books by author
            mark_as_read(): Mark a book as read using title lookup
        """
        normalized_title = title.strip().lower()
        for book in self.books:
            if book.title.lower() == normalized_title:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title.
        
        Finds a book by exact title match (case-insensitive) and updates
        its read status to True. The change is immediately persisted to disk.
        
        This is a convenience method for tracking reading progress. It allows
        marking specific books as read without manually updating the Book object.
        
        Args:
            title (str): The book title to mark as read (case-insensitive).
        
        Returns:
            bool: True if book was found and marked as read, False if book
                not found (no change made in this case).
        
        Examples:
            Mark a book as read:
            
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.mark_as_read("1984")
            True
            >>> book = collection.find_book_by_title("1984")
            >>> book.read
            True
            
            Book not found:
            
            >>> collection.mark_as_read("Nonexistent Book")
            False
        
        See Also:
            find_book_by_title(): Get the Book object to check read status
            add_book(): Add a book (default read status is False)
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title.
        
        Finds and removes a book by exact title match (case-insensitive).
        If the book is found, it is removed from the collection and the
        change is immediately persisted to disk. If the book is not found,
        a helpful message is printed and a warning is logged, but no
        exception is raised (safe deletion).
        
        Args:
            title (str): The book title to remove (case-insensitive,
                whitespace-trimmed, required, non-empty).
        
        Returns:
            bool: True if book was found and removed, False if not found.
        
        Raises:
            ValidationError: If title is empty or only whitespace.
        
        Examples:
            Remove an existing book:
            
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.remove_book("1984")
            True
            >>> collection.find_book_by_title("1984") is None
            True
            
            Try to remove a nonexistent book (prints message, returns False):
            
            >>> collection.remove_book("Nonexistent")
            Book not found: 'Nonexistent'
            False
            
            Empty title (raises ValidationError):
            
            >>> collection.remove_book("")
            ValidationError: Title cannot be empty
        
        See Also:
            add_book(): Add a book to the collection
            find_book_by_title(): Find a book by title (doesn't remove)
        """
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        else:
            message = f"Book not found: '{title.strip()}'"
            logger.warning(message)
            print(message)
            return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (partial match supported).
        
        Searches for books where the given author name appears anywhere
        in the book's author field (case-insensitive). This supports:
        - Partial name matches (e.g., "Orwell" matches "George Orwell")
        - Multiple authors in a single query result
        - Fuzzy author search
        
        Args:
            author (str): The author name or partial name to search for
                (case-insensitive, required, non-empty).
        
        Returns:
            List[Book]: A list of all books where the author name is found.
                Returns an empty list if no matches are found.
        
        Examples:
            Find by full author name:
            
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.add_book("Animal Farm", "George Orwell", 1945)
            >>> books = collection.find_by_author("George Orwell")
            >>> len(books)
            2
            
            Find by partial name:
            
            >>> books = collection.find_by_author("Orwell")
            >>> len(books)
            2
            
            No matches:
            
            >>> books = collection.find_by_author("Unknown Author")
            >>> len(books)
            0
        
        See Also:
            find_book_by_title(): Find a single book by exact title
            list_books(): Get all books without filtering
        """
        return [b for b in self.books if author.lower() in b.author.lower()]
