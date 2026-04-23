import sys
import logging
from books import BookCollection, ValidationError
from utils import display_books, get_book_details

logger = logging.getLogger(__name__)


# Global collection instance
collection = BookCollection()


def handle_list():
    """Display all books in the collection."""
    books = collection.list_books()
    display_books(books)


def handle_add():
    """Add a new book to the collection.
    
    Prompts user for book details (title, author, year) and adds to collection
    if validation passes. Handles both input parsing errors (ValueError) and
    business validation errors (ValidationError).
    """
    print("\nAdd a New Book\n")

    try:
        # ✅ Use dedicated input function with proper error handling
        title, author, year = get_book_details()
    except ValueError as e:
        # ✅ Specific error message for year parsing failure
        logger.warning(f"Year input parsing failed: {e}")
        print(f"\n❌ Error: {e}\n")
        return

    try:
        collection.add_book(title, author, year)
        print("\n✅ Book added successfully.\n")
    except ValidationError as e:
        # ✅ Business logic validation error (e.g., year out of range)
        logger.warning(f"Book validation failed: {e}")
        print(f"\n❌ Error: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    try:
        if collection.remove_book(title):
            print("\nBook removed successfully.\n")
        else:
            print(f"\n⚠️  Book not found: '{title}'\nPlease check the title spelling and try again.\n")
    except ValidationError as e:
        print(f"\nError: {e}\n")


def handle_find():
    """Find and display books by author."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    display_books(books)


def handle_unread():
    """Display all unread books in the collection."""
    books = collection.list_unread_books()
    display_books(books)


def show_help():
    """Display help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  unread   - Show unread books only
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "unread":
        handle_unread()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
