# Cogs – how to add commands

Each **folder** = one cog. Commands live in **one file per command**; `__init__.py` only wires them together (no command logic in there).

## Adding a command (same category)

1. **Create a file** in that cog folder, e.g. `cogs/general/mycommand.py`:

```python
from discord.ext import commands

class MycommandCommands(commands.Cog):
    @commands.command(name="mycommand")
    async def mycommand(self, ctx: commands.Context) -> None:
        """What the command does (shows in >help)."""
        await ctx.send("Done!")
```

2. **In that cog’s `__init__.py`**: add the import and add the class to the `General(...)` line:

```python
from . import hello, ping, mycommand   # add mycommand

class General(ping.PingCommands, hello.HelloCommands, mycommand.MycommandCommands):  # add MycommandCommands
```

That’s it. One new file + one line in `__init__`.

## Adding a new category (new cog)

1. Create `cogs/your_category/` with `__init__.py` (copy from `general/`) and your command files.
2. Add `"cogs.your_category"` to `COGS` in `config.py`.

## Adding a description
### Categories
Go into __init_.py for the category that you want to give a description to -

for example the admin one.

class Admin(refresh.RefreshCommand, reload.ReloadCommand, shutdown.ShutdownCommand, restart.RestartCommand):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        commands.Cog.__init__(self)
        self.description = "Owner only commands."

you add ``` self.description = "your description" ```

### Commands

Go into any command file for example hello.py

from discord.ext import commands

class HelloCommand(commands.Cog):
    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context) -> None:
        # description for the command
        """Hello!"""
        
        await ctx.send(f"Hello, {ctx.author.mention}!")
'
you add ``` """Three quotation marks on each side and put text into in the middle like this""" ```

