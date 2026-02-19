from discord.ext import commands
from .base import AdminBase

class ShutdownCommand(AdminBase):
    @commands.command(name="shutdown", aliases=["quit", "stop"])
    async def shutdown(self, ctx: commands.Context) -> None:
        
        # description for the command
        """Shut down the bot."""
        
        await ctx.send("Shutting down…")
        await self.bot.close()
        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ShutdownCommand(bot))
