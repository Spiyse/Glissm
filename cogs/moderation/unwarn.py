import discord
import asyncio
from discord import app_commands
from discord.ext import commands

from database import supabase
from .views import WarningSelectView


class UnwarnCommand(commands.Cog):

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
                .execute()
        )

        return response.data


    @app_commands.command(name="unwarn", description="Remove a warning from a member.")
    @app_commands.guild_only()
    async def unwarn(
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
                "This user has no warnings.",
                ephemeral=True
            )
            return

        view = WarningSelectView(member, warnings)

        await interaction.response.send_message(
            f"Select which warning to remove from {member.mention}",
            view=view,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UnwarnCommand(bot))