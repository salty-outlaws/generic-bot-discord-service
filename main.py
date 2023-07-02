import os

import discord
from dotenv import load_dotenv
import requests

load_dotenv()
BOT_FRAMEWORK_URL = os.getenv('DISCORD_TOKEN')
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message: discord.Message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        response = requests.post(BOT_FRAMEWORK_URL, json={
            "username": str(message.author.id),
            "message": message.content.strip()
        })

        output = response.json()
        if (output["message"] != ""):
            await message.reply(output["message"], mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


client.run(TOKEN)