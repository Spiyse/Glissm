from __future__ import annotations

import discord
from discord.ext import commands

import config


def has_moderation_access(user: discord.abc.User) -> bool:
    if not isinstance(user, discord.Member):
        return False

    if user.guild_permissions.administrator:
        return True

    if config.MOD_ROLE_IDS and any(role.id in config.MOD_ROLE_IDS for role in user.roles):
        return True

    if config.MOD_ROLE_NAMES and any(role.name.lower() in config.MOD_ROLE_NAMES for role in user.roles):
        return True

    return False


class ModerationCog(commands.Cog):
    """Shared moderation access checks for prefix and slash commands."""

    async def cog_check(self, ctx: commands.Context) -> bool:
        allowed = has_moderation_access(ctx.author)
        if not allowed:
            await ctx.send("You need a moderator role to use moderation commands.")
        return allowed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        allowed = has_moderation_access(interaction.user)
        if not allowed:
            message = "You need a moderator role to use moderation commands."
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        return allowed
