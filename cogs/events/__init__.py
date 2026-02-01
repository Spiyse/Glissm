from discord.ext import commands
from .member_events import MemberEvents


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEvents(bot))