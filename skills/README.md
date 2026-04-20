# サンプルスキル

GitHub Copilot CLI ですぐに使えるスキルテンプレートです。どのスキルフォルダーでも、コピーすればすぐに使い始められます。

## クイックスタート

```bash
# スキルを個人用の skills フォルダーにコピー
cp -r hello-world ~/.copilot/skills/

# または、チームで共有できるようにプロジェクトへコピー
cp -r code-checklist .github/skills/
```

## 利用できるスキル

| スキル | 説明 | 向いている用途 |
|-------|-------------|----------|
| `hello-world` | 最小構成の例（形式を学ぶためのもの） | 初めてスキルを作る人 |
| `code-checklist` | Python コード品質チェックリスト（PEP 8、型ヒント、バリデーション） | 一貫した品質チェック |
| `pytest-gen` | 網羅的な pytest テストを生成 | 体系的なテスト生成 |
| `commit-message` | Conventional Commits 形式のコミットメッセージ | 標準化された git 履歴 |

## スキルの動作のしくみ

スキルは、プロンプトがスキルの `description` に一致すると **自動で起動** します。手動で呼び出す必要はありません。

```bash
copilot

> このコードの品質上の問題をチェックして
# Copilot が "code-checklist" スキルに一致すると判断し、自動で読み込みます

> コミットメッセージを生成して
# Copilot が "commit-message" スキルを読み込みます
```

スキルは直接呼び出すこともできます。
```bash
> /code-checklist books.py をチェックして
> /pytest-gen BookCollection のテストを生成して
> /commit-message
```

## スキルの構成

各スキルは、`SKILL.md` ファイルを含むフォルダーです。

```
skill-name/
└── SKILL.md    # 必須: フロントマターと説明を書く
```

`SKILL.md` には、`name` と `description` を含む YAML フロントマターがあります（どちらも必須です）。

```markdown
---
name: my-skill
description: このスキルが何をするか、いつ使うか
---

# スキルの指示

ここに指示を書きます...
```

## さらにスキルを探す

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - コミュニティ作成のスキルがまとまった GitHub 公式リソース
- **`/plugin marketplace`** - Copilot CLI の中からスキルを探してインストール

## 独自のスキルを作る

1. フォルダーを作成する: `mkdir ~/.copilot/skills/my-skill`
2. フロントマター付きの `SKILL.md` を作成する
3. 指示を書く
4. 説明に合う内容を Copilot に依頼してテストする

詳しくは [Chapter 05: Skills](../../05-skills/README.md) を参照してください。
