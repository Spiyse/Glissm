async def setup_hook(self):
    await self.load_extension("cogs.general.ping")
    await self.load_extension("cogs.general.hello")
    await self.load_extension("cogs.general.modaltest")
    await self.load_extension("cogs.general.test")