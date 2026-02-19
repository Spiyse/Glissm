from discord.ext import commands

class HelloCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context) -> None:
        # description for the command
        """Hello!"""
        
        await ctx.send(f"Hello, {ctx.author.mention}!")
    
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelloCommand(bot))