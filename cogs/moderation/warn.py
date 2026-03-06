import discord
import asyncio
from datetime import timedelta
from discord import app_commands
from discord.ext import commands

import config

from database import supabase

from .modals import MemberActionModal, ModalConfig



class WarnCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _add_warn(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str
    ) -> int:

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(
            None,
            lambda: supabase.table("member_warnings").insert({
                "guild_id": guild_id,
                "user_id": user_id,
                "moderator_id": moderator_id,
                "reason": reason,
            }).execute()
        )

        response = await loop.run_in_executor(
            None,
            lambda: supabase.table("member_warnings")
                .select("id", count="exact")
                .eq("guild_id", guild_id)
                .eq("user_id", user_id)
                .execute()
        )

        return response.count

    @staticmethod
    def can_target(actor: discord.Member, target: discord.Member) -> tuple[bool, str]:

        if actor.id == target.id:
            return False, "You cannot warn yourself."

        if target == actor.guild.owner:
            return False, "You cannot warn the server owner."

        if target.top_role >= actor.top_role and actor != actor.guild.owner:
            return False, "You cannot warn someone with an equal or higher role."

        return True, ""

    @staticmethod
    def bot_can_target(guild: discord.Guild, target: discord.Member) -> tuple[bool, str]:

        me = guild.me

        if me is None:
            return False, "Could not verify bot permissions."

        if not me.guild_permissions.moderate_members:
            return False, "I need the Moderate Members permission."

        if target.top_role >= me.top_role:
            return False, "That member's role is higher than mine."

        return True, ""

    async def run_warn(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str,
        extra: str | None = None,
    ) -> str | discord.Embed:

        guild = interaction.guild
        actor = interaction.user

        if guild is None or not isinstance(actor, discord.Member):
            return "This command can only be used in a server."

        ok, message = self.can_target(actor, target)
        if not ok:
            return message

        ok, message = self.bot_can_target(guild, target)
        if not ok:
            return message

        warnings_count = await self._add_warn(
            guild_id=guild.id,
            user_id=target.id,
            moderator_id=actor.id,
            reason=reason
        )

        me = guild.me
        auto_action = "None"
        action_note = "Threshold not reached."
        
        AUTO_TIMEOUT_HOURS = config.AUTO_TIMEOUT_HOURS
        AUTO_TIMWOUT_WARNING_AMOUNT = config.AUTO_TIMWOUT_WARNING_AMOUNT
        AUTO_KICK_WARNING_AMOUNT = config.AUTO_KICK_WARNING_AMOUNT
        AUTO_BAN_WARNING_AMOUNT = config.AUTO_BAN_WARNING_AMOUNT
        
        if me is None:
            action_note = "Could not verify bot permissions for auto moderation."
        elif warnings_count >= AUTO_BAN_WARNING_AMOUNT:
            if not me.guild_permissions.ban_members:
                action_note = f"Reached {AUTO_BAN_WARNING_AMOUNT} warnings, but I need the Ban Members permission."
            elif target.top_role >= me.top_role:
                action_note = f"Reached {AUTO_BAN_WARNING_AMOUNT} warnings, but that member's role is higher than mine."
            else:
                try:
                    await guild.ban(
                        target,
                        reason=(
                            f"Auto-ban at {AUTO_BAN_WARNING_AMOUNT} warnings | Last reason: {reason} "
                            f"| Moderator: {actor} ({actor.id})"
                        ),
                        delete_message_seconds=0,
                    )
                    auto_action = "Ban"
                    action_note = f"Applied automatic ban at {AUTO_BAN_WARNING_AMOUNT} warnings."
                except discord.Forbidden:
                    action_note = f"Reached {AUTO_BAN_WARNING_AMOUNT} warnings, but I don't have permission to ban that member."
                    
        elif warnings_count >= AUTO_KICK_WARNING_AMOUNT:
            if not me.guild_permissions.kick_members:
                action_note = f"Reached {AUTO_KICK_WARNING_AMOUNT} warnings, but I need the Kick Members permission."
            elif target.top_role >= me.top_role:
                action_note = f"Reached {AUTO_KICK_WARNING_AMOUNT} warnings, but that member's role is higher than mine."
            else:
                try:
                    await guild.kick(
                        target,
                        reason=(
                            f"Auto-kick at {AUTO_KICK_WARNING_AMOUNT} warnings | Last reason: {reason} "
                            f"| Moderator: {actor} ({actor.id})"
                        ),
                    )
                    auto_action = "Kick"
                    action_note = f"Applied automatic kick at {AUTO_KICK_WARNING_AMOUNT} warnings."
                except discord.Forbidden:
                    action_note = f"Reached {AUTO_KICK_WARNING_AMOUNT} warnings, but I don't have permission to kick that member."
            
        elif warnings_count >= AUTO_TIMWOUT_WARNING_AMOUNT:
            if not me.guild_permissions.moderate_members:
                action_note = f"Reached {AUTO_TIMWOUT_WARNING_AMOUNT} warnings, but I need the Moderate Members permission."
            elif target.top_role >= me.top_role:
                action_note = f"Reached {AUTO_TIMWOUT_WARNING_AMOUNT} warnings, but that member's role is higher than mine."
            else:
                try:
                    await target.timeout(
                        timedelta(hours=AUTO_TIMEOUT_HOURS),
                        reason=(
                            f"Auto-timeout at {AUTO_TIMWOUT_WARNING_AMOUNT} warnings | Last reason: {reason} "
                            f"| Moderator: {actor} ({actor.id})"
                        ),
                    )
                    auto_action = f"Timeout ({AUTO_TIMEOUT_HOURS} H)"
                    action_note = f"Applied automatic {AUTO_TIMEOUT_HOURS} H timeout at {AUTO_TIMWOUT_WARNING_AMOUNT} warnings."
                except discord.Forbidden:
                    action_note = f"Reached {AUTO_TIMWOUT_WARNING_AMOUNT} warnings, but I don't have permission to timeout that member."        
            
        embed = discord.Embed(
            title="Member Warned",
            color=discord.Color.orange()
        )
        embed.add_field(name="Member", value=target.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Total warns", value=str(warnings_count), inline=True)
        embed.add_field(name="Auto action", value=auto_action, inline=True)
        embed.add_field(name="Action note", value=action_note, inline=False)

        return embed

    @app_commands.command(name="warn", description="Warn a member from the server.")
    @app_commands.guild_only()
    async def warn_slash(self, interaction: discord.Interaction):

        cfg = ModalConfig(
            title="Warn Member",
            reason_label="Reason",
        )

        await interaction.response.send_modal(
            MemberActionModal(config=cfg, run_action=self.run_warn)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(WarnCommand(bot))