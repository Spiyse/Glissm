import discord
from discord.ext import commands

# The help command is outside the cogs cuz it is it's own thing

class HelpCommand(commands.HelpCommand):
    def get_command_signature(self, command: commands.Command) -> str:

        parent = command.full_parent_name
        alias = command.name if not parent else f"{parent} {command.name}"
        return f"{self.context.clean_prefix}{alias} {command.signature}"


    # made this cuz i didn't like that under each def i had to put this big embed footer chunk of code ;-;
    async def send_embed(self, embed: discord.Embed) -> None:
        embed.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.display_avatar.url)
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping: dict) -> None:
        # list all cogs and commands
        embed = discord.Embed(
            title="Command list",
            description=f"Use `{self.context.clean_prefix}help <command>` for details.",
            color=discord.Color.from_str("#272b3f"),
            timestamp=discord.utils.utcnow(),
        )
        for cog, command_list in mapping.items():
            filtered = await self.filter_commands(command_list, sort=True)
            if not filtered:
                continue
            name = cog.qualified_name if cog else "No category"
            value = " ".join(f"`{c.name}`" for c in filtered)
            embed.add_field(name=name, value=value, inline=False)
        await self.send_embed(embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        # list commands in a cog >help <cog>
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if not filtered:
            await self.send_error_message("No commands in this category are visible to you.")
            return
        embed = discord.Embed(
            title=cog.qualified_name,
            description=cog.description or "No description.",
            color=discord.Color.from_str("#795f9a"),
            timestamp=discord.utils.utcnow(),
        )
        for command in filtered:
            sig = self.get_command_signature(command)
            help_brief = (command.short_doc or "No description.").split("\n")[0]
            embed.add_field(name=sig, value=help_brief, inline=False)
        await self.send_embed(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        # details for one command >help <command>
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.help or "No description.",
            color=discord.Color.from_str("#5f9a93"),
            timestamp=discord.utils.utcnow(),
        )
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{a}`" for a in command.aliases), inline=False)
        if command.clean_params:
            embed.add_field(name="Parameters", value="\n".join(f"`{name}`" for name in command.clean_params), inline=False)
        await self.send_embed(embed)

    async def send_group_help(self, group: commands.Group) -> None:
        # list subcommands >help <group>
        filtered = await self.filter_commands(group.commands, sort=True)
        embed = discord.Embed(
            title=self.get_command_signature(group),
            description=group.help or "No description.",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )
        for command in filtered:
            sig = self.get_command_signature(command)
            help_brief = (command.short_doc or "No description.").split("\n")[0]
            embed.add_field(name=sig, value=help_brief, inline=False)
        embed.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.display_avatar.url)
        await self.send_embed(embed)
        
    async def send_error_message(self, error: str) -> None:
        # Send help errors as an embed
        embed = discord.Embed(
            title="Help",
            description=error,
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        await self.context.send(embed=embed)
