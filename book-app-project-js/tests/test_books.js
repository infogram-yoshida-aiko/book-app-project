const { describe, it, beforeEach } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { BookCollection, ValidationError } = require("../books");

let tempFile;

beforeEach(() => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "book-test-"));
  tempFile = path.join(tempDir, "data.json");
  fs.writeFileSync(tempFile, "[]");
});

describe("BookCollection", () => {
  it("should add a book", () => {
    const collection = new BookCollection(tempFile);
    const initialCount = collection.books.length;
    collection.addBook("1984", "George Orwell", 1949);
    assert.equal(collection.books.length, initialCount + 1);
    const book = collection.findBookByTitle("1984");
    assert.notEqual(book, null);
    assert.equal(book.author, "George Orwell");
    assert.equal(book.year, 1949);
    assert.equal(book.read, false);
  });

  it("should mark a book as read", () => {
    const collection = new BookCollection(tempFile);
    collection.addBook("Dune", "Frank Herbert", 1965);
    const result = collection.markAsRead("Dune");
    assert.equal(result, true);
    const book = collection.findBookByTitle("Dune");
    assert.equal(book.read, true);
  });

  it("should return false when marking a nonexistent book as read", () => {
    const collection = new BookCollection(tempFile);
    const result = collection.markAsRead("Nonexistent Book");
    assert.equal(result, false);
  });

  it("should remove a book", () => {
    const collection = new BookCollection(tempFile);
    collection.addBook("The Hobbit", "J.R.R. Tolkien", 1937);
    const result = collection.removeBook("The Hobbit");
    assert.equal(result, true);
    const book = collection.findBookByTitle("The Hobbit");
    assert.equal(book, null);
  });

  it("should return false when removing a nonexistent book", () => {
    const collection = new BookCollection(tempFile);
    const result = collection.removeBook("Nonexistent Book");
    assert.equal(result, false);
  });

  // Year validation tests (1000-current_year range)

  it("should reject year below 1000", () => {
    const collection = new BookCollection(tempFile);
    assert.throws(() => {
      collection.addBook("Ancient Manuscript", "Unknown", 999);
    }, ValidationError);
  });

  it("should accept year 1000 (lower boundary)", () => {
    const collection = new BookCollection(tempFile);
    const book = collection.addBook("Ancient Book", "Unknown", 1000);
    assert.equal(book.year, 1000);
  });

  it("should accept year 1001 (just above lower boundary)", () => {
    const collection = new BookCollection(tempFile);
    const book = collection.addBook("Medieval Book", "Unknown", 1001);
    assert.equal(book.year, 1001);
  });

  it("should accept current year", () => {
    const collection = new BookCollection(tempFile);
    const currentYear = new Date().getFullYear();
    const book = collection.addBook("This Year's Book", "Author", currentYear);
    assert.equal(book.year, currentYear);
  });

  it("should reject future year (next year)", () => {
    const collection = new BookCollection(tempFile);
    const nextYear = new Date().getFullYear() + 1;
    assert.throws(() => {
      collection.addBook("Future Book", "Author", nextYear);
    }, ValidationError);
  });

  it("should accept last year", () => {
    const collection = new BookCollection(tempFile);
    const lastYear = new Date().getFullYear() - 1;
    const book = collection.addBook("Last Year Book", "Author", lastYear);
    assert.equal(book.year, lastYear);
  });

  it("should reject empty title", () => {
    const collection = new BookCollection(tempFile);
    assert.throws(() => {
      collection.addBook("", "Author", 2020);
    }, ValidationError);
  });

  it("should reject empty author", () => {
    const collection = new BookCollection(tempFile);
    assert.throws(() => {
      collection.addBook("Title", "", 2020);
    }, ValidationError);
  });

  it("should reject non-integer year", () => {
    const collection = new BookCollection(tempFile);
    assert.throws(() => {
      collection.addBook("Title", "Author", 2020.5);
    }, ValidationError);
  });
});
