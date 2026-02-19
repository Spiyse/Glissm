import discord
from discord.ext import commands


class TestCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="test_join")
    @commands.is_owner()
    async def test_member_join(self, ctx: commands.Context) -> None:
        member_events = ctx.bot.get_cog("MemberEvents")
        if member_events:
            await member_events.on_member_join(ctx.author)
            await ctx.send("Tested member join event")
        else:
            await ctx.send("MemberEvents cog not found")

    @commands.command(name="test_left")
    @commands.is_owner()
    async def test_member_left(self, ctx: commands.Context) -> None:
        """Test member left message."""
        member_events = ctx.bot.get_cog("MemberEvents")

        if member_events:
            embed = member_events.create_leave_embed(
                member=ctx.author,
                reason="Left",
                color=discord.Color.red(),
            )
            channel = ctx.bot.get_channel(ctx.channel.id)
            await channel.send(embed=embed)
            await ctx.send("Tested member left event")
        else:
            await ctx.send("MemberEvents cog not found")

    @commands.command(name="test_kicked")
    @commands.is_owner()
    async def test_member_kicked(self, ctx: commands.Context) -> None:
        """Test member kicked message."""
        member_events = ctx.bot.get_cog("MemberEvents")

        if member_events:
            embed = member_events.create_leave_embed(
                member=ctx.author,
                reason="Kicked",
                color=discord.Color.orange(),
                moderator=ctx.author,
                reason_text="Spamming",
            )
            channel = ctx.bot.get_channel(ctx.channel.id)
            await channel.send(embed=embed)
            await ctx.send("Tested member kicked event")
        else:
            await ctx.send("MemberEvents cog not found")

    @commands.command(name="test_banned")
    @commands.is_owner()
    async def test_member_banned(self, ctx: commands.Context) -> None:
        """Test member banned message."""
        member_events = ctx.bot.get_cog("MemberEvents")

        if member_events:
            embed = member_events.create_leave_embed(
                member=ctx.author,
                reason="Banned",
                color=discord.Color.dark_red(),
                moderator=ctx.author,
                reason_text="Violating server rules",
            )
            channel = ctx.bot.get_channel(ctx.channel.id)
            await channel.send(embed=embed)
            await ctx.send("Tested member banned event")
        else:
            await ctx.send("MemberEvents cog not found")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestCommand(bot))
