import discord
from discord.ext import commands
from googlesearch import search
import wikipedia

import random


class PublicFunctions(commands.Cog):
    """Provides basic functionality; accsessible by anyone on the server"""

    def __init__(self, client):
        self.client = client

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Public functions")

    # Commands
    @commands.command()
    async def info(self, ctx, member: commands.MemberConverter = None):
        """Gives user info"""
        if member is None:
            message = discord.Embed(
                title=f"Info - {ctx.message.author.name}", 
                description=f"This is the info of {ctx.message.author.name}", 
                color=0x1167B1
            )
            message.add_field(name="Id", value=f"{ctx.message.author.id}", inline=False)
            message.add_field(name="Joined", value=f"{ctx.message.author.joined_at}")
            message.add_field(
                name="Roles", 
                value=f"{', '.join([role.name for role in ctx.message.author.roles])}", 
                inline=False
            )
        else:
            message = discord.Embed(
                title=f"Info - {member.name}", 
                description=f"This is the info of {member.name}",
                color=0x1167B1
            )
            message.add_field(
                name="Id", value=f"{member.id}", inline=False)
            message.add_field(
                name="Joined", value=f"{member.joined_at}", inline=False)
            message.add_field(
                name="Roles", 
                value=f"{', '.join([role.name for role in member.roles])}", 
                inline=False
            )
       
        await ctx.reply(embed=message)
        return

    @commands.command()
    async def search(self, ctx, search_engine, *, query):
        """Search the web for given term; <search engine (w/g)> <search term>"""

        if search_engine == "w":
            try:
                result = wikipedia.summary(query, sentences=3)
            except wikipedia.exceptions.PageError:
                result = f'No results for "{query}". Try searching for another keyword!'
            except wikipedia.exceptions.DisambiguationError:
                result = f'No explict matches for "{query}". Try using words with clearer insight.'
            finally:
                await ctx.reply(f"{result}")
                return
        elif search_engine == "g":
            result = search(query, tld="com", lang="en",
                            num=1, start=0, stop=None)
            await ctx.reply(f"{result.__next__()}")

    @commands.command()
    async def rules(self, ctx):
        """Shows rules of the server"""
        rules = ""
        with open(r"resources\rules.txt", "r") as file:
            for line in file:
                if line.startswith("#"):
                    continue
                rules = rules + f"\n{line}"
        
        message = discord.Embed(
            title=f"Rules - {ctx.guild.name}", 
            description="These are the rules set by the owner of the server", 
            color=0x1167B1
        )
        message.add_field(name="Rules", value=rules)
        
        await ctx.send(embed=message)
        return

    @commands.command()
    async def decide(self, ctx):
        """Returns yes or no"""

        with open(r"resources\replies.txt", "r") as f:
            reply = random.choice(f.readlines())

            await ctx.send(reply)
            return


def setup(client):
    client.add_cog(PublicFunctions(client))
