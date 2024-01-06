import discord
from discord.ext import commands, tasks
import time

import bot_remake_discord, bot_remake_scrap, bot_remake_scrap_frontpage, config # import the other scripts

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default()) # setup the bot

repeat_scraping = False # flag to check if the bot is running the scraping

@bot.event
async def on_ready():
    channel = bot.get_channel(config.CHANNEL_ID)
    print("Bot is ready")
    await bot_remake_discord.send_message("Bot is ready", channel)

@tasks.loop(seconds=30)
async def normal_scraping_task(channel):
    await bot_remake_scrap.started_scraping(channel)

@tasks.loop(seconds=30)
async def front_page_scraping_task(channel):
    await bot_remake_scrap_frontpage.started_scraping(channel)

@bot.command()
async def normal_scraping(ctx):
    global repeat_scraping
    repeat_scraping = True
    channel = bot.get_channel(config.CHANNEL_ID)
    normal_scraping_task.start(channel)

@bot.command()
async def front_page_scraping(ctx):
    global repeat_scraping
    repeat_scraping = True
    channel = bot.get_channel(config.CHANNEL_ID)
    front_page_scraping_task.start(channel)

@bot.command()
async def stop_scraping(ctx):
    global repeat_scraping
    repeat_scraping = False
    normal_scraping_task.stop()
    front_page_scraping_task.stop()
    channel = bot.get_channel(config.CHANNEL_ID)
    await bot_remake_discord.send_message("Scraping stopped", channel)

bot.run(config.BOT_TOKEN)
