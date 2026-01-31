from discord.ext import commands

import config

from . import activity, refresh, reload, shutdown, restart, status


class Admin(refresh.RefreshCommand, reload.ReloadCommand, shutdown.ShutdownCommand, restart.RestartCommand,
            activity.ChangeActivityCommand, status.ChangeStatusCommand):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        commands.Cog.__init__(self)
        self.description = "Owner only commands."

    async def cog_check(self, ctx: commands.Context) -> bool:
        if await ctx.bot.is_owner(ctx.author):
            return True
        if config.OWNER_ID and ctx.author.id == config.OWNER_ID:
            return True
        if getattr(config, "OWNER_IDS", None) and ctx.author.id in config.OWNER_IDS:
            return True
        return False

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the bot owner can use admin commands.")
            return
        raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
