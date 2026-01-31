from discord.ext import commands
import discord


class ServerInfoCommand(commands.Cog):
    @commands.command(name="serverinfo", aliases=["si"])
    async def serverinfo(self, ctx: commands.Context) -> None:
        # description for the command
        """Shows the server's general info."""

        embed = discord.Embed(
            title="Server Info",
            description="\nGeneral info about the server :)\n",
            colour=0x00F5A3,
            timestamp=discord.utils.utcnow(),
        )


        embed.set_author(
            name=f"{ctx.guild.name}",
            icon_url="https://cdn.discordapp.com/icons/1317584801854914671/019672d5e103f18d78188cdcca58069a.webp?size=512&quot;);",
        )

        embed.add_field(name="Server ID", value=f"`{ctx.guild.id}`", inline=True)
        embed.add_field(name="Server Name", value=f"`{ctx.guild.name}`", inline=True)
        embed.add_field(name="Created on", value=f"`{ctx.guild.created_at}`", inline=True)
        embed.add_field(name="Region", value=f"`{ctx.guild.preferred_locale}`", inline=True)
        embed.add_field(name="Members", value=f"`{ctx.guild.member_count}`", inline=True)
        embed.add_field(name="Owner", value=f"{ctx.guild.owner.mention}", inline=True)

        embed.set_footer(text="Hi")

        await ctx.send(embed=embed)
