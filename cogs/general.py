import discord
from discord.ext import commands

# This holds the general-purpose commands like ping, help, etc.

class General(commands.Cog):
    # Basic utility commands

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        # Check bot latency
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: **{latency_ms}** ms.")

    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context) -> None:
        # Says Hello
        await ctx.send(f"Hello, {ctx.author.mention}!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
