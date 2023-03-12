"""
Discord Bot
~~~~~~~~~~~

A general-purpose discord bot.

"""

__title__ = "Discord Bot"
__author__ = "Sparsh#0483"

import os
from dotenv import load_dotenv

import discord
from discord import Guild
from discord.ext import commands, tasks

# from itertools import cycle


load_dotenv()
TOKEN = os.getenv("TOKEN")  # Discord bot token

COMMAND_PREFIX = ">"
# STATUS = cycle(["Help Command", "Playing Music", "Managing Channels"])

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    help_command=commands.MinimalHelpCommand(),
    status=discord.Status.idle,
    intents=intents
)

# -------------- Events --------------


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # update_status.start()
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"Listening to {COMMAND_PREFIX}help"),
    )
    return


@client.event
async def on_guild_join(guild):
    await guild.owner.send(
        "Hello! Thanks for inviting me to your server.\n"
        f"This is {client.user.name}, a open-source general-purpose discord bot built with discordpy api wrapper in python.\n\n"
        "Contribute here: https://github.com/SparshChaurasia/DiscordBot"
    )

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            message = discord.Embed(
                title=f"Hi, this is {client.user.name}",
                description=f"My prefix is '{COMMAND_PREFIX}'\nUse {COMMAND_PREFIX}help to get started",
                color=0x1167B1
            )
            await channel.send(embed=message)
            break


@client.event
async def on_member_join(member):
    rules = ""
    with open(r"resources\rules.txt", "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            rules = rules + f"\n{line}"

    message = discord.Embed(
        title=f"Hi, this is {client.user.name}",
        description=f"My command prefix in this server is '{COMMAND_PREFIX}'",
        color=0x1167B1
    )
    message.add_field(name="Rules for this server", value=rules)

    await member.send(embed=message)


# -------------- Error handlers ------------------


@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(
            f"Please pass all arguments\nUse {COMMAND_PREFIX}help [command] for more help."
        )
        return
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("No such command")
    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send("Missing required role.")
        return
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("No such member.")
        return
    else:
        await ctx.send("Something went wrong!")
        return


# Updates status
# @tasks.loop(seconds=10)
# async def update_status():
#     await client.change_presence(activity=discord.Game(STATUS.__next__()))


# -------------- Load/Unload Cogs ------------------


@client.command()
@commands.has_role("Bot support")
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")
    return


# Unload cog
@client.command()
@commands.has_role("Bot support")
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Done")
    return


# Reload cog
@client.command()
@commands.has_role("Bot support")
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")
    return


# Load all cogs at startup
for filename in os.listdir(r"./cogs/"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# -------------- Miscellaneous Commands ------------------


@client.command()
async def bot(ctx):
    """Info about the bot"""

    message = discord.Embed(
        title=f"Info",
        description=f"Use {COMMAND_PREFIX}help to get a list of commands",
        color=0x1167B1
    )
    message.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    message.add_field(name="Id", value=client.user.id, inline=False)
    # message.add_field(name="Joined", value=client.user.joined_at, inline=False)
    message.add_field(
        name="Roles", value=f"{', '.join([role.name for role in ctx.guild.get_member(client.user.id).roles if role != ctx.guild.default_role])}", inline=False)
    message.add_field(name="Author", value=f"{__author__}", inline=False)

    await ctx.send(embed=message)
    return


@client.command()
async def ping(ctx):
    """Shows bot latency"""

    latency = round(client.latency * 1000)  # Since latency given is in seconds

    message = discord.Embed(color=0x606060)
    message.add_field(name="Latency", value=f"{latency}ms")

    await ctx.send(embed=message)
    return


client.run(TOKEN)
