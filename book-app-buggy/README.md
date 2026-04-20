# 書籍アプリ - バグ入り版

このディレクトリには、第 03 章のデバッグ練習用として、意図的にバグを入れた書籍コレクションアプリが入っています。

**これらのバグを直接修正しないでください。** 学習者が GitHub Copilot CLI を使って問題を見つけ、デバッグする練習ができるように用意されています。

---

## 意図的に入れてあるバグ

### books_buggy.py

| # | バグ | 症状 |
|---|-----|---------|
| 1 | `find_book_by_title()` が大文字・小文字まで含めて完全一致で比較する | データに "The Hobbit" があるのに "the hobbit" で検索すると何も返りません |
| 2 | `save_books()` でコンテキストマネージャーを使っていない | ファイルハンドルがリークします。権限エラー時の処理もありません |
| 3 | `add_book()` に年のバリデーションがない | 負の年、0 年、かなり未来の年も受け付けてしまいます |
| 4 | `remove_book()` が `in` の部分文字列チェックを使っている | "Dune" を削除すると "Dune Messiah" にも一致して削除されます |
| 5 | `mark_as_read()` がすべての本を既読にしてしまう | ループ変数のバグで、一致した本だけでなく全件を処理してしまいます |
| 6 | `find_by_author()` が完全一致を必要とする | "Tolkien" で "J.R.R. Tolkien" を見つけられません（部分一致なし） |

### book_app_buggy.py

| # | バグ | 症状 |
|---|-----|---------|
| 7 | `show_books()` の番号付けが 0 から始まる | 本が "1. ...", "2. ..." ではなく "0. ...", "1. ..." と表示されます |
| 8 | `handle_add()` が空の title/author を受け付ける | タイトルや著者が空のままの本を追加できてしまいます |
| 9 | `handle_remove()` が常に成功メッセージを出す | 本が見つからなかった場合でも "Book removed" と表示されます |

---

## 第 03 章での使い方

```bash
copilot

> @samples/book-app-buggy/books_buggy.py Users report that searching for
> "The Hobbit" returns no results even though it's in the data. Debug why.

> @samples/book-app-buggy/book_app_buggy.py When I remove a book that
> doesn't exist, the app says it was removed. Help me find why.
```
