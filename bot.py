import discord
from discord.ext import commands
from pathlib import Path
from datetime import datetime
import json
import requests

# 設定読み込み
CONFIG = Path("config.json")
cfg = json.loads(CONFIG.read_text())
BOT_TOKEN = cfg["discord_bot_token"]
WEBHOOK = cfg["discord_webhook"]

BASE = Path.home() / "todo"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def report(ctx):
    """今日のTodoをDiscordに送信する"""
    today_file = BASE / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    if not today_file.exists():
        await ctx.send("今日のTodoファイルがありません。")
        return

    content = today_file.read_text()

    # Webhook送信
    requests.post(WEBHOOK, json={"content": f"本日の完了報告:\n\n{content}"})
    await ctx.send("完了報告を送信しました！")

bot.run(BOT_TOKEN)
