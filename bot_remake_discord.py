from discord.ext import commands, tasks
import discord

import config

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# send the message say the bot is ready
async def send_message(message,channel):
    await channel.send(message)

async def send_embeded(img_link,post_link, title, price, location,channel, post_time = None):
    
    # create the embeded message
    embeded = discord.Embed(title= title, url = post_link,color=config.generate_random_color())
    embeded.add_field(name="Price", value=price, inline=True)
    embeded.add_field(name="Location", value=location, inline=True)
    if post_time != None:
        embeded.add_field(name="Posted Time", value=post_time, inline=False)
    embeded.set_image(url=img_link)

    await channel.send(embed=embeded)







