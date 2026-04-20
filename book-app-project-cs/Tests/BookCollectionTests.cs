using BookApp.Models;
using BookApp.Services;

namespace BookApp.Tests;

public class BookCollectionTests : IDisposable
{
    private readonly string _tempFile;
    private readonly BookCollection _collection;

    public BookCollectionTests()
    {
        _tempFile = Path.GetTempFileName();
        File.WriteAllText(_tempFile, "[]");
        _collection = new BookCollection(_tempFile);
    }

    public void Dispose()
    {
        if (File.Exists(_tempFile)) File.Delete(_tempFile);
    }

    [Fact]
    public void AddBook_ShouldAddAndPersist()
    {
        var initialCount = _collection.Books.Count;
        _collection.AddBook("1984", "George Orwell", 1949);

        Assert.Equal(initialCount + 1, _collection.Books.Count);

        var book = _collection.FindBookByTitle("1984");
        Assert.NotNull(book);
        Assert.Equal("George Orwell", book.Author);
        Assert.Equal(1949, book.Year);
        Assert.False(book.Read);
    }

    [Fact]
    public void MarkAsRead_ShouldSetReadTrue()
    {
        _collection.AddBook("Dune", "Frank Herbert", 1965);
        var result = _collection.MarkAsRead("Dune");

        Assert.True(result);
        Assert.True(_collection.FindBookByTitle("Dune")!.Read);
    }

    [Fact]
    public void MarkAsRead_NonexistentBook_ShouldReturnFalse()
    {
        var result = _collection.MarkAsRead("Nonexistent Book");
        Assert.False(result);
    }

    [Fact]
    public void RemoveBook_ShouldRemoveExistingBook()
    {
        _collection.AddBook("The Hobbit", "J.R.R. Tolkien", 1937);
        var result = _collection.RemoveBook("The Hobbit");

        Assert.True(result);
        Assert.Null(_collection.FindBookByTitle("The Hobbit"));
    }

    [Fact]
    public void RemoveBook_NonexistentBook_ShouldReturnFalse()
    {
        var result = _collection.RemoveBook("Nonexistent Book");
        Assert.False(result);
    }

    // Year validation tests (1000-current_year range)

    [Fact]
    public void AddBook_YearBelow1000_ShouldThrowValidationException()
    {
        var ex = Assert.Throws<ValidationException>(() =>
            _collection.AddBook("Ancient Manuscript", "Unknown", 999)
        );
        Assert.Contains("Year must be between 1000", ex.Message);
    }

    [Fact]
    public void AddBook_Year1000_ShouldBeAccepted()
    {
        var book = _collection.AddBook("Ancient Book", "Unknown", 1000);
        Assert.Equal(1000, book.Year);
    }

    [Fact]
    public void AddBook_Year1001_ShouldBeAccepted()
    {
        var book = _collection.AddBook("Medieval Book", "Unknown", 1001);
        Assert.Equal(1001, book.Year);
    }

    [Fact]
    public void AddBook_CurrentYear_ShouldBeAccepted()
    {
        int currentYear = DateTime.Now.Year;
        var book = _collection.AddBook("This Year's Book", "Author", currentYear);
        Assert.Equal(currentYear, book.Year);
    }

    [Fact]
    public void AddBook_NextYear_ShouldThrowValidationException()
    {
        int nextYear = DateTime.Now.Year + 1;
        var ex = Assert.Throws<ValidationException>(() =>
            _collection.AddBook("Future Book", "Author", nextYear)
        );
        Assert.Contains("Year must be between 1000", ex.Message);
    }

    [Fact]
    public void AddBook_LastYear_ShouldBeAccepted()
    {
        int lastYear = DateTime.Now.Year - 1;
        var book = _collection.AddBook("Last Year Book", "Author", lastYear);
        Assert.Equal(lastYear, book.Year);
    }

    [Fact]
    public void AddBook_EmptyTitle_ShouldThrowValidationException()
    {
        var ex = Assert.Throws<ValidationException>(() =>
            _collection.AddBook("", "Author", 2020)
        );
        Assert.Contains("Title cannot be empty", ex.Message);
    }

    [Fact]
    public void AddBook_EmptyAuthor_ShouldThrowValidationException()
    {
        var ex = Assert.Throws<ValidationException>(() =>
            _collection.AddBook("Title", "", 2020)
        );
        Assert.Contains("Author cannot be empty", ex.Message);
    }
}
