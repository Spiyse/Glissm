from discord.ext import commands


class PingCommand(commands.Cog):
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        # description for the command
        """Shows the bots ping."""
        
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: **{latency_ms}** ms.")
