import asyncio
import logging
import os

import discord
from discord.ext import commands

import config
from help_command import EmbedHelpCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("glissm")


async def load_cogs(bot: commands.Bot) -> None:
  # Load all cogs from config.COGS.
    for cog in config.COGS:
        try:
            await bot.load_extension(cog)
            logger.info("Loaded cog: %s", cog)
        except commands.ExtensionError as e:
            logger.error("Failed to load cog %s: %s", cog, e)


async def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=config.COMMAND_PREFIX,
        intents=intents,
        help_command=EmbedHelpCommand(),
    )

    @bot.event
    async def on_ready() -> None:
        logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id if bot.user else None)

    await load_cogs(bot)

    token = config.DISCORD_TOKEN or os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env or environment")

    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
