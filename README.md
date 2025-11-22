# Daily ToDo Generator （Python）

Python で **毎朝の ToDo ファイルを自動生成し、LINE / Discord / macOS 通知も行うツール** の README です。
VSCode をメイン開発環境として 36 時間以内に完成させられるシンプルな構成になっています。

---

## 📌 概要

このツールは、以下を自動で行う **独自の ToDo 生成ツール** です：

* 毎朝手動でコマンドを実行すると、その日の ToDo Markdown を生成
* 生成した ToDo を LINE と Discord に送信
* macOS 通知センターに通知
* PC 起動時にも自動実行可能（macOS LaunchAgent）
* テンプレートベースで編集が容易

ファイルは `~/todo/YYYY-MM-DD.md` の形で保存されます。

---

## 📁 ディレクトリ構成

```
todo-generator/
├── main.py                # 実行スクリプト
├── templates/
│   └── default_template.md # ToDoテンプレート
├── config.example.json    # 設定ファイルの例（任意）
└── README.md
```

---

## 🧩 1. テンプレート設定

ToDo の初期内容は `templates/default_template.md` から生成されます。

例：

```md
# {{date}} の ToDo

## 最優先
- [ ] タスク1

## 勉強
- [ ] 学習 30分

## プロジェクト
- [ ] プロジェクトA

## 習慣
- [ ] 筋トレ
- [ ] 日記

## メモ
- 自由記述
```

`{{date}}` は自動的に置換されます。

---

## 🔐 2. 環境変数の設定（重要）

通知に必要な情報は **環境変数で管理** します。

### LINE Notify トークン

1. LINE Notify にログイン
2. 「トークンを発行」で個人 or グループ用トークンを取得
3. macOS の `~/.zshenv` に追加

```bash
export LINE_NOTIFY_TOKEN="YOUR_TOKEN_HERE"
```

### Discord Webhook URL

Discord サーバー → チャンネル設定 → Integrations → Webhooks → URL をコピー

```bash
export DISCORD_WEBHOOK_URL="YOUR_WEBHOOK_URL"
```

編集後：

```bash
source ~/.zshenv
```

※ セキュリティのため **GitHub に絶対に公開しないこと**。

---

## 🖥 3. 必要パッケージ

```bash
pip install requests pync python-dateutil
```

macOS 通知用に `pync` を使います（動かない場合は自動で osascript に fallback）。

---

## ⚙️ 4. 実行方法

### 基本

```bash
python main.py
```

→ `~/todo/2025-01-01.md` のようなファイルが生成されます。

### よく使うオプション

```
--open      生成後に VSCode で開く
--dry-run   何が行われるかだけを表示
--no-notify 通知をオフにする
--date      任意の日付で生成
```

例：

```bash
python main.py --open
```

---

## 🔔 5. 通知仕様

### LINE 通知

メッセージ本文を通知。成功するとステータス 200。

### Discord 通知

Webhook にテキストを送信。

### macOS 通知

`pync` が利用可能ならそれを使用。
利用不可の場合：

```bash
osascript -e 'display notification "message" with title "title"'
```

---

## 🚀 6. Mac 起動時に自動実行（任意）

PC 起動後に自動で今日の ToDo を作らせたい場合、LaunchAgent を使います。

### 設定ファイル作成

`~/Library/LaunchAgents/com.todo.daily.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.todo.daily</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/path/to/todo-generator/main.py</string>
  </array>

  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
```

ロード：

```bash
launchctl load ~/Library/LaunchAgents/com.todo.daily.plist
```

---

## 🧪 7. 動作テスト（推奨）

1. `--dry-run` で内容確認
2. `python main.py` でファイル生成確認
3. LINE / Discord 通知が届くか確認
4. macOS 通知が表示されるか確認
5. LaunchAgent を設定してログインして動作を確認

---

## 🛡 セキュリティ注意

* トークン類は絶対に GitHub に公開しない
* `.gitignore` に `config.json` と秘密情報を追加
* LINE Notify はレート制限あり（連投に注意）

---

## 🔧 拡張案

* Notion / Slack への追加出力
* テンプレートをマルチファイル化
* GitHub コミット履歴として「毎日のToDo進捗」をログ化
* 習慣トラッカー機能の追加

---
Lineは追加しませんでした。