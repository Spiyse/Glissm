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
        sync_msg = ""
        if ctx.guild is not None:
            self.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await self.bot.tree.sync(guild=ctx.guild)
            sync_msg = f"\nSynced **{len(synced)}** app commands to this server."

        if failed:
            await ctx.send(f"Refreshed: **{', '.join(loaded)}**\nFailed: **{', '.join(failed)}**{sync_msg}")
        else:
            await ctx.send(f"Refreshed all cogs: **{', '.join(loaded)}**{sync_msg}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RefreshCommand(bot))
