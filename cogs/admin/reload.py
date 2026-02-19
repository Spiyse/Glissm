from discord.ext import commands

from .base import AdminBase
from cogs.discovery import discover_cogs
from logger import logger

class ReloadCommand(AdminBase):
    @commands.command(name="reload")
    async def reload(self, ctx: commands.Context, cog_name: str) -> None:
        
        # description for the command
        """Reload a specific cog by name."""
        
        cog_name = cog_name.lower().strip()
        full_name = cog_name if cog_name.startswith("cogs.") else f"cogs.{cog_name}"
        known_cogs = discover_cogs()
        if full_name not in known_cogs:
            display = ", ".join(c.replace("cogs.", "") for c in known_cogs)
            await ctx.send(f"Unknown cog. Known: **{display}**")
            return
        try:
            if full_name not in self.bot.extensions:
                await self.bot.load_extension(full_name)
            else:
                await self.bot.reload_extension(full_name)
            logger.info("Reloaded cog: %s", full_name)
            await ctx.send(f"Reloaded **{full_name}**.")
        except commands.ExtensionError as e:
            await ctx.send(f"Failed to reload: **{e}**")
            
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReloadCommand(bot))
