from discord import app_commands
from discord.ext import commands
import discord

from .modals import MemberActionModal, ModalConfig


class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def run_ban(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str,
        extra: str | None,  # delete days
    ) -> str:
        guild = interaction.guild
        actor = interaction.user
        if guild is None or not isinstance(actor, discord.Member):
            return "This command can only be used in a server."

        delete_days = int((extra or "0").strip())
        if not 0 <= delete_days <= 7:
            return "Delete message days must be between 0 and 7."

        await guild.ban(
            target,
            reason=f"{reason} | Moderator: {actor} ({actor.id})",
            delete_message_seconds=delete_days * 86400,
        )
        return f"Banned {target.mention}\nReason: {reason}"

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.guild_only()
    async def ban_slash(self, interaction: discord.Interaction):
        cfg = ModalConfig(
            title="Ban Member",
            reason_label="Reason",
            show_extra=True,
            extra_label="Delete message days (0-7)",
            extra_default="0",
            extra_max_length=1,
        )
        await interaction.response.send_modal(MemberActionModal(config=cfg, run_action=self.run_ban))


async def setup(bot: commands.Bot):
    await bot.add_cog(BanCommand(bot))
