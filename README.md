# Glissm
Glissm is a multi-purpose Discord bot built with `discord.py` and dynamic cog loading.


## Features
- Prefix and slash command support
- Dynamic cog discovery (`cogs/discovery.py`)
- Admin reload/refresh workflow for fast iteration
- Moderation tooling with warning storage (Supabase)

## Commands
```
MODERATION (slash commands)

  /ban         ban member with optional message deletion (0-7 days)
  /kick        remove member from server
  /timeout     silence member for specified duration (max 28d)
  /warn        issue warning to member (stored in database)
  /unwarn      remove specific warning from record
  /warnings    view member's warning history (10 most recent)

ADMIN (owner only)

  change_activity (ca)     modify bot activity status
  change_status (cs)       set online status (online/idle/dnd/offline)
  refresh                  reload all cogs + sync commands
  reload <cog>             reload specific cog
  restart                  full bot restart
  shutdown (quit/stop)     terminate bot process

UTILITY

  serverinfo (si)          detailed server information
  uptime                   bot runtime since last restart
  hello                    personalized greeting
  ping                     display bot latency
```

## Quickstart
1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable intents:
- `Message Content Intent` (required for prefix commands like `>ping`)
- `Server Members Intent` (recommended for moderation/member features)
3. Create a `.env` file in the project root:
```env
DISCORD_TOKEN=
OWNER_ID=
LOG_CHANNEL_ID=
LEAVE_CHANNEL_ID=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
MOD_ROLE_IDS=
MOD_ROLE_NAMES=mod,moderator
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Run the bot:
```bash
python main.py
```

## Invite to server

if you don't want to self host, i have custom verison of the bot hosted on my own server that runs 24/7.
all the info is on my site https://spiyse.github.io/Glissm-Bot-Website/

## Project Layout
- `main.py`: startup, event wiring, extension loading
- `config.py`: environment parsing and runtime config
- `database.py`: Supabase client setup
- `help_command.py`: custom grouped help command
- `cogs/`: command/event modules

## Cog Discovery Rules
- Auto-discovers Python modules under `cogs/**`
- Skips `__init__.py`
- Skips utility/internal modules listed in `cogs/discovery.py`
- Loads only modules that define `setup(bot)`

## Troubleshooting
### Prefix commands not responding
- Confirm `Message Content Intent` is enabled
- Confirm the bot can read/send messages in the channel
- Confirm your prefix matches `COMMAND_PREFIX`

### Slash commands not showing
- Restart the bot and wait for sync to complete
- Confirm invite includes `applications.commands`
- Confirm command checks (owner/mod roles) are satisfied

## Development Notes
- Keep extension entry points in each cog file (`async def setup(bot)`).
- Avoid loading cogs from package `__init__.py` files.
- Use admin `reload`/`refresh` commands while developing.
