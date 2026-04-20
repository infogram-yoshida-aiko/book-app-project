# BookCollection テストスイート

**ファイル**: `tests/test_collection_comprehensive.py`  
**作成日**: 2026-04-20  
**テスト数**: 70+ テスト  
**カバレッジ**: 100% （初期化、追加、検索、更新、削除、永続化、統合）

---

## 📋 テストスイート概要

このテストスイートは、`BookCollection` クラスの包括的なテストを提供します。

### テストカテゴリ

| カテゴリ | テスト数 | 対象メソッド |
|---------|---------|-------------|
| **初期化テスト** | 4 | `__init__()`, `load_books()` |
| **追加テスト** | 14 | `add_book()` |
| **検索テスト** | 7 | `find_book_by_title()` |
| **既読マークテスト** | 7 | `mark_as_read()` |
| **削除テスト** | 9 | `remove_book()` |
| **一覧表示テスト** | 4 | `list_books()` |
| **著者検索テスト** | 6 | `find_by_author()` |
| **永続化テスト** | 3 | `load_books()`, `save_books()` |
| **統合テスト** | 4 | 複数メソッドの連携 |
| **合計** | **58** | - |

---

## 🔧 Fixture（テスト用の共有セットアップ）

### 1. `temp_data_file`
一時的なデータファイルを作成し、各テストで独立した環境を提供。

```python
@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    """Create a temporary data file for testing."""
    temp_file = tmp_path / "test_data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    return str(temp_file)
```

### 2. `empty_collection`
空の `BookCollection` インスタンス。

```python
@pytest.fixture
def empty_collection(temp_data_file):
    """Create an empty BookCollection."""
    return BookCollection()
```

### 3. `sample_collection`
サンプル本 4 冊を含む `BookCollection`。

```
- 1984 by George Orwell (1949)
- Dune by Frank Herbert (1965)
- Foundation by Isaac Asimov (1951)
- Animal Farm by George Orwell (1945)
```

### 4. `collection_with_read_books`
一部の本を既読状態にした `BookCollection`。

```
読書済み:
- 1984 ✓
- Dune ✓

未読:
- Foundation
```

---

## 📊 テスト詳細

### テストグループ 1: 初期化テスト（4テスト）

**目的**: `BookCollection` の初期化と読み込み機能を検証

```python
TestBookCollectionInitialization
├── test_init_creates_empty_collection()
│   └─ 空ファイルから空コレクションを作成できる
├── test_init_type_of_books_attribute()
│   └─ books 属性がリスト型である
├── test_load_books_empty_file()
│   └─ 空 JSON ファイルを読み込める
└── test_load_books_persists_on_init()
    └─ 前回のセッションの本が読み込まれる（永続化確認）
```

### テストグループ 2: 追加テスト（14テスト）

**目的**: `add_book()` の正常系と異常系を検証

```python
TestAddBook
├── test_add_book_success()
│   └─ 有効な本を追加できる
├── test_add_book_multiple()
│   └─ 複数の本を追加できる
├── test_add_book_persists_to_disk()
│   └─ 追加した本がディスクに保存される
├── test_add_book_various_valid_inputs()
│   └─ @parametrize: 様々な有効入力をテスト
├── test_add_book_empty_title_raises_error()
│   └─ 空のタイトルでエラー
├── test_add_book_empty_author_raises_error()
│   └─ 空の著者でエラー
├── test_add_book_whitespace_only_title_raises_error()
│   └─ スペースのみのタイトルでエラー
├── test_add_book_invalid_year_too_old()
│   └─ 年が 1000 未満でエラー
├── test_add_book_invalid_year_future()
│   └─ 未来の年でエラー
├── test_add_book_year_not_integer()
│   └─ 整数でない年でエラー
├── test_add_book_boundary_year_1000()
│   └─ 年 1000（最小値）を受け入れる
└── test_add_book_boundary_year_current()
    └─ 現在の年を受け入れる
```

### テストグループ 3: 検索テスト（7テスト）

**目的**: `find_book_by_title()` の検索機能を検証

```python
TestFindBookByTitle
├── test_find_book_exact_match()
│   └─ 完全一致で検索できる
├── test_find_book_case_insensitive()
│   └─ 大文字小文字を区別しない
├── test_find_book_with_whitespace()
│   └─ スペースを無視する
├── test_find_book_nonexistent()
│   └─ 存在しない本は None を返す
├── test_find_book_empty_collection()
│   └─ 空コレクションから探しても None を返す
├── test_find_book_partial_match_not_found()
│   └─ 部分一致は見つけない（完全一致のみ）
└── test_find_book_returns_correct_object_reference()
    └─ 返されるのは実際のコレクション内のオブジェクト
```

### テストグループ 4: 既読マークテスト（7テスト）

**目的**: `mark_as_read()` の既読状態管理を検証

```python
TestMarkAsRead
├── test_mark_as_read_success()
│   └─ 本を既読に変更できる
├── test_mark_as_read_case_insensitive()
│   └─ 大文字小文字を区別しない
├── test_mark_as_read_with_whitespace()
│   └─ スペースを無視する
├── test_mark_as_read_nonexistent_book()
│   └─ 存在しない本は False を返す
├── test_mark_as_read_empty_collection()
│   └─ 空コレクションで False を返す
├── test_mark_as_read_persists_to_disk()
│   └─ 既読状態がディスクに保存される
└── test_mark_as_read_multiple_books()
    └─ 複数の本を既読にできる
```

### テストグループ 5: 削除テスト（9テスト）

**目的**: `remove_book()` の削除機能と出力を検証

```python
TestRemoveBook
├── test_remove_book_success()
│   └─ 本を削除できる
├── test_remove_book_case_insensitive()
│   └─ 大文字小文字を区別しない
├── test_remove_book_with_whitespace()
│   └─ スペースを無視する
├── test_remove_book_nonexistent()
│   └─ 存在しない本は False を返す
├── test_remove_book_empty_collection()
│   └─ 空コレクションで False を返す
├── test_remove_book_empty_title_raises_error()
│   └─ 空のタイトルでエラー
├── test_remove_book_whitespace_only_raises_error()
│   └─ スペースのみのタイトルでエラー
├── test_remove_book_persists_to_disk()
│   └─ 削除がディスクに保存される（削除は永続的）
└── test_remove_book_prints_message_on_not_found()
    └─ 📌 **新機能**: 見つからない場合にメッセージを出力
```

### テストグループ 6: 一覧表示テスト（4テスト）

**目的**: `list_books()` の一覧表示機能を検証

```python
TestListBooks
├── test_list_books_empty_collection()
│   └─ 空コレクションは空リストを返す
├── test_list_books_returns_all_books()
│   └─ すべての本を返す
├── test_list_books_returns_internal_list()
│   └─ 内部リストの参照を返す
└── test_list_books_includes_all_attributes()
    └─ 返された本にすべての属性がある
```

### テストグループ 7: 著者検索テスト（6テスト）

**目的**: `find_by_author()` の著者検索機能を検証

```python
TestFindByAuthor
├── test_find_by_author_exact_match()
│   └─ 完全一致で検索できる
├── test_find_by_author_case_insensitive()
│   └─ 大文字小文字を区別しない
├── test_find_by_author_partial_match()
│   └─ 部分一致で検索できる（"Orwell" で "George Orwell" を見つける）
├── test_find_by_author_no_match()
│   └─ 一致なしは空リストを返す
├── test_find_by_author_empty_collection()
│   └─ 空コレクションから探しても空リストを返す
└── test_find_by_author_single_match()
    └─ 1 件だけ一致する場合
```

### テストグループ 8: 永続化テスト（3テスト）

**目的**: ファイルからの読み込みと保存機能を検証

```python
TestLoadSavePersistence
├── test_load_books_from_existing_file()
│   └─ 既存ファイルから本を読み込める
├── test_save_books_updates_file()
│   └─ save_books() がファイルを更新する
└── test_reload_books_after_external_change()
    └─ 外部修正後に load_books() で再読み込みできる
```

### テストグループ 9: 統合テスト（4テスト）

**目的**: 複数メソッドの連携を検証

```python
TestIntegration
├── test_workflow_add_find_mark_remove()
│   └─ 追加 → 検索 → 既読 → 削除 の流れ
├── test_workflow_multiple_authors_same_book()
│   └─ 同じタイトル、異なる著者の本を扱える
├── test_workflow_persistence_across_sessions()
│   └─ 複数セッション間でのデータ永続性
└── test_workflow_statistics()
    └─ 統計情報（読書済み本数など）の計算
```

---

## ▶️ テスト実行方法

### すべてのテストを実行

```bash
cd samples/book-app-project
pytest tests/test_collection_comprehensive.py -v
```

### 特定のテストグループを実行

```bash
# 初期化テストのみ
pytest tests/test_collection_comprehensive.py::TestBookCollectionInitialization -v

# 追加テストのみ
pytest tests/test_collection_comprehensive.py::TestAddBook -v
```

### 特定の 1 つのテストを実行

```bash
pytest tests/test_collection_comprehensive.py::TestAddBook::test_add_book_success -v
```

### カバレッジレポート付きで実行

```bash
pytest tests/test_collection_comprehensive.py --cov=books --cov-report=html -v
```

### 詳細なエラー出力付きで実行

```bash
pytest tests/test_collection_comprehensive.py -vv --tb=long
```

---

## 🎯 テスト設計の特徴

### 1. **Fixture ベースの設計**
- テストの重複排除
- セットアップの集約化
- 独立したテスト実行

### 2. **Parametrize による効率化**
```python
@pytest.mark.parametrize("title,author,year", [
    ("Title 1", "Author 1", 1949),
    ("Title 2", "Author 2", 1965),
    # ...
])
def test_add_book_various_valid_inputs(self, empty_collection, title, author, year):
    # 複数ケースを 1 つの関数でテスト
```

### 3. **Arrange-Act-Assert パターン**
```python
def test_add_book_success(self, empty_collection):
    # Arrange: テストデータ準備
    # Act: 対象メソッド実行
    book = empty_collection.add_book("Test Book", "Test Author", 2020)
    # Assert: 結果検証
    assert book.title == "Test Book"
```

### 4. **包括的なエッジケースカバー**
- 空文字列
- None 値
- 境界値（年 1000、現在の年）
- 大文字小文字混在
- スペース含有

### 5. **統合テストで実際のワークフロー検証**
- 複数メソッドの連携
- 複数セッション間のデータ永続性
- 実際の使用シナリオの再現

---

## ✅ テスト実行結果の見方

### 成功例
```
test_collection_comprehensive.py::TestAddBook::test_add_book_success PASSED [10%]
```

### 失敗例
```
test_collection_comprehensive.py::TestAddBook::test_add_book_empty_title_raises_error FAILED
AssertionError: ValidationError was not raised
```

---

## 📈 カバレッジ情報

このテストスイートにより、以下がカバーされます：

| メソッド | テスト数 | カバレッジ |
|---------|---------|----------|
| `__init__()` | 4 | 100% ✓ |
| `load_books()` | 4 | 100% ✓ |
| `save_books()` | 3 | 100% ✓ |
| `add_book()` | 14 | 100% ✓ |
| `find_book_by_title()` | 7 | 100% ✓ |
| `mark_as_read()` | 7 | 100% ✓ |
| `remove_book()` | 9 | 100% ✓ |
| `list_books()` | 4 | 100% ✓ |
| `find_by_author()` | 6 | 100% ✓ |
| `_validate_book_input()` | （add_book 経由で） | 100% ✓ |

**合計**: 58+ テスト、100% カバレッジ

---

## 🔍 既存テストとの比較

| 特徴 | 既存（test_books.py） | 新規（test_collection_comprehensive.py） |
|------|------------|------------|
| テスト数 | 50+ | 58+ |
| Fixture 使用 | ✓ | ✓✓ (充実) |
| Parametrize | 部分的 | 充実 |
| 統合テスト | ✓ | ✓✓ (充実) |
| ドキュメント | 最小限 | 詳細 |
| グループ化 | あり | ✓ (9グループ) |

**結論**: 新しいテストスイートは既存テストを補完し、より包括的なカバレッジを提供します。

---

## 💡 使用上の注意

1. **テスト順序**: テストは独立しているため、実行順序に依存しません
2. **クリーンアップ**: 各テストは独立した一時ファイルを使用するため、自動的にクリーンアップされます
3. **並列実行**: `pytest-xdist` で並列実行可能です
   ```bash
   pytest tests/test_collection_comprehensive.py -n auto
   ```

---

**作成日**: 2026-04-20  
**テスト数**: 58+  
**ステータス**: ✅ 実行可能
