from discord import app_commands
from discord.ext import commands
import discord

from .modals import MemberActionModal, ModalConfig


class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def can_target(actor: discord.Member, target: discord.Member) -> tuple[bool, str]:
        if actor.id == target.id:
            return False, "You cannot kick yourself."

        if target == actor.guild.owner:
            return False, "You cannot kick the server owner."

        if target.top_role >= actor.top_role and actor != actor.guild.owner:
            return False, "You cannot kick someone with an equal or higher role."

        return True, ""

    @staticmethod
    def bot_can_target(guild: discord.Guild, target: discord.Member) -> tuple[bool, str]:
        me = guild.me
        if me is None:
            return False, "Could not verify bot permissions."

        if not me.guild_permissions.kick_members:
            return False, "I need the Kick Members permission."

        if target.top_role >= me.top_role:
            return False, "That member's role is higher than mine."

        return True, ""

    async def run_kick(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str,
        extra: str | None = None,
    ) -> str:
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

        try:
            await guild.kick(
                target,
                reason=f"{reason} | Moderator: {actor} ({actor.id})",
            )
        except discord.Forbidden:
            return "I don't have permission to kick that member."

        return f"Kicked {target.mention}\nReason: {reason}"

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.guild_only()
    async def kick_slash(self, interaction: discord.Interaction):
        cfg = ModalConfig(
            title="Kick Member",
            show_extra=False,
            reason_label="Reason",
        )
        await interaction.response.send_modal(MemberActionModal(config=cfg, run_action=self.run_kick))


async def setup(bot: commands.Bot):
    await bot.add_cog(KickCommand(bot))
