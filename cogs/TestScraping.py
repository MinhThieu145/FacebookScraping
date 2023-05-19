import discord 
from discord.ext import commands
from discord import app_commands
import asyncio
import json

class TestSCraping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='testscraping', description='Use to test scraping Facebook Marketplace')
    async def choosecolor(self, interation: discord.Interaction, url: str):
        await interation.response.defer(thinking=True)

        embed = discord.Embed(title='Is this the result you want',color=discord.Color.green())
        embed.add_field(name='Click the link to view the preview', value='[Preview](https://facebook-crawler-data.s3.amazonaws.com/website.pdf)', inline=False)

        # add text saying: react with 👍 if you want to want to start the crawler
        embed.add_field(name='React with 👍 if you want to want to start the crawler', value='', inline=False)
        message = await interation.followup.send(embed=embed)
        await message.add_reaction('👍')

        def CheckReaction (reaction, user):
            return user == interation.user and str(reaction.emoji) in ['👍', '👎']

        try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=CheckReaction)
        except asyncio.TimeoutError:
            await interation.followup.send('You did not react in time')
        else:
            if str(reaction.emoji) == '👍':
                 # read the json file and get the data
                with open('items.json', 'r') as f:
                    data = json.load(f)

                    for item in data:
                        item_url = item['post_link']
                        image_url = item['img_link']
                        title = item['title']
                        price = item['price']
                        location = item['location']

                        embed = discord.Embed(title=title, url=item_url)
                        embed.set_image(url=image_url)
                        embed.add_field(name="Price", value=price, inline=True)
                        embed.add_field(name="Location", value=location)
                        embed.set_footer(text="Facebook Marketplace")
                        # send the data to the channel
                        await interation.followup.send(embed=embed)
        

async def setup(client: commands.Bot):
    await client.add_cog(TestSCraping(client))