from discord.ext import commands
import config
import os
import sys
import subprocess

from logger import logger


class RestartCommand(commands.Cog):
    @commands.command(name="restart")
    async def restart(self, ctx: commands.Context) -> None:
        
        # description for the command
        """Reload all cogs and restart the bot process."""
        
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
            await ctx.send(f"Reloaded: **{', '.join(loaded)}**\nFailed: **{', '.join(failed)}**\nRestarting bot...")
        else:
            await ctx.send(f"Reloaded all cogs: **{', '.join(loaded)}**\nRestarting bot...")
        
        logger.info("Restarting bot process")
        
        subprocess.Popen([sys.executable, "main.py"], cwd=os.path.dirname(os.path.abspath(__file__)).replace("\\cogs\\admin", ""))
        await self.bot.close()
