from discord.ext import commands

from . import hello, ping


class General(ping.PingCommand, hello.HelloCommand):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        commands.Cog.__init__(self)
        self.description = "General utility commands."


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
