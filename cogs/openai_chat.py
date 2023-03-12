import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """You are a discord moderator with complete server access.
You know all about social media, gaming, movies and music.
You can provide advice on social media, gaming, movies, music and anything related to today's youth.
Please aim to be friendly, creative and helpful. in all of your responses.
Format any list on individual lines with a dash and a space in front of each item.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10


class OpenAIChat(commands.Cog):
    """AI based chat responses"""

    def __init__(self, client):
        self.client = client

    def get_response(self, instructions, chat_history, new_question):
        """Get a response from ChatCompletion

        Args:
            instructions: The instructions for the chat bot - this determines how it will behave
            chat_history: Chat chat_history
            new_question: The new question to ask the bot

        Returns:
            The response text
        """
        # build the messages
        messages = [
            {"role": "system", "content": instructions},
        ]
        # add the previous questions and answers
        for question, answer in chat_history[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})
        # add the new question
        messages.append({"role": "user", "content": new_question})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=1,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )
        return completion.choices[0].message.content

    def get_moderation(self, question):
        """
        Check the question is safe to ask the model

        Parameters:
            question (str): The question to check

        Returns a list of errors if the question is not safe, otherwise returns None
        """

        errors = {
            "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
            "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
            "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
            "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
            "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
            "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
            "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
        }
        response = openai.Moderation.create(input=question)
        if response.results[0].flagged:
            # get the categories that are flagged and generate a message
            result = [
                error
                for category, error in errors.items()
                if response.results[0].categories[category]
            ]
            return result
        return None

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded OpenAI chat reponses")

    @commands.Cog.listener()
    async def on_message(self, message):
        chat_history = []
        mention = f"<@{self.client.user.id}>"

        if not mention in message.content:
            return

        new_question = message.content.replace(mention, "").strip()

        errors = self.get_moderation(new_question)
        if errors:
            await message.channel.send("The question did not pass the moderation test.")
            for error in errors:
                print(error)
            return
        response = self.get_response(
            INSTRUCTIONS, chat_history, new_question
        )

        # add the new question and answer to the list of previous questions and answers
        chat_history.append((new_question, response))
        await message.channel.send(response)
        return


def setup(client):
    client.add_cog(OpenAIChat(client))
