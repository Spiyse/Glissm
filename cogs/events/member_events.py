import discord
import config
import random

from discord.ext import commands
from logger import logger

class MemberEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def create_leave_embed(self, member: discord.Member, reason: str = "Left", color: discord.Color = None, moderator: discord.User = None, reason_text: str = None):
        
        goodbye_messages = [f"Goodbye {member.mention}!", f"Byee {member.mention}!", f"Cya {member.mention}!"]
        
        if color is None:
            color = discord.Color.red()
        
        embed = discord.Embed(
            title=f"Member {reason}",
            description=random.choice(goodbye_messages),
            color=color,
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=False)
        
        if moderator:
            embed.add_field(name="Moderator", value=moderator.mention, inline=True)
            
        if reason_text:
            embed.add_field(name="Reason", value=reason_text or "No reason provided", inline=False)
            
        embed.add_field(name="Joined", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)

        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)
        
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.info(f"Member joined: {member} (ID: {member.id}) - Guild: {member.guild}")
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)
        
        greeting_messages = [f"Hello {member.mention}!", f"Welcome {member.mention}!", f"Hii {member.mention}!"]
        
        if not channel:
            logger.warning(f"Join channel not found (ID: {config.LOG_CHANNEL_ID})")
            return
        
        embed = discord.Embed(
            title="Member Joined",
            description=random.choice(greeting_messages),
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=False)
        embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)

        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)

        await channel.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        logger.info(f"Member left: {member} (ID: {member.id}) - Guild: {member.guild}")
        channel = self.bot.get_channel(config.LEAVE_CHANNEL_ID)
        
        reason = "Left"
        color = discord.Color.red()
        moderator = None
        reason_text = None
        
        try:
            async for entry in member.guild.audit_logs(limit=5):
                if entry.target.id == member.id:
                    if entry.action == discord.AuditLogAction.kick:
                        reason = "Kicked"
                        color = discord.Color.orange()
                        moderator = entry.user
                        reason_text = entry.reason
                        break
                    elif entry.action == discord.AuditLogAction.ban:
                        reason = "Banned"
                        color = discord.Color.dark_red()
                        moderator = entry.user
                        reason_text = entry.reason
                        break
        except discord.Forbidden:
            logger.warning("No permission to read audit log")
        
        if not channel:
            logger.warning(f"Leave channel not found (ID: {config.LEAVE_CHANNEL_ID})")
            return
        
        embed = self.create_leave_embed(member, reason, color, moderator, reason_text)
        
        await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEvents(bot))
