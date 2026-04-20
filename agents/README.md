# サンプルエージェント定義

このフォルダーには、GitHub Copilot CLI でエージェントを使い始めるときに役立つ、シンプルなエージェントテンプレートが入っています。

## クイックスタート

```bash
# エージェントを個人用の agents フォルダーにコピー
cp hello-world.agent.md ~/.copilot/agents/

# または、チームで共有できるようにプロジェクトへコピー
cp python-reviewer.agent.md .github/agents/
```

## このフォルダーにあるサンプルファイル

| ファイル | 説明 | 向いている用途 |
|------|-------------|----------|
| `hello-world.agent.md` | 最小構成の例（11 行） | 形式を学ぶ |
| `python-reviewer.agent.md` | Python コード品質レビュー担当 | コードレビュー、PEP 8、型ヒント |
| `pytest-helper.agent.md` | Pytest テスト支援の専門家 | テスト生成、フィクスチャ、境界ケース |

## さらにエージェントを探す

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - コミュニティ作成のエージェントや使い方がまとまった GitHub 公式リソース

---

## エージェントファイルの形式

各エージェントファイルには、少なくとも `description` を含む YAML フロントマターが必要です。

```markdown
---
name: my-agent
description: このエージェントが何をするかの簡単な説明
tools: ["read", "edit", "search"]  # 任意: 使用できるツールを制限
---

# エージェント名

ここにエージェントへの指示を書きます...
```

**利用できる YAML プロパティ:**

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `description` | **はい** | エージェントが何をするか |
| `name` | いいえ | 表示名（省略時はファイル名） |
| `tools` | いいえ | 使用を許可するツールの一覧（省略するとすべて使用可能）。下の別名も参照してください。 |
| `target` | いいえ | `vscode` または `github-copilot` のみに制限 |

**ツールの別名**: `read`, `edit`, `search`, `execute` (shell), `web`, `agent`

> 💡 **メモ**: `model` プロパティは VS Code では使えますが、Copilot CLI ではまだサポートされていません。
>
> 📖 **公式ドキュメント**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)

## エージェントファイルの保存場所

エージェントは次の場所に保存できます。
- `~/.copilot/agents/` - すべてのプロジェクトで使えるグローバルエージェント
- `.github/agents/` - プロジェクト専用のエージェント
- `.agent.md` files - VS Code 互換の形式

各エージェントは `.agent.md` 拡張子を持つ個別ファイルです。

---

## 使い方の例

```bash
# 特定のエージェントで開始
copilot --agent python-reviewer

# または、セッション中に対話的にエージェントを選択
copilot
> /agent
# 一覧から "python-reviewer" を選択

# その後のプロンプトには、そのエージェントの専門性が適用されます
> @samples/book-app-project/books.py このコードの品質上の問題をレビューして

# 別のエージェントに切り替え
> /agent
# "pytest-helper" を選択

> @samples/book-app-project/tests/test_books.py 追加するとよいテストはありますか？
```

---

## 独自のエージェントを作る

1. `~/.copilot/agents/` に `.agent.md` 拡張子の新しいファイルを作成する
2. 少なくとも `description` を含む YAML フロントマターを追加する
3. わかりやすい見出しを付ける（例: `# Security Agent`）
4. エージェントの専門分野、基準、ふるまいを定義する
5. `/agent` または `--agent <name>` で使う

**効果的なエージェントを作るコツ:**
- 専門分野は具体的に書く
- コード規約やパターンを含める
- 何をチェックするのかを明確にする
- 出力形式の希望も書いておく
