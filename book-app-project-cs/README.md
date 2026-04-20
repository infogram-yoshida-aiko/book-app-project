# 書籍コレクションアプリ

*(この README は、GitHub Copilot CLI を使って改善できるよう、あえて粗めに書かれています)*

手元にある本や、これから読みたい本を管理するための C# のコンソールアプリです。
本の追加、削除、一覧表示ができ、既読としてマークすることもできます。

---

## 現在の機能

* JSON ファイル（このアプリのデータベース）から本の情報を読み込みます
* 一部では入力チェックがまだ弱めです
* テストはいくつかありますが、まだ十分とは言えません

---

## ファイル

* `Program.cs` - メインの CLI エントリーポイント
* `Models/Book.cs` - 書籍を表すモデルクラス
* `Services/BookCollection.cs` - データ処理を担当する BookCollection クラス
* `data.json` - サンプルの書籍データ
* `Tests/BookCollectionTests.cs` - xUnit テスト

---

## アプリの実行

```bash
dotnet run -- list
dotnet run -- add
dotnet run -- find
dotnet run -- remove
dotnet run -- help
```

## テストの実行

```bash
cd Tests
dotnet test
```

---

## メモ

* もちろん、本番運用向けに仕上がっているわけではありません
* 改善の余地があるコードがいくつかあります
* あとからコマンドを増やすこともできます
