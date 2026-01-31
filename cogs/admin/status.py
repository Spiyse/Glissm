from discord.ext import commands
import discord

class ChangeStatusCommand(commands.Cog):
    @commands.command(name="change_status", aliases=["cs"])
    async def change_status(self, ctx: commands.Context, *, status_text: str = None) -> None:
        
        if status_text is None or status_text.strip() == '':
            await ctx.send(f"Current status: **{self.bot.status}**")
            return
        
        status_text = status_text.lower().strip()
        status_map = {
            'online': discord.Status.online,
            'offline': discord.Status.offline,
            'idle': discord.Status.idle,
            'dnd': discord.Status.dnd,
        }
        
        if status_text not in status_map:
            await ctx.send(f"Invalid status")
            return
        try:
            await self.bot.change_presence(status=status_map[status_text])
            await ctx.send(f"Status changed to: **{status_text}**")
        except Exception as e:
            await ctx.send("Failed to change status")