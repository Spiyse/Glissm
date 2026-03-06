from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

import discord
from discord import ui


@dataclass(slots=True)
class ModalConfig:
    title: str
    reason_label: str
    reason_default: str = "No reason provided"
    show_extra: bool = False
    extra_label: str = "Extra"
    extra_default: str = ""
    extra_max_length: int = 20

    
class MemberActionModal(ui.Modal):
    user_select = ui.Label(
        text="Select a member",
        component=ui.UserSelect(placeholder="Choose a member", min_values=1, max_values=1),
    )

    def __init__(
        self,
        *,
        config: ModalConfig,
        run_action: Callable[
            [discord.Interaction, discord.Member, str, str | None],
            Awaitable[str | discord.Embed],
        ],
        warnings: dict[str, list[str]] | None = None,
        warning_count: int = 0,
    ):
        super().__init__(title=config.title)
        self.run_action = run_action
        self.show_extra = config.show_extra
        self.warnings = warnings or {}
        self.warning_count = warning_count

        self.reason = ui.TextInput(
            label=config.reason_label,
            style=discord.TextStyle.paragraph,
            required=True,
            default=config.reason_default,
            max_length=500,
        )

        self.add_item(self.reason)

        if self.show_extra:
            self.extra = ui.TextInput(
                label=config.extra_label,
                required=False,
                default=config.extra_default,
                max_length=config.extra_max_length,
            )
            self.add_item(self.extra)

    async def on_submit(self, interaction: discord.Interaction):
        target: discord.Member = self.user_select.component.values[0]
        extra_value = self.extra.value if self.show_extra else None
        result = await self.run_action(interaction, target, self.reason.value, extra_value)

        if isinstance(result, discord.Embed):
            await interaction.response.send_message(embed=result, ephemeral=True)
            return

        await interaction.response.send_message(result, ephemeral=True)