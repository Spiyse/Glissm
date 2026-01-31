from discord.ext import commands

from . import uptime, serverinfo


class Utility(uptime.UptimeCommand, serverinfo.ServerInfoCommand):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.description = "Utility commands."


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))
    
