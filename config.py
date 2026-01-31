import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent / ".env")

# Main stuff for the bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = (os.getenv("COMMAND_PREFIX") or ">").strip().strip('"\'')

# put your Discord user ID for admin commands :)
_raw = os.getenv("OWNER_ID")
OWNER_ID = int(_raw) if _raw and _raw.isdigit() else None
OWNER_IDS = []

# Cogs to load on startup
COGS = [
    "cogs.general",
    "cogs.admin",
    "cogs.utility",
]
