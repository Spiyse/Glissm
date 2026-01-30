from discord.ext import commands
import config

from logger import logger

class RefreshCommand(commands.Cog):
    @commands.command(name="refresh")
    async def refresh(self, ctx: commands.Context) -> None:
        
        # description for the command
        """Reload all cogs and display results.""" 
        
        loaded = []
        failed = []
        for cog in config.COGS:
            try:
                await self.bot.reload_extension(cog)
                loaded.append(cog.replace("cogs.", ""))
                logger.info("Reloaded cog: %s", cog)
            except commands.ExtensionError as e:
                failed.append(f"{cog}: {e}")
                logger.error("Failed to reload %s: %s", cog, e)
        if failed:
            await ctx.send(f"Refreshed: **{', '.join(loaded)}**\nFailed: **{', '.join(failed)}**")
        else:
            await ctx.send(f"Refreshed all cogs: **{', '.join(loaded)}**")
