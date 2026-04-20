namespace BookApp.Models;

public class ValidationException : Exception
{
    public ValidationException(string message) : base(message) { }
}

public class Book
{
    public string Title { get; set; } = string.Empty;
    public string Author { get; set; } = string.Empty;
    public int Year { get; set; }
    public bool Read { get; set; }
}
