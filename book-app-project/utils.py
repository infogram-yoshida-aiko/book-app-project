import logging
from typing import List
from books import Book

logger = logging.getLogger(__name__)


def print_menu() -> None:
    """Display the main menu."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Get user's menu choice with validation (1-5 only).
    
    Repeatedly prompts the user until a valid menu option (1-5) is entered.
    Logs invalid choices for debugging. Returns immediately upon valid input.
    
    Returns:
        str: User's choice as a string ("1", "2", "3", "4", or "5")
    
    Examples:
        >>> # User enters: "6" then "3"
        >>> choice = get_user_choice()
        # Output: "Please enter a number between 1 and 5."
        >>> choice
        '3'
    """
    valid_choices = {"1", "2", "3", "4", "5"}
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if choice in valid_choices:
            return choice
        # ✅ Log invalid attempts for security/debugging
        logger.warning(f"Invalid menu choice attempted: {choice!r}")
        print("❌ Please enter a number between 1 and 5.")


def get_book_details() -> tuple[str, str, int]:
    """Collect book details from user input.
    
    Prompts for title, author, and publication year. Year input is validated
    and converted to integer before returning. Invalid year input raises
    ValueError instead of using a dangerous default value.
    
    Returns:
        tuple[str, str, int]: (title, author, year)
    
    Raises:
        ValueError: If year input cannot be parsed as a valid integer.
    
    Examples:
        >>> # User enters: "1984", "George Orwell", "1949"
        >>> title, author, year = get_book_details()
        >>> (title, author, year)
        ('1984', 'George Orwell', 1949)
    """
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError as e:
        # ✅ Fail Fast: 例外を発生させる（デフォルト値を返さない）
        # ✅ Exception chaining: 元の例外情報を保持
        logger.error(f"Year parsing failed for input: {year_input!r}")
        raise ValueError(
            f"Year must be a valid number. Got: {year_input!r}"
        ) from e

    return title, author, year


def display_books(books: List[Book]) -> None:
    """Display a list of books with formatted output.
    
    Prints all books in the collection with read status. Handles output
    errors gracefully (e.g., if stdout is closed or redirected improperly).
    Does nothing if the book list is empty.
    
    Args:
        books: List of Book objects to display
    
    Raises:
        IOError: If output cannot be written to stdout
    
    Examples:
        >>> from books import Book
        >>> books = [Book("1984", "George Orwell", 1949, read=False)]
        >>> display_books(books)
        Your Books:
        1. 1984 by George Orwell (1949) - 📖 Unread
    """
    if not books:
        print("No books in your collection.")
        return

    try:
        print("\nYour Books:")
        for index, book in enumerate(books, start=1):
            status = "✅ Read" if book.read else "📖 Unread"
            print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
        print()
    except IOError as e:
        # ✅ Log IO errors explicitly
        logger.error(f"Failed to display books: {e}")
        raise
