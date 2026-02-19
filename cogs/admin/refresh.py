from discord.ext import commands

from .base import AdminBase
from cogs.discovery import discover_cogs
from logger import logger

class RefreshCommand(AdminBase):
    @commands.command(name="refresh")
    async def refresh(self, ctx: commands.Context) -> None:
        
        # description for the command
        """Reload all cogs and display results.""" 
        
        loaded = []
        failed = []
        for cog in discover_cogs():
            try:
                if cog in self.bot.extensions:
                    await self.bot.reload_extension(cog)
                else:
                    await self.bot.load_extension(cog)
                loaded.append(cog.replace("cogs.", ""))
                logger.info("Reloaded cog: %s", cog)
            except commands.ExtensionError as e:
                failed.append(f"{cog}: {e}")
                logger.error("Failed to reload %s: %s", cog, e)
        if failed:
            await ctx.send(f"Refreshed: **{', '.join(loaded)}**\nFailed: **{', '.join(failed)}**")
        else:
            await ctx.send(f"Refreshed all cogs: **{', '.join(loaded)}**")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RefreshCommand(bot))
