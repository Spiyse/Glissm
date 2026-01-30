from discord.ext import commands


class ShutdownCommand(commands.Cog):
    @commands.command(name="shutdown", aliases=["quit", "stop"])
    async def shutdown(self, ctx: commands.Context) -> None:
        
        # description for the command
        """Shut down the bot."""
        
        await ctx.send("Shutting down…")
        await self.bot.close()