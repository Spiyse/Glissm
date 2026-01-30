from discord.ext import commands
import logging
import config

logger = logging.getLogger("glissm")

class ReloadCommand(commands.Cog):
    @commands.command(name="reload")
    async def reload(self, ctx: commands.Context, cog_name: str) -> None:
        
        # description for the command
        """Reload a specific cog by name."""
        
        cog_name = cog_name.lower().strip()
        full_name = cog_name if cog_name.startswith("cogs.") else f"cogs.{cog_name}"
        if full_name not in config.COGS:
            await ctx.send(f"Unknown cog. Known: **{', '.join(c.replace('cogs.', '') for c in config.COGS)}**")
            return
        try:
            await self.bot.reload_extension(full_name)
            logger.info("Reloaded cog: %s", full_name)
            await ctx.send(f"Reloaded **{full_name}**.")
        except commands.ExtensionError as e:
            await ctx.send(f"Failed to reload: **{e}**")