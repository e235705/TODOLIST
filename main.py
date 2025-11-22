#!/usr/bin/env python3
import os
import argparse
from datetime import date
from pathlib import Path
import requests
import subprocess
import sys

# optional: pync for macOS notifications
try:
    from pync import Notifier
    HAVE_PYNC = True
except Exception:
    HAVE_PYNC = False

TEMPLATE_PATH = Path(__file__).parent / "templates" / "default_template.md"
TODO_DIR = Path.home() / "todo"
LOG_FILE = Path.home() / ".todo_generator_logs.txt"

LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

def load_template():
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def render_template(tpl: str, d: date):
    return tpl.replace("{{date}}", d.isoformat())

def write_todo_file(content: str, d: date, dry_run=False):
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    fname = TODO_DIR / f"{d.isoformat()}.md"
    if dry_run:
        print(f"[dry-run] would write: {fname}")
        return fname
    fname.write_text(content, encoding="utf-8")
    log(f"created {fname}")
    return fname

def notify_line(message: str):
    if not LINE_TOKEN:
        print("LINE token not configured.")
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": message}
    resp = requests.post(url, headers=headers, data=data)
    print("LINE:", resp.status_code)

def notify_discord(message: str):
    if not DISCORD_WEBHOOK:
        print("Discord webhook not configured.")
        return
    payload = {"content": message}
    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    print("Discord:", resp.status_code)

def notify_macos(title: str, message: str):
    if HAVE_PYNC:
        Notifier.notify(message, title=title)
    else:
        # fallback to osascript
        cmd = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", cmd])

def log(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{text}\n")

def open_with_vscode(path: Path):
    try:
        subprocess.run(["code", str(path)])
    except FileNotFoundError:
        print("VSCode コマンド 'code' が見つかりません。PATHを確認してください。")

def main():
    parser = argparse.ArgumentParser(description="Daily TODO generator")
    parser.add_argument("--date", help="YYYY-MM-DD", default=None)
    parser.add_argument("--open", action="store_true", help="open file in editor")
    parser.add_argument("--no-notify", action="store_true", help="disable notifications")
    parser.add_argument("--dry-run", action="store_true", help="show what will happen")
    args = parser.parse_args()

    d = date.today() if not args.date else date.fromisoformat(args.date)
    tpl = load_template()
    content = render_template(tpl, d)

    fname = write_todo_file(content, d, dry_run=args.dry_run)

    summary = f"ToDo for {d.isoformat()} created: {fname.name}"
    if not args.dry_run and not args.no_notify:
        # Notify destinations
        notify_macos("今日のToDoを作成しました", summary)
        notify_discord(summary)
        notify_line(summary)

    if args.open and not args.dry_run:
        open_with_vscode(fname)

    print("done")

if __name__ == "__main__":
    main()
