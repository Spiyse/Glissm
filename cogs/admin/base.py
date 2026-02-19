from discord.ext import commands
import config

class AdminBase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def cog_check(self, ctx: commands.Context) -> bool:
        if await ctx.bot.is_owner(ctx.author):
            return True
        if config.OWNER_ID and ctx.author.id == config.OWNER_ID:
            return True
        return bool(getattr(config, "OWNER_IDS", None) and ctx.author.id in config.OWNER_IDS)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error,commands.CheckFailure):
            await ctx.send("Only the bot owner can use admin commands.")
            return
        raise error