from discord.ext import commands, tasks
import discord

import old_scraper

BOT_TOKEN = "MTA4MzYzNzk2ODk1MjExNTI0MA.GDtgAP.GAjNSRHgXBC5yYZcJzQnPhaITzPmlUHk-9q8RE"
CHANNEL_ID = 1083640013180387352
CHECK_INTERVAL = 30  # in seconds

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot is ready")
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Bot is ready")
    # send intruction to use the bot
    await channel.send(
        "Use !start to start the check loop and !stop to stop the check loop. Bot will run the check loop every 5 seconds."
    )


# Markdown format before sending
def format_data_to_markdown(data):
    title = data['title']
    time = data['time']
    location = data['location']
    photo_link = data['photo_link']
    post_link = data['post_link']

    markdown = f"""
- Title: {title}
- Price: {time}
- Location: {location}
- Photo: {photo_link}
- Post link: {post_link}
"""
    return markdown



# Define a background task that periodically executes the check command
@tasks.loop(seconds=CHECK_INTERVAL)
async def check_loop():
    channel = bot.get_channel(CHANNEL_ID)

    # get data dict from old_scraper
    data_dict = old_scraper.CompareData()

    # if the data dict is empty, send a message and return
    if not data_dict:
        await channel.send("No new listing")
        return
    
    await channel.send(format_data_to_markdown(data_dict[0]))


@bot.command()
async def start(ctx):
    # initialize the df
    old_scraper.start()

    # loop to see any new listing
    check_loop.start()
    await ctx.send("Started the check loop")

# Define a command to stop the background task
@bot.command()
async def stop(ctx):
    check_loop.stop()
    old_scraper.stop()
    await ctx.send("Stopped the check loop")

bot.run(BOT_TOKEN)
