# 書籍コレクションアプリ

*(この README は、GitHub Copilot CLI を使って改善できるよう、あえて粗めに書かれています)*

手元にある本や、これから読みたい本を管理するための JavaScript アプリです。
本の追加、削除、一覧表示ができ、既読としてマークすることもできます。

---

## 現在の機能

* JSON ファイル（このアプリのデータベース）から本の情報を読み込みます
* 一部では入力チェックがまだ弱めです
* テストはいくつかありますが、まだ十分とは言えません

---

## ファイル

* `book_app.js` - メインの CLI エントリーポイント
* `books.js` - データ処理を担当する BookCollection クラス
* `utils.js` - UI と入力処理のためのヘルパー関数
* `data.json` - サンプルの書籍データ
* `tests/test_books.js` - Node の組み込みテストランナーを使った出発点用のテストコード

---

## アプリの実行

```bash
node book_app.js list
node book_app.js add
node book_app.js find
node book_app.js remove
node book_app.js help
```

## テストの実行

```bash
npm test
```

---

## メモ

* もちろん、本番運用向けに仕上がっているわけではありません
* 改善の余地があるコードがいくつかあります
* あとからコマンドを増やすこともできます
