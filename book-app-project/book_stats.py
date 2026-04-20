from dataclasses import dataclass
from typing import List, Optional
from books import Book


@dataclass
class BookStats:
    """統計情報を格納するデータクラス"""
    total_count: int
    read_count: int
    unread_count: int
    oldest_book: Optional[Book]
    newest_book: Optional[Book]


def get_book_statistics(books: List[Book]) -> BookStats:
    """
    本のリストを受け取り、統計情報を返す関数
    
    Args:
        books: Book オブジェクトのリスト
        
    Returns:
        BookStats: 統計情報を含むデータクラス
    """
    if not books:
        return BookStats(
            total_count=0,
            read_count=0,
            unread_count=0,
            oldest_book=None,
            newest_book=None
        )
    
    # 総数と既読数の計算
    total_count = len(books)
    read_count = sum(1 for book in books if book.read)
    unread_count = total_count - read_count
    
    # 最も古い本と最も新しい本を探す
    oldest_book = min(books, key=lambda b: b.year)
    newest_book = max(books, key=lambda b: b.year)
    
    return BookStats(
        total_count=total_count,
        read_count=read_count,
        unread_count=unread_count,
        oldest_book=oldest_book,
        newest_book=newest_book
    )


def print_statistics(stats: BookStats) -> None:
    """統計情報をわかりやすく表示する"""
    print("\n📊 書籍統計情報\n")
    print(f"総数:     {stats.total_count} 冊")
    print(f"既読数:   {stats.read_count} 冊")
    print(f"未読数:   {stats.unread_count} 冊")
    
    if stats.oldest_book:
        print(f"\n最も古い本:  '{stats.oldest_book.title}' ({stats.oldest_book.year}年)")
    if stats.newest_book:
        print(f"最も新しい本: '{stats.newest_book.title}' ({stats.newest_book.year}年)")
    
    print()


# 使用例
if __name__ == "__main__":
    from books import BookCollection
    
    collection = BookCollection()
    stats = get_book_statistics(collection.list_books())
    print_statistics(stats)
