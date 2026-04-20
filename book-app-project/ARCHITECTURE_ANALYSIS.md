# book_app.py と books.py の関係と改善分析

## 📐 アーキテクチャ図

```
┌─────────────────────────────────────────────────────┐
│                   book_app.py                       │
│                  (CLI Interface)                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ handle_add   │ │ handle_list   │ │ handle_find  │ │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ │
│         │                │                 │        │
│  ┌──────┴────────────────┴─────────────────┴──────┐ │
│  │ Global collection (BookCollection)            │ │
│  └──────┬─────────────────────────────────────────┘ │
└─────────┼──────────────────────────────────────────┘
          │ (依存)
┌─────────▼──────────────────────────────────────────┐
│                   books.py                         │
│              (Data & Business Logic)               │
│  ┌──────────────────────────────────────────────┐  │
│  │  BookCollection (状態管理)                    │  │
│  │  ├─ add_book()                               │  │
│  │  ├─ remove_book()                            │  │
│  │  ├─ find_by_author()                         │  │
│  │  ├─ mark_as_read()                           │  │
│  │  ├─ load_books()  ─────┐                     │  │
│  │  └─ save_books()   ────┼→ data.json (永続化) │  │
│  │                         │                     │  │
│  │  ├─ _validate_book_input() (バリデーション)  │  │
│  │  └─ @Book (dataclass)                        │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

---

## 🔗 ファイル間の関係

### **book_app.py の責務**
- ✅ CLI（コマンドラインインターフェース）処理
- ✅ ユーザー入力の受け取り
- ✅ `BookCollection` インスタンスの管理
- ✅ コマンドルーティング
- ✅ ハンドラー関数の定義

### **books.py の責務**
- ✅ データモデル（`Book` dataclass）
- ✅ 状態管理（`BookCollection`）
- ✅ 永続化（JSON読み書き）
- ✅ ビジネスロジック（検索、フィルタリング）
- ✅ バリデーション

### **依存関係**
```
book_app.py → books.py (一方向)
```
- ✅ **健全な依存**: UIレイヤーがドメインレイヤーに依存（良い）
- ❌ **逆依存なし**: books.py は book_app.py に依存しない（良い）

---

## ✅ 現在の良い点

### 1. **責任の明確な分離**
```
book_app.py (UI層)      ────→  books.py (ビジネスロジック層)
```
- 低結合: book_app.py は books.py にのみ依存
- 高凝聚性: 各ファイルは単一責任

### 2. **グローバル状態の管理**
```python
# book_app.py
collection = BookCollection()  # シングルトン的に管理
```
- 単一の `BookCollection` インスタンス
- すべてのハンドラー関数がアクセス可能

### 3. **バリデーション層**
```python
# books.py
collection.add_book()  # 必ずバリデーション実行
```
- UIから独立したバリデーション
- books.py 内で検証ロジック完結

### 4. **エラーハンドリング**
```python
# book_app.py
try:
    collection.add_book(...)
except ValidationError as e:  # 明示的例外処理
    print(f"Error: {e}")
```

---

## ⚠️ 改善できる点

### 🔴 **CRITICAL**

#### 1. **グローバル状態による テスト困難性**
**問題:**
```python
# book_app.py (行 7)
collection = BookCollection()  # グローバル変数
```

**影響:**
- テストの独立性が失われる
- テスト間で状態が共有される
- `BookCollection` の初期化時に即座に `data.json` を読む

**改善案:**
```python
# book_app.py (改善版)
class BookApp:
    """Application controller."""
    
    def __init__(self, data_file: str = "data.json"):
        self.collection = BookCollection(data_file)
    
    def handle_add(self):
        # ... コード
```

---

#### 2. **data.json のハードコード化**
**問題:**
```python
# books.py (行 11)
DATA_FILE = "data.json"
```

**影響:**
- 実行ディレクトリに依存
- テストで上書きが複雑
- 複数インスタンス起動時にファイルが競合

**改善案:**
```python
# books.py (改善版)
class BookCollection:
    def __init__(self, data_file: str = "data.json"):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()
    
    def load_books(self):
        try:
            with open(self.data_file, "r") as f:
                # ...
```

---

### 🟠 **HIGH**

#### 3. **remove_book のユーザーフィードバック不足**
**問題:**
```python
# book_app.py (行 36-42)
def handle_remove():
    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)
    print("\nBook removed if it existed.\n")  # ❌ あいまい
```

**改善案:**
```python
def handle_remove():
    title = input("Enter the title of the book to remove: ").strip()
    if collection.remove_book(title):
        print(f"\nBook '{title}' removed successfully.\n")
    else:
        print(f"\nBook '{title}' not found.\n")
```

---

#### 4. **mark_as_read コマンドが未実装**
**問題:**
```python
# book_app.py
# "mark_as_read" コマンドがない
```

**改善案:**
```python
def handle_mark_read():
    """Mark a book as read."""
    print("\nMark Book as Read\n")
    title = input("Book title: ").strip()
    
    try:
        if collection.mark_as_read(title):
            print(f"\n'{title}' marked as read.\n")
        else:
            print(f"\n'{title}' not found.\n")
    except ValidationError as e:
        print(f"\nError: {e}\n")
```

---

#### 5. **エラーハンドリングの不備**
**問題:**
```python
# books.py (行 39-42)
def save_books(self):
    """Save the current book collection to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump([asdict(b) for b in self.books], f, indent=2)
    # ❌ IOError, PermissionError をキャッチしない
```

**改善案:**
```python
def save_books(self) -> None:
    """Save the current book collection to JSON."""
    try:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)
    except IOError as e:
        print(f"ERROR: Cannot save books: {e}")
        raise
```

---

### 🟡 **MEDIUM**

#### 6. **find_book_by_title が非効率**
**問題:**
```python
# books.py (行 76-80)
def find_book_by_title(self, title: str) -> Optional[Book]:
    for book in self.books:  # ❌ 線形探索 O(n)
        if book.title.lower() == title.lower():
            return book
    return None
```

**改善案（小規模なら現状でOK、大規模なら）:**
```python
# キャッシュを使う場合
def __init__(self, data_file: str = "data.json"):
    self.books: List[Book] = []
    self._title_index: Dict[str, Book] = {}
    self.load_books()

def find_book_by_title(self, title: str) -> Optional[Book]:
    return self._title_index.get(title.lower())
```

---

#### 7. **セキュリティ: ファイルパス検証なし**
**問題:**
```python
# books.py
with open(DATA_FILE, "w") as f:  # ❌ パス検証なし
```

**改善案:**
```python
from pathlib import Path

def __init__(self, data_file: str = "data.json"):
    # パスの検証
    path = Path(data_file).resolve()
    if path.name != "data.json":
        raise ValueError("Invalid data file")
    self.data_file = str(path)
```

---

#### 8. **load_books の警告メッセージが print**
**問題:**
```python
# books.py (行 35-37)
except json.JSONDecodeError:
    print("Warning: data.json is corrupted. Starting with empty collection.")
    self.books = []  # ❌ sideeffect + print文
```

**改善案:**
```python
# ロギング機構を使う
import logging

logger = logging.getLogger(__name__)

def load_books(self):
    try:
        # ...
    except json.JSONDecodeError:
        logger.warning(f"Corrupted data file: {self.data_file}")
        self.books = []
```

---

## 📋 改善優先度チェックリスト

| 優先度 | 項目 | 難度 | 効果 |
|--------|------|------|------|
| 🔴 P1 | グローバル状態をクラスにする | 高 | 高 |
| 🔴 P1 | data_file をコンストラクタ引数に | 低 | 高 |
| 🟠 P2 | handle_remove のフィードバック | 低 | 中 |
| 🟠 P2 | mark_as_read コマンド実装 | 低 | 中 |
| 🟠 P2 | save_books エラーハンドリング | 中 | 高 |
| 🟡 P3 | ロギング機構の導入 | 中 | 中 |
| 🟡 P3 | インデックス最適化 | 低 | 低 |

---

## 🎯 改善実装の流れ

### Phase 1: グローバル状態を排除
```python
class BookApp:
    def __init__(self, data_file: str = "data.json"):
        self.collection = BookCollection(data_file)
    
    def handle_add(self): ...
    def handle_remove(self): ...
    def main(self): ...
```

### Phase 2: data_file パラメータ化
```python
class BookCollection:
    def __init__(self, data_file: str = "data.json"):
        self.data_file = data_file
        # ...
```

### Phase 3: エラーハンドリング強化
```python
def save_books(self) -> None:
    try:
        # ...
    except IOError as e:
        raise
```

### Phase 4: ロギング導入
```python
import logging

logger = logging.getLogger(__name__)
# print文をlogger.info() に置き換え
```

---

## ✨ 改善後の期待効果

| 効果 | 説明 |
|------|------|
| **テスト性向上** | グローバル状態がないため各テストが独立 |
| **保守性向上** | 依存関係が明示的 |
| **再利用性向上** | `BookCollection` を複数インスタンス化可能 |
| **デバッグ容易性** | エラー追跡が明確 |
| **スケーラビリティ** | 将来的に DB への切り替えが容易 |

---

## 📊 複雑度分析

| メトリクス | book_app.py | books.py | 評価 |
|-----------|-----------|---------|------|
| 圏複雑度 | 5 | 3 | 🟡 中 |
| 関数数 | 6 | 8 | ✅ 適切 |
| 行数 | 93 | 102 | ✅ 適切 |
| グローバル状態 | ❌ あり | ❌ あり | 改善対象 |
| テストカバレッジ | 部分的 | 100% | 🟡 改善中 |

---

## 🚀 次のステップ

1. ✅ Phase 1 実装: グローバル状態の排除
2. ✅ Phase 2 実装: データファイル設定
3. ✅ Phase 3 実装: エラーハンドリング
4. ✅ テスト追加: 新しいアーキテクチャ対応
5. ✅ ドキュメント更新: 新しい使用方法

---

## 参考: リファクタリング後のコード例

```python
# book_app.py (改善版)
import sys
from books import BookCollection, ValidationError
from utils import display_books


class BookApp:
    """Main application controller."""
    
    def __init__(self, data_file: str = "data.json"):
        self.collection = BookCollection(data_file)
    
    def handle_add(self):
        print("\nAdd a New Book\n")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        year_str = input("Year (press Enter to skip): ").strip()
        
        try:
            year = int(year_str) if year_str else 0
        except ValueError:
            print("\nError: Year must be a valid number.\n")
            return
        
        try:
            self.collection.add_book(title, author, year)
            print("\nBook added successfully.\n")
        except ValidationError as e:
            print(f"\nError: {e}\n")
    
    def main(self, command: str):
        handlers = {
            "add": self.handle_add,
            "list": self.handle_list,
            # ...
        }
        handler = handlers.get(command)
        if handler:
            handler()
        else:
            self.show_help()


if __name__ == "__main__":
    app = BookApp()
    command = sys.argv[1].lower() if len(sys.argv) > 1 else "help"
    app.main(command)
```
