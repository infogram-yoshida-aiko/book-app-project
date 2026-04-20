# 書籍コレクションアプリ

*(この README は、GitHub Copilot CLI を使って改善できるよう、あえて粗めに書かれています)*

手元にある本や、これから読みたい本を管理するための Python アプリです。本の追加、削除、一覧表示ができ、既読としてマークすることもできます。

**本アプリの最大の特徴**: エラーハンドリング設計が本番品質で、ユーザーに親切なエラーメッセージが表示されます。

---

## クイックスタート

```bash
# 本を追加する
python book_app.py add

# すべての本を表示する
python book_app.py list

# 著者で本を検索する
python book_app.py find

# 本を削除する
python book_app.py remove

# ヘルプを表示する
python book_app.py help
```

---

## ドキュメント

### 初心者向け
- **[ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md)** ← 最初に読んでください
  - エラーの種類
  - よくあるシナリオ
  - 対処方法の解説
  - FAQ

- **[BOOKS_API.md](./BOOKS_API.md)**
  - API リファレンス
  - 使用例
  - トラブルシューティング

### 技術者向け
- **[ERROR_HANDLING_FIXES.md](./ERROR_HANDLING_FIXES.md)**
  - 改善内容の詳細
  - Before/After コード比較
  - テスト推奨事項

- **[ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md)**
  - システム設計
  - レイヤー構成
  - データフロー

---

## 機能一覧

| 機能 | 説明 |
|------|------|
| **Add a book** | 新しい本を追加（タイトル、著者、出版年） |
| **List books** | コレクション内のすべての本を表示 |
| **Mark as read** | 本を既読としてマーク |
| **Remove a book** | コレクションから本を削除 |
| **Find by author** | 著者で本を検索 |

---

## ファイル構成

```
book-app-project/
├── book_app.py              # メイン CLI エントリーポイント
├── books.py                 # BookCollection クラス（データ処理）
├── utils.py                 # UI・入力処理のヘルパー
├── data.json                # 本のデータ（JSON 形式）
├── tests/                   # pytest テストスイート
├── README.md                # このファイル
├── BOOKS_API.md             # API リファレンス
├── ERROR_HANDLING_GUIDE.md  # エラー対応ガイド
├── ERROR_HANDLING_FIXES.md  # 技術者向け改善レポート
└── ARCHITECTURE_ANALYSIS.md # システムアーキテクチャ
```

---

## テストの実行

```bash
# すべてのテストを実行
python -m pytest tests/

# 詳細な出力で実行
python -m pytest tests/ -v

# カバレッジ付きで実行
python -m pytest tests/ --cov=books --cov=utils
```

---

## エラーハンドリング

本アプリは以下の原則に従っています：

✅ **Fail Fast** - エラーで即座に失敗（無効値を返さない）  
✅ **明確なエラーメッセージ** - ユーザーが対処できるレベルの情報  
✅ **ログ記録** - 問題追跡用の詳細情報  
✅ **入力検証** - 複数レベルのバリデーション

> エラーが出ても、本のデータは追加・変更されません。安全に再試行できます。

例：
```
Enter publication year: invalid
❌ Error: Year must be a valid number. Got: 'invalid'

Add a New Book
Enter book title:
```

詳しくは [ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md) を参照。

---

## 本番環境への適用

本アプリはそのまま本番環境で使用できるよう設計されています：

- ✅ 入力バリデーション完備
- ✅ エラーハンドリング実装
- ✅ ロギング機能
- ✅ 例外チェーニング対応
- ✅ Google スタイル docstrings

### 次のステップ
1. データベース（PostgreSQL など）への移行
2. Web API (Flask/FastAPI) 化
3. ユニットテスト拡充
4. CI/CD パイプライン統合

---

## 改善の歴史

### [2026-04-20] エラーハンドリング包括改善

- ✅ year=0 デフォルト値バグを削除
- ✅ 入力検証ループを追加
- ✅ Exception chaining 対応
- ✅ ロギング統合
- ✅ Google スタイル docstrings 追加

詳細は [ERROR_HANDLING_FIXES.md](./ERROR_HANDLING_FIXES.md) を参照。

---

## よくある質問

**Q: エラーが出たら本は追加されますか?**  
A: されません。エラーが発生すると処理は止まり、本のデータは変更されません。

**Q: なぜ年に下限（1000）があるのか?**  
A: 一般的な図書館システムの設計です。詳しくは [ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md#q1-なぜ年に-1000-という下限があるの) を参照。

**Q: エラーメッセージをカスタマイズできますか?**  
A: できます。`books.py` の `_validate_book_input()` を編集してください。

---

## 参考資料

- Python 公式ドキュメント: [例外処理](https://docs.python.org/ja/3/tutorial/errors.html)
- PEP 8: [Python コードのスタイルガイド](https://pep8-ja.readthedocs.io/)
- [Google Python スタイルガイド](https://google.github.io/styleguide/pyguide.html)
