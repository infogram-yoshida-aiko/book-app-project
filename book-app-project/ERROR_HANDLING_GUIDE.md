# エラーハンドリング実践ガイド

**対象読者**: Python 初心者  
**作成日**: 2026-04-20  
**目的**: Book Collection App のエラーが「何が悪いか」「どう対処するか」を学ぶ

---

## 概要（TL;DR）

このガイドでは、Book Collection App で発生するエラーとその対処方法を学びます。

- **ユーザー入力エラー** - 不正な値を入力したときの対処
- **バリデーションエラー** - ビジネスルール違反（例：年の範囲外）
- **デバッグのコツ** - エラーメッセージから原因を特定する

---

## 目次

1. [エラーの種類](#エラーの種類)
2. [よくあるエラーシナリオ](#よくあるエラーシナリオ)
3. [エラー対応のコツ](#エラー対応のコツ)
4. [参考リンク](#参考リンク)

---

## エラーの種類

### 1. 入力エラー（ValueError）

**何が起きた?**  
入力した値が期待した形式ではない。

**発生場面**:
- 年の入力で数字以外を入力した
- メニュー選択で範囲外の番号を入力した

**エラーメッセージ例**:
```
Year must be a valid number. Got: 'abc'
```

**対処方法**:
```
❌ 「abc」ではなく、数字を入力してください
✅ 「1949」と入力して試し直してください
```

---

### 2. バリデーションエラー（ValidationError）

**何が起きた?**  
入力値は正しい形式だが、ビジネスルール（本の条件）に違反している。

**発生場面**:
- 本のタイトルが空白
- 著者が空白
- 年が 1000 より前、または現在より後

**エラーメッセージ例**:
```
Year must be between 1000 and 2026
```

**対処方法**:
```
❌ 「3000」は未来の年だから不可
✅ 「2020」など、過去の年を入力してください
```

---

### 3. メニューエラー

**何が起きた?**  
メニューに存在しない選択肢を選んだ。

**発生場面**:
```
📚 Book Collection App
1. Add a book
2. List books
3. Mark book as read
4. Remove a book
5. Exit
```

ユーザーが「6」を選ぶなど。

**エラーメッセージ例**:
```
❌ Please enter a number between 1 and 5.
```

**対処方法**:
```
再度メニューが表示されます。1～5 の中から選んでください。
```

---

## よくあるエラーシナリオ

### シナリオ 1: 年をテキストで入力した

**ユーザーの入力**:
```
Enter book title: 1984
Enter author: George Orwell
Enter publication year: nineteen forty-nine
```

**アプリの応答**:
```
❌ Error: Year must be a valid number. Got: 'nineteen forty-nine'

Add a New Book

Enter book title:
```

**何が悪かったのか**?
年は数字（1949）で入力する必要があります。

**正しい入力**:
```
Enter publication year: 1949
```

---

### シナリオ 2: 年が範囲外

**ユーザーの入力**:
```
Enter book title: Future Tech
Enter author: Jane Doe
Enter publication year: 3000
```

**アプリの応答**:
```
❌ Error: Year must be between 1000 and 2026
```

**何が悪かったのか**?
本は未来の本ではなく、実在する本を記録するアプリです。

**正しい入力**:
```
Enter publication year: 2024
```

---

### シナリオ 3: 本のタイトルを空白で送信

**ユーザーの入力**:
```
Enter book title: (ただリターンキーを押す)
Enter author: Some Author
Enter publication year: 2020
```

**アプリの応答**:
```
❌ Error: Title cannot be empty
```

**何が悪かったのか**?
タイトルは必須です。空白では本を識別できません。

**正しい入力**:
```
Enter book title: The Great Gatsby
```

---

### シナリオ 4: メニューで無効な選択肢

**ユーザーの入力**:
```
Choose an option (1-5): 99
```

**アプリの応答**:
```
❌ Please enter a number between 1 and 5.
Choose an option (1-5): 2
```

**何が悪かったのか**?
メニューには 1～5 のオプションしかありません。

**正しい入力**:
```
Choose an option (1-5): 2
```

---

## エラー対応のコツ

### 1. エラーメッセージをよく読む

> エラーメッセージには、何が悪かったかのヒントが隠れています。

**例**:
```
Year must be between 1000 and 2026
         ↑ 年の話
                    ↑ このペア（1000～2026）のみ許可
```

### 2. 「どこで」エラーが発生したかを特定

**フロー**:
```
入力 (utils.py)
  ↓
バリデーション (books.py)
  ↓
エラー表示 (book_app.py)
```

**各段階で何をチェックしている?**

| 段階 | チェック内容 | エラー時の動作 |
|------|------------|-------------|
| utils.py | 形式チェック（数字か?） | ValueError で即座に失敗 |
| books.py | ルールチェック（年の範囲） | ValidationError で拒否 |
| book_app.py | エラーキャッチ | ユーザーにメッセージ表示 |

### 3. 間違えても大丈夫

エラーはアプリが「それは許可できません」と教えてくれるだけです。

**重要**: エラーが出ても、本は追加されていません。
```python
# エラーが出た場合
Try:
    collection.add_book(title, author, year)
    print("✅ Book added successfully")
except ValidationError as e:
    print(f"❌ Error: {e}")  # ここで表示
    # 本は追加されない ← 安全
```

---

## エラーハンドリング設計のポイント

### 原則 1: Fail Fast（即座に失敗する）

❌ 悪い例:
```python
try:
    year = int(year_input)
except ValueError:
    year = 0  # 無効な値を返す
    # → 後で add_book() で再びエラー（混乱）
```

✅ 良い例:
```python
try:
    year = int(year_input)
except ValueError as e:
    raise ValueError(f"Year must be a number: {year_input!r}") from e
    # → ユーザーに即座にフィードバック
```

### 原則 2: 例外の種類を分ける

```python
# 入力形式エラー（ユーザーが対処可能）
except ValueError:
    print("Year must be a number")

# ビジネスルール違反エラー（ユーザーが対処可能）
except ValidationError:
    print("Year must be between 1000 and 2026")

# システムエラー（ユーザーが対処不可）
except IOError:
    print("Failed to save collection")
```

### 原則 3: ロギングで問題追跡

```python
import logging
logger = logging.getLogger(__name__)

try:
    year = int(year_input)
except ValueError as e:
    logger.error(f"Year parsing failed: {year_input!r}")  # 開発者向け
    raise ValueError(f"Invalid year: {year_input!r}") from e
```

**ログレベル**:
- `logger.error()` - システムの重大問題
- `logger.warning()` - ユーザーの不正入力
- `logger.info()` - 正常な操作記録

---

## エラーハンドリング改善の背景

### 前のバージョンの問題

```python
# ❌ 古いコード（危険）
try:
    year = int(year_input)
except ValueError:
    print("Invalid year. Defaulting to 0.")
    year = 0  # 無効な値をそのまま返す
```

**何が悪い?**
1. `year=0` は本のルールに違反
2. `add_book()` で再びエラー（ユーザー困惑）
3. エラー発生地点が不明確
4. ロギングなし

**例（ユーザー体験）**:
```
年を入力: "abc"
→ "Invalid year. Defaulting to 0."
→ book added...
→ Error: Year must be between 1000 and 2026
→ ユーザー: "0 の何が悪いの？"
```

### 改善後

```python
# ✅ 新しいコード（安全）
try:
    year = int(year_input)
except ValueError as e:
    logger.error(f"Year parsing failed: {year_input!r}")
    raise ValueError(f"Year must be a valid number. Got: {year_input!r}") from e
```

**改善点**:
1. エラーで即座に失敗（無効値を返さない）
2. ユーザーに直接フィードバック
3. エラー発生地点が明確
4. ロギングで問題追跡可能

---

## デバッグのコツ

### 1. エラーメッセージ全体を読む

❌ 良くない:
```
エラーが出た → リトライ
```

✅ 良い:
```
エラーメッセージを読む → 原因を特定 → 入力を修正
```

### 2. エラースタックトレースを確認（開発者向け）

```python
Traceback (most recent call last):
  File "book_app.py", line 30, in handle_add
    title, author, year = get_book_details()
  File "utils.py", line 73, in get_book_details
    raise ValueError(...) from e
ValueError: Year must be a valid number. Got: 'abc'
```

**読むポイント**:
- 一番下 → 実際のエラー
- その上 → エラーが発生した関数
- さらに上 → 呼び出し元

### 3. print デバッグ（簡易的）

```python
year_input = input("Enter year: ")
print(f"DEBUG: year_input = {year_input!r}, type = {type(year_input)}")
try:
    year = int(year_input)
except ValueError:
    print(f"DEBUG: Conversion failed")
```

---

## 参考リンク

- [BOOKS_API.md](./BOOKS_API.md) - API リファレンス
- [ERROR_HANDLING_FIXES.md](./ERROR_HANDLING_FIXES.md) - 技術者向け詳細ドキュメント
- [books.py](./books.py) - コード内 docstrings
- [utils.py](./utils.py) - 入力処理関数

---

## FAQ

### Q1: なぜ年に 1000 という下限があるの?

**A**: 一般的な図書館システムの設計です。  
- 1000 年前後から本の印刷が始まった
- 無限に遡る必要はない
- 不正な値（0, -100）をフィルタするためのルール

### Q2: エラーが出ました。本は追加されますか?

**A**: されません。  
エラーが出ると、`add_book()` は実行されずに例外で終了します。  
```python
if validation_failed:
    raise ValidationError(...)
    # ここで終了 ↓
# add_book() には到達しない
```

### Q3: エラーメッセージをカスタマイズできますか?

**A**: できます。`books.py` の `_validate_book_input()` でメッセージを編集できます。

```python
# books.py の例
if year < 1000:
    raise ValidationError("古すぎる本です（1000年以降のみ）")
```

### Q4: ログはどこに保存されますか?

**A**: デフォルトでは標準エラー出力（stderr）に表示されます。  
本番環境ではファイルに出力するよう設定できます：

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## まとめ

| 概念 | 説明 | 対処方法 |
|------|------|--------|
| ValueError | 形式が間違っている | 数字など正しい形式で入力 |
| ValidationError | 値がルール違反 | ルール内の値に修正 |
| 入力検証ループ | 無効な選択肢で再プロンプト | 1-5 の中から選択 |
| Fail Fast | エラーで即座に失敗 | デバッグが簡単 |
| Exception Chaining | 元のエラー情報を保持 | 問題追跡が容易 |

---

**次のステップ**: [BOOKS_API.md](./BOOKS_API.md) で API 全体を学ぶ  
**さらに詳しく**: [ERROR_HANDLING_FIXES.md](./ERROR_HANDLING_FIXES.md) で技術詳細を確認
