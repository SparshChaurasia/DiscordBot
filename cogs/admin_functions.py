import asyncio
from discord.ext import commands

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
        await ctx.send(f"Kicked {member.mention} for reason: {reason}")

        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def ban(
        self, ctx, member: commands.MemberConverter, *, reason="not mentioned"
    ):
        """Ban a member; <member> [reason]"""

        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for reason: {reason}")
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
                await ctx.send(f"Unbanned {user.mention}")
            return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def tempban(
        self, ctx, member: commands.MemberConverter, duration, *, reason="not mentioned"
    ):
        """Ban a member temporarily; <member> <duration; eg- 1m, 1h, 1d> [reason]"""

        amount = duration[:-1]
        unit = duration[-1]

        multiplier = {"m": 60, "h": 3600, "d": 216000}
        units = {"m": "minute(s)", "h": "hour(s)", "d": "day(s)"}

        await member.ban(reason=reason)
        await ctx.send(
            f"Banned {member.mention} for reason: {reason} "
            f"for: {amount} {units[unit]}"
        )

        await asyncio.sleep(int(amount) * multiplier[unit])

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.name, member.discriminator

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def clear(self, ctx, n=10):
        """Clear messages; [number of messages; default = 10]"""

        await ctx.channel.purge(limit=n + 1)
        await ctx.send(f"Cleared {n} messages")
        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def mute(self, ctx, member: commands.MemberConverter, duration="5m"):
        """Mute a member in voice channel; <member> [duration]"""

        amount = duration[:-1]
        unit = duration[-1]

        multiplier = {"m": 60, "h": 3600, "d": 216000}
        units = {"m": "minute(s)", "h": "hour(s)", "d": "day(s)"}

        await member.edit(mute=True)
        await ctx.send(f"Muted {member.mention} for: {amount} {units[unit]}")

        await asyncio.sleep(int(amount) * multiplier[unit])
        await member.edit(mute=False)

        return

    @commands.command()
    @commands.has_role(ADMIN_ROLE_1 or ADMIN_ROLE_2)
    async def unmute(self, ctx, member: commands.MemberConverter):
        await member.edit(mute=False)
        await ctx.send(f"Unmuted {member.mention}")
        return


def setup(client):
    client.add_cog(AdminFunctions(client))
