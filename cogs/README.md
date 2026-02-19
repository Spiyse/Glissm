# Cogs Guide

This project uses a per-file extension model.

## Add a New Command/Cog
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
4. Restart bot or use admin reload/refresh commands.

## Add a New Category
1. Create a folder under `cogs/`, for example `cogs/fun/`.
2. Add your cog files inside that folder.
3. Keep `cogs/fun/__init__.py` minimal (empty or docstring only).

## Important Notes
- Do not put command wiring in package `__init__.py`.
- Auto-discovery loads valid extension modules automatically.
- If you add helper files that are not extensions, exclude them in `cogs/discovery.py`.

## Descriptions
- Command description: use a method docstring.
- Cog-level description: set `self.description` in the cog `__init__`.
