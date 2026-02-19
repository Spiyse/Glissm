import asyncio
import logging
import os

import discord
from discord.ext import commands

import config
from cogs.discovery import discover_cogs
from help_command import HelpCommand
from logger import logger

logging.basicConfig(level=logging.INFO)

async def load_cogs(bot: commands.Bot) -> None:
    for cog in discover_cogs():
        try:
            if cog in bot.extensions:
                await bot.unload_extension(cog)
            await bot.load_extension(cog)
            logger.info("Loaded cog: %s", cog)
        except commands.ExtensionError as e:
            logger.error("Failed to load cog %s: %s", cog, e)


async def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(
        command_prefix=config.COMMAND_PREFIX,
        intents=intents,
        help_command=HelpCommand(),
    )
    bot.synced = False
    

    @bot.event
    async def on_ready() -> None:
        if not bot.synced:
            await bot.tree.sync()
            bot.synced = True
            logger.info("Synced application commands.")
        logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id if bot.user else None)

    await load_cogs(bot)

    token = config.DISCORD_TOKEN or os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env or environment")

    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
