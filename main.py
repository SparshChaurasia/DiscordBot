"""
Discord Bot
~~~~~~~~~~~

A general-purpose discord bot.

"""

__title__ = "Discord Bot"
__author__ = "Sparsh#0483"
__version__ = "1.0.1"

import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TOKEN")

COMMAND_PREFIX = ">"
# STATUS = cycle(["Help Command", "Playing Music", "Managing Channels"])

client = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    help_command=commands.MinimalHelpCommand(),
    status=discord.Status.idle,
)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # update_status.start()
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"Listening to {COMMAND_PREFIX}help"),
    )
    return


# @client.event
# async def on_guild_join(ctx):
#     pass


@client.event
async def on_message(message):
    mention = f"<@!{client.user.id}>"
    if mention in message.content:
        await message.channel.send(
            f"Hi, this is {client.user}\n"
            f"A general purpose discord bot made by {__author__}\n"
            f"My prefix is '{COMMAND_PREFIX}'"
        )
        return
    else:
        await client.process_commands(message)


# Error handlers
@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(
            "Please pass all arguments\nUse {COMMAMD_PREFIX}help [command] for more help."
        )
        return
    # elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
    #     await ctx.send("No such command")
    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send("Requires additional permissions.")
        return
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("No such member.")
        return
    # else:
    #     await ctx.send("Something went wrong!")
    #     return


# Updates status
# @tasks.loop(seconds=10)
# async def update_status():
#     await client.change_presence(activity=discord.Game(STATUS.__next__()))


# Load cog
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


@client.command()
async def bot(ctx):
    """Info about the bot"""

    await ctx.send(
        f"Username: {client.user}\n"
        f"Roles: {', '.join([role.name for role in ctx.guild.get_member(client.user.id).roles if role != ctx.guild.default_role])}\n"
        f"Author: {__author__}\n"
        f"Version: {__version__}\n"
        f"Use {COMMAND_PREFIX}help to get a list of commands"
    )
    return


@client.command()
async def ping(ctx):
    """Shows bot latency"""

    await ctx.send(f"{round(client.latency * 1000)}ms")
    return


client.run(TOKEN)
