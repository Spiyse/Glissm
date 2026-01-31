from discord.ext import commands
import discord

class ChangeActivityCommand(commands.Cog):
    @commands.command(name="change_activity", aliases=["ca"])
    async def change_activity(self, ctx: commands.Context, activity_type: str = None, *, activity_text: str = None) -> None:
        
        if activity_type is None:
            current_activity = self.bot.activity
            if current_activity:
                await ctx.send(f"Current activity: **{current_activity.name}**")
            else:
                await ctx.send("No activity is currently set :p")
            return
        
        type_map = {
            'game': discord.ActivityType.playing,
            'streaming': discord.ActivityType.streaming,
            'listening': discord.ActivityType.listening,
            'watching': discord.ActivityType.watching,
        }
        
        if activity_type.lower() in type_map:
            if activity_text is None or activity_text.strip() == '':
                await ctx.send("Please provide activity text gang >ca <type> <text>")
                return
            try:
                await self.bot.change_presence(activity=discord.Activity(type=type_map[activity_type.lower()], name=activity_text))
                await ctx.send(f"Activity changed to: **{activity_text}** (type: {activity_type})")
            except Exception as e:
                await ctx.send("Failed to change activity :(")
        else:
            full_text = f"{activity_type} {activity_text}" if activity_text else activity_type
            try:
                await self.bot.change_presence(activity=discord.Game(name=full_text))
                await ctx.send(f"Activity changed to: **{full_text}**")
            except:
                await ctx.send("Failed to change activity :(")