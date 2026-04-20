# バグ入りコードのサンプル

このフォルダには、GitHub Copilot CLI を使ったコードレビューやデバッグ練習のために、意図的にバグを入れたコードが入っています。

## フォルダ構成

```
buggy-code/
├── js/                    # JavaScript のサンプル
│   ├── userService.js     # ユーザー管理（バグ 8 個）
│   └── paymentProcessor.js # 支払い処理（バグ 8 個）
└── python/                # Python のサンプル
    ├── user_service.py    # ユーザー管理（バグ 10 個）
    └── payment_processor.py # 支払い処理（バグ 12 個）
```

## クイックスタート

### JavaScript

```bash
copilot

# セキュリティ監査
> Review @samples/buggy-code/js/userService.js for security issues

# バグをすべて見つける
> Find all bugs in @samples/buggy-code/js/paymentProcessor.js
```

### Python

```bash
copilot

# セキュリティ監査
> Review @samples/buggy-code/python/user_service.py for security issues

# バグをすべて見つける
> Find all bugs in @samples/buggy-code/python/payment_processor.py
```

## バグの種類

### 両方の言語に共通するもの

| バグの種類 | 説明 |
|----------|-------------|
| SQL インジェクション | SQL クエリにユーザー入力をそのまま埋め込んでいる |
| ハードコードされた秘密情報 | API キーやパスワードがソースコードに埋め込まれている |
| 競合状態 | 共有状態に適切な同期がない |
| 機密データのログ出力 | パスワードやカード番号がログに出力される |
| 入力値検証の不足 | ユーザーが入力したデータのチェックがない |
| エラーハンドリングなし | try/catch や try/except のブロックがない |
| 弱いパスワード比較 | 平文比較、またはタイミング攻撃に弱い比較をしている |
| 認可チェック不足 | 認可確認なしで操作できてしまう |

### Python 特有のバグ

| バグの種類 | 説明 |
|----------|-------------|
| Pickle のデシリアライズ | 信頼できないデータに対して `pickle.loads()` を使っている |
| eval() インジェクション | ユーザー入力を `eval()` に渡している |
| 安全でない YAML の読み込み | セーフローダーなしで `yaml.load()` を使っている |
| シェルインジェクション | `os.system()` の呼び出しにユーザー入力をそのまま使っている |
| 弱いハッシュ化 | パスワードハッシュに MD5 を使っている |
| 安全でない乱数 | セキュリティ用途に `random` module を使っている |

## 練習課題

1. **セキュリティ監査**: 包括的なセキュリティレビューを実行し、すべての脆弱性を重要度ごとに整理してみましょう
2. **バグを 1 つ修正する**: 重大なバグを 1 つ選び、Copilot に修正案を出してもらい、なぜそれで直るのかを理解しましょう
3. **テストを作る**: デプロイ前にこうしたバグを見つけられるテストを作ってみましょう
4. **安全にリファクタリングする**: 動作を保ちながら SQL インジェクションのバグを修正してみましょう
