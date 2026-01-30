import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent / ".env")

# Main stuff for the bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = (os.getenv("COMMAND_PREFIX") or ">").strip().strip('"\'')

# Cogs to load on startup (module names under cogs/)
COGS = [
    "cogs.general",
]
