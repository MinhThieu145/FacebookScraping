import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import requests

# secret token
BOT_TOKEN = 'MTA5OTM0MTMyMDg0MzE3NDA4OA.G8uu-z.Orwh7Dk1lDnOgdmsyQcy4Ykl3hisq2JEldFww4'
GUILD_ID = 1083640013180387349

# innitialize the bot
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix= commands.when_mentioned ,intents= discord.Intents.default())
        self.cog_list = ['cogs.PingCommand', 'cogs.ReactionCommand', 'cogs.SetURLCommand', 'cogs.CreateNewUser']

    async def setup_hook(self):
        for ext in self.cog_list:
            await self.load_extension(ext)

    async def on_ready(self):
        synced = await self.tree.sync()
        


# set up client and command tree
client = Client()

# run the bots
client.run(BOT_TOKEN)
