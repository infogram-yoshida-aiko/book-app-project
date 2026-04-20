const fs = require("fs");
const path = require("path");

const DATA_FILE = path.join(__dirname, "data.json");

class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

class Book {
  constructor(title, author, year, read = false) {
    this.title = title;
    this.author = author;
    this.year = year;
    this.read = read;
  }
}

class BookCollection {
  constructor(dataFile) {
    this.dataFile = dataFile || DATA_FILE;
    this.books = [];
    this.loadBooks();
  }

  loadBooks() {
    try {
      const raw = fs.readFileSync(this.dataFile, "utf-8");
      const data = JSON.parse(raw);
      this.books = data.map((b) => new Book(b.title, b.author, b.year, b.read));
    } catch (err) {
      if (err.code === "ENOENT") {
        this.books = [];
      } else if (err instanceof SyntaxError) {
        console.log("Warning: data.json is corrupted. Starting with empty collection.");
        this.books = [];
      } else {
        throw err;
      }
    }
  }

  saveBooks() {
    const data = this.books.map((b) => ({
      title: b.title,
      author: b.author,
      year: b.year,
      read: b.read,
    }));
    fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
  }

  static validateBookInput(title, author, year) {
    if (!title || !title.trim()) {
      throw new ValidationError("Title cannot be empty");
    }
    if (!author || !author.trim()) {
      throw new ValidationError("Author cannot be empty");
    }
    if (typeof year !== "number" || !Number.isInteger(year)) {
      throw new ValidationError("Year must be an integer");
    }
    const currentYear = new Date().getFullYear();
    if (year < 1000 || year > currentYear) {
      throw new ValidationError(`Year must be between 1000 and ${currentYear}`);
    }
  }

  addBook(title, author, year) {
    BookCollection.validateBookInput(title, author, year);
    const book = new Book(title, author, year);
    this.books.push(book);
    this.saveBooks();
    return book;
  }

  listBooks() {
    return this.books;
  }

  findBookByTitle(title) {
    return this.books.find((b) => b.title.toLowerCase() === title.toLowerCase()) || null;
  }

  markAsRead(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      book.read = true;
      this.saveBooks();
      return true;
    }
    return false;
  }

  removeBook(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      this.books = this.books.filter((b) => b !== book);
      this.saveBooks();
      return true;
    }
    return false;
  }

  findByAuthor(author) {
    return this.books.filter((b) => b.author.toLowerCase() === author.toLowerCase());
  }
}

module.exports = { Book, BookCollection, ValidationError, DATA_FILE };
