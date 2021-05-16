import asyncio
import discord
from discord import guild
from discord import colour
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

class cog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="mute",
        description="Mutes the selected user.",
        guild_ids=[716611500256657469], # For testing only.
        options=[
            create_option(
                name="user",
                description="The user to mute.",
                option_type=6,
                required=True
            ),
            create_option(
                name="reason",
                description="Reason for muted the person.",
                option_type=3,
                required=False
            )
        ])
    @commands.has_permissions(manage_roles=True)
    async def _mute(self, ctx: SlashContext, user, reason="No reason provided."):
        mutedRole = None
        for role in ctx.guild.roles:
            if role.name == "Muted":
                mutedRole = role
                break
        if not mutedRole: await ctx.send(embed=discord.Embed(title="Please make a muted role.")); return
        member = ctx.guild.get_member(user.id)
        if member:
            await member.add_roles(mutedRole, reason=f"Muted by {ctx.author} for reason: {reason}")
            await ctx.send(f"Muted {user.mention}", hidden=True)

    @cog_ext.cog_slash(
        name="unmute",
        description="Unmutes the selected user.",
        guild_ids=[716611500256657469], # For testing only.
        options=[
            create_option(
                name="user",
                description="The user to unmute.",
                option_type=6,
                required=True
            ),
            create_option(
                name="reason",
                description="Reason for unmuting the person.",
                option_type=3,
                required=False
            )
        ])
    @commands.has_permissions(manage_roles=True)
    async def _unmute(self, ctx: SlashContext, user, reason="No reason provided."):
        mutedRole = None
        for role in ctx.guild.roles:
            if role.name == "Muted":
                mutedRole = role
                break
        if not mutedRole: await ctx.send(embed=discord.Embed(title="Please make a muted role.")); return
        member = ctx.guild.get_member(user.id)
        if member:
            try:
                await member.remove_roles(mutedRole, reason=f"Unmuted by {ctx.author} for reason: {reason}")
            except: pass
            await ctx.send(f"Unmuted {user.mention}", hidden=True)

def setup(client):
    client.add_cog(cog(client))
