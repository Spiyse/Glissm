from discord.ext import commands
import discord

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot    
    
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        # description for the command
        """Shows the bots ping."""
        
        latency_ms = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="Latency",
            description=f"\n```\n{latency_ms} ms\n```",
            timestamp=discord.utils.utcnow()
            )

        embed.set_footer(text="Requested")
        
        await ctx.send(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCommand(bot))