# Cogs Guide
This project uses a per-file extension model. Each loadable module is expected to be self-contained.

## Quick Rules
- One cog module per file
- Every loadable module must define `async def setup(bot)`
- Keep package `__init__.py` files minimal
- Shared helpers should not be treated as extensions

## Add a New Cog
1. Create a file, for example `cogs/general/mycommand.py`.
2. Add a cog class and command(s):
```python
from discord.ext import commands

class MyCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="mycommand")
    async def mycommand(self, ctx: commands.Context) -> None:
        await ctx.send("Done!")
```
3. Add the extension entry point in the same file:
```python
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCommand(bot))
```
4. Restart the bot or use admin reload/refresh commands.

## Add a New Category
1. Create a folder under `cogs/` (example: `cogs/fun/`).
2. Add cog files in that folder.
3. Keep `cogs/fun/__init__.py` empty (or docstring only).

## Discovery Behavior
- Discovery scans `cogs/**/*.py`
- `__init__.py` is skipped
- Files under `utils` are skipped
- Modules without `setup(bot)` are skipped
- Modules listed in the blocked list in `cogs/discovery.py` are skipped

## Good Practices
- Put user-facing command details in command docstrings
- Keep shared UI/components in dedicated helper modules
- Keep permission checks centralized when possible
