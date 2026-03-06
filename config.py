import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent / ".env")

# Main stuff for the bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = (os.getenv("COMMAND_PREFIX") or ">").strip().strip('"\'')

# Owner id (set in .env)
_raw = os.getenv("OWNER_ID")
OWNER_ID = int(_raw) if _raw and _raw.isdigit() else None
OWNER_IDS = []
 
 # Channels where the member join and leave messages get sent ( set in .env )
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID")) if os.getenv("LOG_CHANNEL_ID") else None
LEAVE_CHANNEL_ID = int(os.getenv("LEAVE_CHANNEL_ID")) if os.getenv("LEAVE_CHANNEL_ID") else None

# Warn system settings
AUTO_TIMEOUT_HOURS = 1
AUTO_TIMWOUT_WARNING_AMOUNT = 3
AUTO_KICK_WARNING_AMOUNT = 5
AUTO_BAN_WARNING_AMOUNT = 7

# Moderation access control
_mod_role_ids = (os.getenv("MOD_ROLE_IDS") or "").split(",")
MOD_ROLE_IDS = {
    int(role_id.strip())
    for role_id in _mod_role_ids
    if role_id.strip().isdigit()
}

_mod_role_names = (os.getenv("MOD_ROLE_NAMES") or "mod,moderator").split(",")
MOD_ROLE_NAMES = {name.strip().lower() for name in _mod_role_names if name.strip()}

