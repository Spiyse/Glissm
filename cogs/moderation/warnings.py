import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from database import supabase


class WarningsCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    async def get_warnings(self, guild_id: int, user_id: int):

        loop = asyncio.get_running_loop()

        response = await loop.run_in_executor(
            None,
            lambda: supabase.table("member_warnings")
                .select("*")
                .eq("guild_id", guild_id)
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
        )

        return response.data


    @app_commands.command(name="warnings", description="Show a member's warnings.")
    @app_commands.guild_only()
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        warnings = await self.get_warnings(
            interaction.guild.id,
            member.id
        )

        if not warnings:
            await interaction.response.send_message(
                f"{member.mention} has no warnings.",
                ephemeral=True
            )
            return


        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.orange()
        )

        embed.set_thumbnail(url=member.display_avatar.url)


        for warn in warnings[:10]:   # show max 10

            date = datetime.fromisoformat(
                warn["created_at"]
            ).strftime("%Y-%m-%d %H:%M")

            embed.add_field(
                name=f"Warning #{warn['id']}",
                value=(
                    f"**Reason:** {warn['reason']}\n"
                    f"**Moderator:** <@{warn['moderator_id']}>\n"
                    f"**Date:** {date}"
                ),
                inline=False
            )


        embed.set_footer(
            text=f"Total warnings: {len(warnings)}"
        )


        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(WarningsCommand(bot))