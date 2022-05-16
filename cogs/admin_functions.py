import discord
from discord.ext import commands

import asyncio

ADMIN_ROLE_1 = "Owner"
ADMIN_ROLE_2 = "Co owner"


class AdminFunctions(commands.Cog):
    """Provides admin functionality; require specific permission or role"""

    def __init__(self, client):
        self.client = client

    # Event(s)
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Admin functions")
        return

    # Command(s)
    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def kick(
        self, ctx, member: commands.MemberConverter, *, reason="Not mentioned"
    ):
        """Kick a member; <member> [reason]"""

        await member.kick(reason=reason)

        message = discord.Embed(
            title=f"Kick - {member.name}",
            description=f"{member.name} was kicked by {ctx.message.author.name}", 
            color=0xFFA500
        )
        message.add_field(name="Reason", value=reason)
        
        await ctx.send(embed=message)
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def ban(
        self, ctx, member: commands.MemberConverter, *, reason="Not mentioned"
    ):
        """Ban a member; <member> [reason]"""

        await member.ban(reason=reason)

        message = discord.Embed(
            title=f"Ban - {member.name}",
            description=f"{member.name} was banned by {ctx.message.author.name}",
            color=0xFF0000
        )
        message.add_field(name="Reason", value=reason)

        await ctx.send(embed=message)
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def unban(self, ctx, *, member):
        """Unban a member; <member>"""

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                message = discord.Embed(
                    title=f"Unbanned - {member_name}", 
                    description=f"{member_name} was unbanned by {ctx.message.author.name}", 
                    color=0x00FF00
                )

                await ctx.send(embed=message)
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def tempban(
        self, ctx, member: commands.MemberConverter, duration, *, reason="Not mentioned"
    ):
        """Ban a member temporarily; <member> <duration; eg- 1m, 1h, 1d> [reason]"""

        amount = duration[:-1]
        unit = duration[-1]

        multiplier = {"m": 60, "h": 3600, "d": 216000}
        units = {"m": "minute(s)", "h": "hour(s)", "d": "day(s)"}

        await member.ban(reason=reason)

        message = discord.Embed(
            title=f"Ban - {member.name}",
            description=f"{member.name} was banned by {ctx.message.author.name}",
            color=0xFFFF00
        )
        message.add_field(name="Reason", value=reason)
        message.add_field(name="Duration", value=f"{amount} {units[unit]}")

        await ctx.send(embed=message)

        await asyncio.sleep(int(amount) * multiplier[unit])

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.name, member.discriminator

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                message = discord.Embed(
                    title=f"Unbanned - {member.name}",
                    description=f"Ban duration for {member.name} is over",
                    color=0x00FF00
                )
                
                await ctx.send(embed=message)

        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def clear(self, ctx, n=10):
        """Clear messages; [number of messages; default = 10]"""

        await ctx.channel.purge(limit=n + 1)  # Including the clear command also
        
        message = discord.Embed(
            title=f"Removed messages - {n}", 
            description=f"The messages were removed by {ctx.message.author.name}", 
            color=0x606060
        )
        
        await ctx.send(embed=message)
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def mute(self, ctx, member: commands.MemberConverter, duration="5m", reason="Not mentioned"):
        """Mute a member in voice channel; <member> [duration]"""

        amount = duration[:-1]
        unit = duration[-1]

        multiplier = {"m": 60, "h": 3600, "d": 216000}
        units = {"m": "minute(s)", "h": "hour(s)", "d": "day(s)"}

        await member.edit(mute=True)
        
        message = discord.Embed(
            title=f"Mute - {member.name}",
            description=f"{member.name} was muted by {ctx.message.author.name}",
            color=0xFFA500
        )
        message.add_field(name="Reason", value=reason)
        message.add_field(name="Duration", value=f"{amount} {units[unit]}")
        
        await ctx.send(embed=message)

        await asyncio.sleep(int(amount) * multiplier[unit])
        await member.edit(mute=False)

        message = discord.Embed(
            title=f"Unmuted - {member.name}",
            description=f"Mute duration for {member.name} is over",
            color=0x00FF00
        )

        await ctx.send(embed=message)
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def unmute(self, ctx, member: commands.MemberConverter):
        # await member.edit(mute=False)

        message = discord.Embed(
            title=f"Unmuted - {member.name}",
            description=f"{member.name} was unmuted by {ctx.message.author.name}",
            color=0x00FF00
        )

        await ctx.send(embed=message)
        return


def setup(client):
    client.add_cog(AdminFunctions(client))
