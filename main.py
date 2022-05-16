"""
Discord Bot
~~~~~~~~~~~

A general-purpose discord bot.

"""

__title__ = "Discord Bot"
__author__ = "Sparsh#0483"

import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
# from itertools import cycle


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
    mention = str(client.user.id)
    if mention in message.content:
        await message.channel.send(
            f"Hi, this is {client.user.name}\n"
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
            f"Please pass all arguments\nUse {COMMAND_PREFIX}help [command] for more help."
        )
        return
    # elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
    #     await ctx.send("No such command")
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
    
    message = discord.Embed(
        title=f"Info - {client.user.name}", 
        description=f"Use {COMMAND_PREFIX}help to get a list of commands", 
        color=0x1167B1
    )
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
