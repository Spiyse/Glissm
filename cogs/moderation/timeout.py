from discord import app_commands
from discord.ext import commands
import discord
from datetime import timedelta

from .modals import MemberActionModal, ModalConfig


class TimeoutCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def can_target(actor: discord.Member, target: discord.Member) -> tuple[bool, str]:
        if actor.id == target.id:
            return False, "You cannot timeout yourself."

        if target == actor.guild.owner:
            return False, "You cannot timeout the server owner."

        if target.top_role >= actor.top_role and actor != actor.guild.owner:
            return False, "You cannot timeout someone with an equal or higher role."

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

    @staticmethod
    def parse_duration(value: str | None) -> timedelta | None:
        raw = (value or "").strip().lower()
        if not raw:
            return None

        unit = raw[-1]
        amount_str = raw[:-1]
        if unit not in {"m", "h", "d"} or not amount_str.isdigit():
            return None

        amount = int(amount_str)
        if amount <= 0:
            return None

        if unit == "m":
            return timedelta(minutes=amount)
        if unit == "h":
            return timedelta(hours=amount)
        return timedelta(days=amount)

    async def run_timeout(
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

        duration = self.parse_duration(extra)
        if duration is None:
            return "Invalid duration. Use formats like 30m, 2h, or 1d."

        if duration > timedelta(days=28):
            return "Timeout cannot be longer than 28 days."

        try:
            await target.timeout(
                duration,
                reason=f"{reason} | Moderator: {actor} ({actor.id})",
            )
        except discord.Forbidden:
            return "I don't have permission to timeout that member."

        return f"Timed out {target.mention} for {extra}\nReason: {reason}"

    @app_commands.command(name="timeout", description="Timeout a member in the server.")
    @app_commands.guild_only()
    async def timeout_slash(self, interaction: discord.Interaction):
        cfg = ModalConfig(
            title="Timeout Member",
            show_extra=True,
            reason_label="Reason",
            extra_label="Duration (30m, 2h, 1d, etc.)",
            extra_default="30m",
            extra_max_length=5,
            
        )
        await interaction.response.send_modal(MemberActionModal(config=cfg, run_action=self.run_timeout))


async def setup(bot: commands.Bot):
    await bot.add_cog(TimeoutCommand(bot))
