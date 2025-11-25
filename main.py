from datetime import datetime
from pathlib import Path

BASE = Path.home() / "todo"
TEMPLATE = Path("templates/default_template.md")

def create_today_file():
    today = datetime.now().strftime("%Y-%m-%d")
    path = BASE / f"{today}.md"

    BASE.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(TEMPLATE.read_text(), encoding="utf-8")
        print(f"{path} を作成しました。")
    else:
        print(f"{path} はすでに存在します。")

if __name__ == "__main__":
    create_today_file()
