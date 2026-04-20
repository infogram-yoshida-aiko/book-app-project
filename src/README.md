# サンプルソースコード（旧版・任意の参考資料）

> **メモ**: このコースのメインサンプルは `../book-app-project/` にある **Python の書籍コレクションアプリ** です。ここにある JS/React のファイルは以前のコース版で使っていたもので、JavaScript の例も見てみたい学習者向けの補足資料として残しています。

このフォルダーにはサンプルのソースファイルが入っています。学習用の例なので、完全に動作するアプリケーションとして作られているわけではありません。

## 構成

```
src/
├── api/           # API ルートハンドラー
│   ├── auth.js    # 認証エンドポイント
│   └── users.js   # ユーザー CRUD エンドポイント
├── auth/          # クライアント側の認証処理
│   ├── login.js   # ログインフォームのロジック
│   └── register.js # 登録フォームのロジック
├── components/    # React コンポーネント
│   ├── Button.jsx # 再利用できるボタン
│   └── Header.jsx # ナビゲーション付きのアプリヘッダー
├── models/        # データモデル
│   └── User.js    # ユーザーモデル
├── services/      # ビジネスロジック
│   ├── productService.js
│   └── userService.js
├── utils/         # 補助関数
│   └── helpers.js
├── index.js       # アプリのエントリーポイント
└── refactor-me.js # 初心者向けリファクタリング練習用（Chapter 03）
```

## 使い方

コース内の例では、これらのファイルを `@` 構文で参照します。

```bash
copilot

> @samples/src/utils/helpers.js が何をしているか説明して
> @samples/src/api/ にセキュリティ上の問題がないかレビューして
> @samples/src/auth/login.js と @samples/src/auth/register.js を比較して
```

## リファクタリング練習

`refactor-me.js` は、Chapter 03 のリファクタリング練習のために用意されたファイルです。

```bash
copilot

> @samples/src/refactor-me.js 変数 'x' を、よりわかりやすい名前に変更して
> @samples/src/refactor-me.js この関数は長すぎます。より小さな関数に分割して
> @samples/src/refactor-me.js 未使用の変数を削除して
```

## メモ

- ファイルには、レビュー練習で Copilot が見つけられるよう、意図的な TODO や軽微な問題が含まれています
- これは実際に動かすことを目的としたものではないデモコードです。本番利用向けではありません
- `@` を使ったファイル参照構文を学ぶために活用できます
