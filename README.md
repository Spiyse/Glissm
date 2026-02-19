# Glissm
Glissm is a multi-purpose Discord bot built with `discord.py`.

## Setup
1. Create a bot at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable **Message Content Intent** (required for prefix commands like `>ping`).
3. Create a `.env` file in the project root:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   COMMAND_PREFIX=>
   OWNER_ID=your_user_id
   ```
4. Invite the bot to your server with `bot` and `applications.commands` scopes.
5. Run the bot:
   ```bash
   python main.py
   ```

## Architecture
- `main.py`: startup, bot events, extension loading.
- `cogs/`: all command/event modules.
- `cogs/discovery.py`: dynamic cog discovery used by startup and admin reload/refresh.

## Cog Loading Rules
- Cogs are auto-discovered from `cogs/**/*.py`.
- `__init__.py` files are skipped.
- Helper/internal modules are filtered in `cogs/discovery.py`.
- Every loadable cog module must include:
  - a `commands.Cog` class
  - `async def setup(bot)` that calls `await bot.add_cog(...)`

## Troubleshooting
- Prefix commands do not respond:
  - check **Message Content Intent** in Discord Developer Portal
  - check bot channel permissions
- Slash commands do not appear:
  - wait for startup sync to complete
  - confirm invite included `applications.commands`
