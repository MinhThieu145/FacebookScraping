# Try send message to discord server

import discord
from discord.ext import commands

BOT_TOKEN = 'MTA5OTM0MTMyMDg0MzE3NDA4OA.G8uu-z.Orwh7Dk1lDnOgdmsyQcy4Ykl3hisq2JEldFww4'
CHANNEL_ID = 1083640013180387352

client = commands.Bot(command_prefix='/', intents=discord.Intents.all())
# send msg to channel
async def send_msg(msg):
    channel = client.get_channel(CHANNEL_ID)

    await channel.send(msg)

# send mesage

@client.event
async def on_ready():
    await send_msg('Bot is ready')
# innit bot
client.run(BOT_TOKEN)   