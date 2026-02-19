async def setup_hook(self):
    await self.load_extension("cogs.utility.uptime")
    await self.load_extension("cogs.utility.serverinfo")