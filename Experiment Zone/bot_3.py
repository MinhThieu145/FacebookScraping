from discord.ext import commands, tasks
import discord

BOT_TOKEN = "MTA4MzYzNzk2ODk1MjExNTI0MA.GJak7Z.2QARy9CVYlMRyJ-ysjLu8zofT3JujNY74WRufo"
CHANNEL_ID = 1083640013180387352

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


import random
import test_call_function


@bot.event
async def on_ready():
    print("Bot is ready")
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Bot is ready")

# generate 5 random hex code for color
def generate_random_color():
    return random.randint(0, 0xffffff)

@bot.command()
async def start(ctx):
    await ctx.send("Bot is started")
    
    # get info
    title, price, location, time, photo_link = await test_call_function.info(ctx)

    embeded = discord.Embed(title= title, color=generate_random_color())
    embeded.add_field(name="Price", value=price, inline=True)
    embeded.add_field(name="Location", value=location, inline=True)
    embeded.add_field(name="Time", value=time, inline=False)
    embeded.set_image(url=photo_link)
    await ctx.send(embed=embeded)


bot.run(BOT_TOKEN)