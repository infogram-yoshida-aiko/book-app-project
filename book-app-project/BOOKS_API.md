# books.py - API リファレンス

`books.py` は、書籍コレクションの管理とデータ永続化を担当するコアモジュールです。JSON ファイルベースのデータストレージを提供し、CRUD 操作と検索機能をサポートしています。

**対応バージョン**: Python 3.10+  
**ドキュメント作成日**: 2026-04-20

---

## 目次

1. [クイックスタート](#クイックスタート)
2. [データモデル](#データモデル)
3. [API リファレンス](#apiリファレンス)
4. [エラーハンドリング](#エラーハンドリング)
5. [使用例](#使用例)
6. [トラブルシューティング](#トラブルシューティング)

---

## クイックスタート

### 基本的な使い方

```python
from books import BookCollection, ValidationError

# コレクションを初期化（data.json から自動読み込み）
collection = BookCollection()

# 本を追加
try:
    book = collection.add_book("1984", "George Orwell", 1949)
    print(f"追加成功: {book.title}")
except ValidationError as e:
    print(f"エラー: {e}")

# すべての本を表示
for book in collection.list_books():
    status = "✅ 読済" if book.read else "📖 未読"
    print(f"- {book.title} ({book.author}, {book.year}) {status}")

# 本を検索
book = collection.find_book_by_title("1984")
if book:
    print(f"見つかった: {book.title}")

# 本を読済にマーク
collection.mark_as_read("1984")

# 本を削除
if collection.remove_book("1984"):
    print("削除成功")
else:
    print("本が見つかりません")
```

---

## データモデル

### `Book` (dataclass)

書籍情報を格納するデータクラスです。

```python
@dataclass
class Book:
    title: str      # 本のタイトル（必須）
    author: str     # 著者名（必須）
    year: int       # 出版年（必須、1000-現在年）
    read: bool      # 読済フラグ（デフォルト: False）
```

#### 属性

| 属性 | 型 | 説明 | 制約 |
|------|-----|------|------|
| `title` | str | 本のタイトル | 空文字列不可、スペースのみ不可 |
| `author` | str | 著者名 | 空文字列不可、スペースのみ不可 |
| `year` | int | 出版年 | 整数型、1000 以上、現在年以下 |
| `read` | bool | 読済フラグ | 初期値: `False` |

#### 例

```python
from books import Book

# Book インスタンスの作成
book = Book(
    title="Clean Code",
    author="Robert C. Martin",
    year=2008,
    read=True
)

print(book.title)  # "Clean Code"
print(book.read)   # True
```

---

### `ValidationError` (カスタム例外)

入力値が不正な場合に発生する例外です。

```python
from books import ValidationError

try:
    # 不正な入力
    collection.add_book("", "Author", 2020)
except ValidationError as e:
    print(f"バリデーションエラー: {e}")
    # 出力: "Title cannot be empty"
```

---

## API リファレンス

### `BookCollection` クラス

#### コンストラクタ

```python
def __init__(self) -> None
```

書籍コレクションを初期化し、`data.json` から自動的に読み込みます。

**挙動**:
- `data.json` が存在する場合、そのデータを読み込む
- ファイルが存在しない場合、空のコレクションで開始
- JSON が破損している場合、ログに警告を出力して空のコレクションで開始

**例**:
```python
collection = BookCollection()
print(f"読み込まれた本の数: {len(collection.books)}")
```

---

#### `add_book(title: str, author: str, year: int) -> Book`

新しい本をコレクションに追加し、自動的にファイルに保存します。

**パラメータ**:
- `title` (str): 本のタイトル
- `author` (str): 著者名
- `year` (int): 出版年

**戻り値**:
- `Book`: 追加された Book オブジェクト

**例外**:
- `ValidationError`: 入力値が不正な場合

**バリデーション**:
- タイトルと著者は空文字列またはスペースのみ不可
- `year` は整数型で、1000 以上、現在年以下である必要がある

**例**:
```python
try:
    book = collection.add_book("Dune", "Frank Herbert", 1965)
    print(f"追加成功: {book.title}")
except ValidationError as e:
    print(f"入力エラー: {e}")
```

**❌ 不正な入力例**:
```python
# エラー: 空のタイトル
collection.add_book("", "Author", 2020)
# → ValidationError: "Title cannot be empty"

# エラー: 年が文字列
collection.add_book("Title", "Author", "2020")
# → ValidationError: "Year must be an integer"

# エラー: 年が範囲外
collection.add_book("Title", "Author", 2099)
# → ValidationError: "Year must be between 1000 and 2026"
```

---

#### `list_books() -> List[Book]`

コレクションのすべての本を返します。

**戻り値**:
- `List[Book]`: 本のリスト（空の場合は空リスト）

**例**:
```python
books = collection.list_books()
for book in books:
    print(f"{book.title} by {book.author}")
```

---

#### `find_book_by_title(title: str) -> Optional[Book]`

タイトルで本を検索します。**大文字小文字を区別しません**。

**パラメータ**:
- `title` (str): 検索するタイトル（スペースは自動で削除）

**戻り値**:
- `Book`: 見つかった場合
- `None`: 見つからない場合

**特徴**:
- 検索文字列は大文字小文字を区別しない
- 前後のスペースは自動で削除（トリミング）
- 完全一致検索（部分一致ではない）

**例**:
```python
# すべて同じ本を見つけます
collection.find_book_by_title("Dune")
collection.find_book_by_title("dune")
collection.find_book_by_title("DUNE")
collection.find_book_by_title("  Dune  ")  # スペース削除

# 見つからない場合
if collection.find_book_by_title("Nonexistent"):
    print("見つかった")
else:
    print("見つかりません")
```

---

#### `find_by_author(author: str) -> List[Book]`

著者名で本を検索します。**部分一致**をサポートしています。

**パラメータ**:
- `author` (str): 検索する著者名

**戻り値**:
- `List[Book]`: マッチした本のリスト（見つからない場合は空リスト）

**特徴**:
- 大文字小文字を区別しない
- 部分一致検索（「Frank」で「Frank Herbert」を検出）
- 複数の本が返される可能性あり

**例**:
```python
# "Frank Herbert" の本をすべて検索
books = collection.find_by_author("Frank")
for book in books:
    print(f"{book.title} by {book.author}")

# 著者が見つからない場合は空リスト
if not collection.find_by_author("Unknown"):
    print("該当する著者がいません")
```

---

#### `mark_as_read(title: str) -> bool`

本を「読済」にマークします。

**パラメータ**:
- `title` (str): 本のタイトル（大文字小文字を区別しない）

**戻り値**:
- `True`: マーク成功
- `False`: 本が見つからない場合

**例**:
```python
if collection.mark_as_read("1984"):
    print("✅ 読済にマークしました")
else:
    print("❌ 本が見つかりません")
```

---

#### `remove_book(title: str) -> bool`

本をコレクションから削除します。

**パラメータ**:
- `title` (str): 削除する本のタイトル（大文字小文字を区別しない）

**戻り値**:
- `True`: 削除成功
- `False`: 本が見つからない場合

**例外**:
- `ValidationError`: タイトルが空の場合

**例**:
```python
# 削除成功
if collection.remove_book("Old Book"):
    print("削除成功")

# 本が見つからない場合
else:
    print("本が見つかりません")

# 不正な入力
try:
    collection.remove_book("")
except ValidationError as e:
    print(f"エラー: {e}")
    # 出力: "Title cannot be empty"
```

---

#### `save_books() -> None`

コレクションを `data.json` に保存します。

**用途**:
- `add_book()` と `remove_book()` は自動で呼び出す
- 通常、明示的に呼び出す必要はない

**例**:
```python
# 本を追加（自動で save_books() が呼ばれる）
collection.add_book("New Book", "Author", 2024)

# 明示的に保存したい場合
collection.save_books()
```

---

#### `load_books() -> None`

`data.json` からコレクションを再度読み込みます。

**用途**:
- 初期化時に自動で呼び出す
- ファイルが外部から更新された場合の再読み込み

**例外処理**:
- ファイルが見つからない → 空のコレクションで続行
- JSON が破損 → ログに警告、空のコレクションで続行

**例**:
```python
# 外部から data.json が変更された場合
collection.load_books()  # 再度読み込み
```

---

## エラーハンドリング

### `ValidationError` を捕捉する

```python
from books import BookCollection, ValidationError

collection = BookCollection()

try:
    collection.add_book("", "Author", 2020)
except ValidationError as e:
    print(f"❌ 入力エラー: {e}")
```

### よくあるエラー

| エラーメッセージ | 原因 | 解決策 |
|-----------------|------|--------|
| `Title cannot be empty` | タイトルが空またはスペースのみ | 有効なタイトルを入力 |
| `Author cannot be empty` | 著者名が空またはスペースのみ | 有効な著者名を入力 |
| `Year must be an integer` | 年が整数以外 | 整数値を入力（例: `2024`） |
| `Year must be between 1000 and XXXX` | 年が範囲外 | 1000〜現在年の範囲を指定 |

---

## 使用例

### 例1: 本を追加して一覧表示

```python
from books import BookCollection, ValidationError

collection = BookCollection()

# 複数の本を追加
try:
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Clean Code", "Robert Martin", 2008)
except ValidationError as e:
    print(f"エラー: {e}")

# 一覧表示
print("\n📚 My Books:")
for i, book in enumerate(collection.list_books(), 1):
    status = "✅" if book.read else "📖"
    print(f"{i}. {status} {book.title} ({book.author}, {book.year})")
```

**出力**:
```
📚 My Books:
1. 📖 1984 (George Orwell, 1949)
2. 📖 Dune (Frank Herbert, 1965)
3. 📖 Clean Code (Robert Martin, 2008)
```

---

### 例2: 読済状態を変更

```python
# 本を読済にマーク
if collection.mark_as_read("1984"):
    print("✅ 1984 を読済にマークしました")

# 読済状態を確認
book = collection.find_book_by_title("1984")
if book and book.read:
    print(f"✅ {book.title} は読済です")
```

---

### 例3: 著者で検索

```python
# Frank Herbert の本をすべて検索
books = collection.find_by_author("Frank")
if books:
    print(f"🔍 '{Frank}' で見つかった本:")
    for book in books:
        print(f"  - {book.title} ({book.year})")
else:
    print("該当する本がありません")
```

---

### 例4: 本を削除

```python
# 本を削除
title = "Old Book"
try:
    if collection.remove_book(title):
        print(f"✅ '{title}' を削除しました")
    else:
        print(f"❌ '{title}' が見つかりません")
except ValidationError as e:
    print(f"❌ エラー: {e}")
```

---

## トラブルシューティング

### Q: 本を追加したのに再起動後に消えています

**A**: `data.json` が正しく保存されているか確認してください。

```python
# data.json を確認
import json
with open("data.json", "r") as f:
    data = json.load(f)
    print(f"保存されている本の数: {len(data)}")
```

---

### Q: ValidationError が予期せず発生します

**A**: バリデーション条件を確認してください。

```python
from books import BookCollection, ValidationError

collection = BookCollection()

# デバッグ: 各入力を確認
title = "My Book"
author = "Author Name"
year = 2024

print(f"Title valid: {bool(title and title.strip())}")
print(f"Author valid: {bool(author and author.strip())}")
print(f"Year type: {type(year).__name__}, Value: {year}")

try:
    collection.add_book(title, author, year)
except ValidationError as e:
    print(f"エラー: {e}")
```

---

### Q: data.json が破損した場合はどうなりますか？

**A**: 自動的に空のコレクションで開始され、ログに警告が出力されます。

```python
import logging

# ログレベルを DEBUG に設定してメッセージを確認
logging.basicConfig(level=logging.DEBUG)

collection = BookCollection()
# data.json が破損している場合：
# WARNING:books:data.json is corrupted. Starting with empty collection.
```

---

### Q: 大文字小文字を区別した検索がしたいです

**A**: 現在の実装では大文字小文字を区別しません。必要に応じて カスタムメソッドを作成してください。

```python
def find_book_by_title_exact(collection, title: str):
    """大文字小文字を区別した完全一致検索"""
    for book in collection.list_books():
        if book.title == title:
            return book
    return None
```

---

## セキュリティに関する注記

- **ファイルパーミッション**: `data.json` には個人的な本の情報が含まれます。ファイルパーミッションを適切に設定してください。
- **入力検証**: このモジュールは基本的なバリデーションを実施しますが、本番環境ではさらに厳密な検証を追加してください。
- **並行アクセス**: 複数のプロセスが同時に `data.json` にアクセスすると、データが破損する可能性があります。

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2026-04-20 | 初版作成 |

---

**最終更新**: 2026-04-20
