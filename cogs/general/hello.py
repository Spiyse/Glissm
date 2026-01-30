from discord.ext import commands

class HelloCommand(commands.Cog):
    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context) -> None:
        # description for the command
        """Hello!"""
        
        await ctx.send(f"Hello, {ctx.author.mention}!")
        