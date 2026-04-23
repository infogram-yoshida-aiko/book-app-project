# Copilot Instructions for book-app-project

A Python CLI application for managing a personal book collection with robust error handling and production-quality code patterns.

## Quick Commands

### Run the Application
```bash
# Add a book
python book_app.py add

# List all books
python book_app.py list

# Find books by author
python book_app.py find

# Remove a book
python book_app.py remove

# Mark a book as read
python book_app.py read

# Show help
python book_app.py help
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_books.py -v

# Run a specific test
python -m pytest tests/test_books.py::test_add_book -v

# Run with coverage
python -m pytest tests/ --cov=books --cov=auth --cov=utils
```

## Architecture

The codebase follows a clean **three-layer architecture**:

```
book_app.py (CLI Layer)
    ├─ User input handling
    ├─ Command routing
    └─ Output formatting
         │
         ▼
books.py (Business Logic Layer)
    ├─ BookCollection (state management)
    ├─ Book dataclass (data model)
    ├─ Input validation
    └─ JSON persistence
         │
         ▼
data.json (Data Layer)
```

### Key Components

- **book_app.py**: CLI entry point with command handlers (handle_add, handle_list, etc.)
- **books.py**: Core domain logic with `BookCollection` and `Book` classes
- **auth.py**: User authentication with `AuthManager` and `User` classes
- **utils.py**: Helper functions for input/output (display_books, get_book_details)
- **tests/**: Full test suite with pytest

### Data Flow for Adding a Book

1. User runs `python book_app.py add`
2. `book_app.py` calls `handle_add()`
3. `handle_add()` calls `utils.get_book_details()` to gather input
4. Input is passed to `collection.add_book(title, author, year)`
5. `books.py` validates input via `_validate_book_input()`
6. If valid, `Book` object is created and added to list
7. `save_books()` persists to `data.json`
8. Success message displayed to user

### Error Handling Philosophy

- **Fail Fast**: Errors stop execution immediately; data never partially saved
- **User-Friendly Messages**: Clear, actionable error messages (not technical stack traces)
- **Validation Layers**: 
  - Input parsing in `utils.py` (type conversion)
  - Business validation in `books.py` (domain rules)
  - Exception chaining preserves root causes
- **Logging**: All errors logged to `logger` for debugging

## Key Conventions

### Custom Exceptions

Always use custom exceptions for domain logic, never bare exceptions:

```python
# Good
from books import ValidationError
raise ValidationError("Title cannot be empty")

# Bad
raise Exception("error")
```

### Validation Pattern

Validation happens in `books.py` before data modifications:

```python
def add_book(self, title: str, author: str, year: int) -> Book:
    # Validation first (raises ValidationError if invalid)
    self._validate_book_input(title, author, year)
    
    # Only then modify state
    book = Book(title=title, author=author, year=year)
    self.books.append(book)
    self.save_books()
    return book
```

### Docstring Format

Use Google-style docstrings with Args, Returns, Raises, and Examples sections:

```python
def find_by_author(self, author: str) -> List[Book]:
    """Find all books by a given author (partial match supported).
    
    Args:
        author (str): The author name or partial name to search for.
    
    Returns:
        List[Book]: A list of all matching books.
    
    Raises:
        ValidationError: If author is empty or only whitespace.
    
    Examples:
        >>> collection = BookCollection()
        >>> collection.add_book("1984", "George Orwell", 1949)
        >>> books = collection.find_by_author("Orwell")
        >>> len(books)
        1
    """
```

### Logging, Not Print

Use logging for diagnostics; reserve `print()` for user-facing output only:

```python
# Good - diagnostic
logger.warning(f"Book not found: '{title}'")

# Good - user output
print(f"\n⚠️ Book not found: '{title}'")

# Bad - diagnostics should not use print
print("Book not found in collection")
```

### JSON Persistence

- Data is automatically saved after `add_book()`, `remove_book()`, and `mark_as_read()`
- Manual `save_books()` calls are rarely needed
- `load_books()` is called on `BookCollection()` initialization
- Corrupted JSON files log a warning and start with empty collection

### Authentication Module

The `auth.py` module provides production-ready user management:

- **Password hashing**: SHA-256 with salt (use bcrypt for production)
- **Validation**: Username, email, and password strength checks
- **User management**: Registration, login, activation, deactivation
- **Security**: Tracks failed login attempts, prevents plaintext storage

Use `AuthManager` for any user-related operations:

```python
manager = AuthManager()
user = manager.register("john_doe", "john@example.com", "password123")
if manager.login("john_doe", "password123"):
    print("Login successful")
```

## Testing Guidelines

### Test Structure

Tests use pytest with fixtures for isolation:

```python
@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Isolate each test with its own temp data file."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
```

### Test Organization

- **test_books.py**: BookCollection and Book dataclass tests
- **test_auth.py**: AuthManager and User tests
- **test_utils.py**: Helper function tests
- **test_collection_comprehensive.py**: Integration tests
- **test_integration.py**: End-to-end scenarios

### Writing Tests

Always test both success and failure paths:

```python
def test_add_book_valid():
    """Happy path: add a valid book."""
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == 1

def test_add_book_invalid_title():
    """Error path: title cannot be empty."""
    collection = BookCollection()
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        collection.add_book("", "Author", 1949)
```

## Validation Rules

### Book Validation

- **Title**: Non-empty, max 200 characters
- **Author**: Non-empty, max 100 characters
- **Year**: 1000 to current year (inclusive)

### Authentication Validation

- **Username**: 3-50 characters, alphanumeric + underscore only
- **Email**: Valid format (contains @ and domain)
- **Password**: Minimum 8 characters, maximum 128 characters

## Common Patterns

### Checking if a Book Exists

```python
# Returns Optional[Book]
book = collection.find_book_by_title("1984")
if book:
    print(f"Found: {book.author}")
else:
    print("Not found")
```

### Searching by Author

```python
# Supports partial name matching
books = collection.find_by_author("Orwell")  # Case-insensitive
for book in books:
    print(book.title)
```

### Unread Books

```python
unread = collection.list_unread_books()
for book in unread:
    print(f"{book.title} by {book.author} ({book.year})")
```

## Known Limitations & Future Improvements

- **Data Storage**: Currently JSON-based; database migration planned
- **Concurrency**: Single-threaded; no multi-process safety
- **Performance**: Linear search (O(n)); indexing could optimize for large collections
- **CLI**: No fancy UI; consider Click/Typer framework for production
- **Authentication**: In-memory only; needs persistence layer

## Documentation Files

- **ERROR_HANDLING_GUIDE.md**: User-facing error handling explanations
- **BOOKS_API.md**: Complete API reference with examples
- **ARCHITECTURE_ANALYSIS.md**: Detailed system design and improvements
- **TESTS_COMPREHENSIVE.md**: Test coverage documentation
- **TESTS_AUTH.md**: Authentication testing details
