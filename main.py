import os

import discord
from dotenv import load_dotenv
import requests

load_dotenv()
BOT_FRAMEWORK_URL = os.getenv('BOT_FRAMEWORK_URL')
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
            "message": message.content.strip(),
            "guild": str(message.guild.id)
        })
        
        output = response.json()

        try:
            if output["type"] == "embed":
                embedVar = discord.Embed(title=output["title"], description=output["summary"], color=0x00ff00)
                for k,v in output["fields"].items():
                    embedVar.add_field(name=k, value=v, inline=False)
                await message.reply(embed=embedVar)
            elif output["type"] == "image":
                await message.reply(output["image"])
            elif output["type"] == "text":
                await message.reply(output["message"], mention_author=True)
            elif output["type"] == "error":
                embedVar = discord.Embed(title="Error", description=output["error"], color=0xff0000)
                await message.reply(embed=embedVar)
            else:
                pass
        except e:
            print(response.text)
            raise e

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
