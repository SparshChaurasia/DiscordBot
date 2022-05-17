import discord
from discord.ext import commands
from googlesearch import search
# import wikipedia
import wikipediaapi

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
                title=f"Info", 
                color=0x1167B1
            )
            message.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            message.add_field(name="Id", value=f"{ctx.message.author.id}", inline=False)
            message.add_field(name="Joined", value=f"{ctx.message.author.joined_at}", inline=False)
            message.add_field(
                name="Roles", 
                value=f"{', '.join([role.name for role in ctx.message.author.roles])}", 
                inline=False
            )
        else:
            message = discord.Embed(
                title=f"Info", 
                color=0x1167B1
            )
            message.set_author(name=member.name, icon_url=member.avatar_url)
            message.add_field(name="Id", value=f"{member.id}", inline=False)
            message.add_field(name="Joined", value=f"{member.joined_at}", inline=False)
            message.add_field(
                name="Roles", 
                value=f"{', '.join([role.name for role in member.roles])}", 
                inline=False
            )
       
        await ctx.send(embed=message)
        return

    @commands.command()
    async def search(self, ctx, search_engine, *, query):
        """Search the web for given term; <search engine (w/g)> <search term>"""

        if search_engine == "w":
            wiki_wiki = wikipediaapi.Wikipedia(
                language='en',
                extract_format=wikipediaapi.ExtractFormat.WIKI
            )

            p_wiki = wiki_wiki.page(query)

            if not p_wiki.exists():
                print("page does not exist")
                message = discord.Embed(
                    title=f"No results - {query}", 
                    description=f"No matching pages for {query} have been found\n"
                                 " - Try using common words or phrases\n"
                                 " - Use important words only\n"
                                 " - Avoid any typos",
                    color=0xFF0000
                )
                await ctx.send(embed=message)
                return

            message = discord.Embed(
                title=f"Search results - {query}",
                url=p_wiki.fullurl,
                description=". ".join(p_wiki.summary.split(". ")[0:3]),
                color=0x1167B1   
            )
            for section in p_wiki.sections:
                if section.text:
                    message.add_field(name=section.title, value=section.text.split(". ")[0])
                message

            await ctx.send(embed=message)
            return

        elif search_engine == "g":
            result = search(query, lang="en", num=5, start=0, stop=6)

            search_link = query.replace(" ", "+")
            message = discord.Embed(
                title=f"Search results - {query}",
                url=f"https://google.com/search?q={search_link}",
                description="\n".join(result),
                color=0x1167B1
            )   

            await ctx.reply(embed=message)
            return

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
