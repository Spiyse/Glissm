from discord.ext import commands
import discord
import datetime, time

class UptimeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.startTime = time.time()
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.startTime = time.time()
    
    @commands.command(name="uptime")
    async def ping(self, ctx: commands.Context) -> None:
        # description for the command
        """Shows the bots uptime."""
        
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-self.startTime))))
        
        embed = discord.Embed(
            title="Uptime",
            description=f"\n```\n{uptime}\n```",
            timestamp=discord.utils.utcnow()
            )

        embed.set_footer(text="Requested")
        
        await ctx.send(embed=embed)
            

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UptimeCommand(bot))         
