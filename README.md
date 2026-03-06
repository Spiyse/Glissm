# Glissm
Glissm is a multi-purpose Discord bot built with `discord.py` and dynamic cog loading.

## Features
- Prefix and slash command support
- Dynamic cog discovery (`cogs/discovery.py`)
- Admin reload/refresh workflow for fast iteration
- Moderation tooling with warning storage (Supabase)

## Quickstart
1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable intents:
- `Message Content Intent` (required for prefix commands like `>ping`)
- `Server Members Intent` (recommended for moderation/member features)
3. Create a `.env` file in the project root:
```env
DISCORD_TOKEN=
COMMAND_PREFIX=>
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
