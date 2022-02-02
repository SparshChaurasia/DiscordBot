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
            await ctx.reply(
                f"Username: {ctx.message.author.mention}\n"
                f"ID: {ctx.message.author.id}\n"
                f"Joined: {ctx.message.author.joined_at}\n"
                f"Roles: {', '.join([role.name for role in ctx.message.author.roles if role != ctx.guild.default_role])}"
            )
            return
        else:
            await ctx.reply(
                f"Username: {member.mention}\n"
                f"ID: {member.id}\n"
                f"Joined: {member.joined_at}\n"
                f"Roles: {', '.join([role.name for role in member.roles if role != ctx.guild.default_role])}"
            )

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
            await ctx.send(rules)
            return

    @commands.command()
    async def decide(self, ctx):
        """Returns yes or no"""

        replies = {
            "affirmative": [
                "This is acceptable",
                "I'll allow it",
                "Imagine doing that unironically",
                "The council has decided, this is ok",
                "This shouldn't interest me, but it does",
            ],
            "negative": [
                "Unacceptable condition",
                "What about no?",
                "No because no",
                "I like saying no",
                "Just no, please, don't",
            ],
        }

        choice = replies[random.choice(["affirmative", "negative"])]
        await ctx.send(choice[random.randint(0, len(choice)) - 1])
        return


def setup(client):
    client.add_cog(PublicFunctions(client))
