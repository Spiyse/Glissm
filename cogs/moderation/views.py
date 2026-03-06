import discord
import asyncio
from discord import ui
from datetime import datetime

from database import supabase


class ConfirmUnwarnView(ui.View):

    def __init__(self, member: discord.Member, warning: dict):
        super().__init__(timeout=60)

        self.member = member
        self.warning = warning


    @ui.button(label="Confirm", style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):

        warning_id = self.warning["id"]

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(
            None,
            lambda: supabase.table("member_warnings")
                .delete()
                .eq("id", warning_id)
                .execute()
        )

        await interaction.response.edit_message(
            content="",
            embed= discord.Embed(
                title=f"Warning removed from {self.member.display_name}",
                color=discord.Color.green()
            ),
            view=None
        )


    @ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):

        await interaction.response.edit_message(
            content="Unwarn cancelled.",
            embed=None,
            view=None
        )


class WarningSelect(ui.Select):

    def __init__(self, member: discord.Member, warnings: list):

        options = []

        for warn in warnings:

            label = warn["reason"][:80]

            options.append(
                discord.SelectOption(
                    label=label,
                    value=str(warn["id"])
                )
            )

        super().__init__(
            placeholder="Select warning to remove",
            options=options,
            min_values=1,
            max_values=1
        )

        self.member = member
        self.warnings = warnings


    async def callback(self, interaction: discord.Interaction):

        warning_id = int(self.values[0])

        warning = next(w for w in self.warnings if w["id"] == warning_id)

        moderator_id = warning["moderator_id"]
        reason = warning["reason"]
        timestamp = warning["created_at"]

        date = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")

        embed = discord.Embed(
            title="⚠️ Confirm Warning Removal",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="User",
            value=self.member.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=f"<@{moderator_id}>",
            inline=True
        )

        embed.add_field(
            name="Date",
            value=date,
            inline=True
        )

        view = ConfirmUnwarnView(self.member, warning)

        await interaction.response.edit_message(
            embed=embed,
            view=view
        )


class WarningSelectView(ui.View):

    def __init__(self, member: discord.Member, warnings: list):
        super().__init__(timeout=60)

        self.add_item(WarningSelect(member, warnings))