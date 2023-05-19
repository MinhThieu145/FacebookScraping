import asyncio
import discord 
from discord.ext import commands
from discord import app_commands

import boto3
from datetime import datetime


import time

class SetURLCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Connect to the database
    async def connect_to_database(self):
        s3_client = boto3.client('s3')
        # return the bucket
        return s3_client
    

    # Save change to the database
    async def save_to_database(self, user_id, channel_id ,url, hour, minute):

        # get the bucket
        client = await self.connect_to_database()

        # download the file
        client.download_file('facebook-crawler-data', 'url_data.csv', 'url_data.csv')

        # create new line
        new_line = f'{user_id}, {channel_id} , {url},{hour},{minute}\n'

        # append the new line to the file
        with open('url_data.csv', 'a') as f:
            f.write(new_line)

        # upload the file to the bucket
        client.upload_file('url_data.csv', 'facebook-crawler-data', 'url_data.csv')

    # # a function to see a screen shot of the website
    # async def get_screenshot(self, url):
    #     # set up chrome driver
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--window-size=1920x1080")
    #     chrome_options.add_argument("--disable-gpu")

    #     # set up driver
    #     driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')

    #     # get the url
    #     driver.get(url)

    #     # wait for the page to load
    #     time.sleep(2)

    #     # take a screenshot
    #     driver.save_screenshot('screenshot.png')

    #     # close the driver
    #     driver.quit()

    @app_commands.command(name='seturl', description='Set the URL you want to scrap and the schedule you want it to run')
    @app_commands.describe(hour='Will repeat every x hour', minute ='Will repeat every x minute')
    @app_commands.choices(hour = [ 
        app_commands.Choice(name='1', value='1'),
        app_commands.Choice(name='2', value='2'),
        app_commands.Choice(name='3', value='3'),
        app_commands.Choice(name='4', value='4'),
        app_commands.Choice(name='5', value='5'),
    ])

    # only 0, 15, 30 and 60 for minute
    @app_commands.choices(minute = [
        app_commands.Choice(name='0', value='0'),
        app_commands.Choice(name='15', value='15'),
        app_commands.Choice(name='30', value='30'),
        app_commands.Choice(name='45', value='45'),
    ])        
    
    async def seturl(self, interation: discord.Interaction, url: str, hour: app_commands.Choice[str], minute: app_commands.Choice[str]):
        try:
            await interation.response.defer(thinking=True)
            
            # call the function to get the screenshot

            embed = discord.Embed(title='Is this the result you want', description='Setting the URL for the crawler', color=discord.Color.green())
            embed.add_field(name='URL', value=url, inline=False)
            embed.add_field(name='Click the link to view the preview', value='[Preview](https://facebook-crawler-data.s3.amazonaws.com/website.pdf)', inline=False)

            message = await interation.followup.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            
            def CheckReaction (reaction, user):
                return user == interation.user and str(reaction.emoji) in ['👍', '👎']
            
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=CheckReaction)
            except asyncio.TimeoutError:
                await interation.followup.send('You did not react in time')
            else:
                if str(reaction.emoji) == '👍':
                    # Get the user id
                    user_id = interation.user.id

                    # get the channel id
                    channel_id = interation.channel.id


                    # Save the data to the database
                    await self.save_to_database(user_id=user_id, url=url, channel_id=channel_id ,hour=hour.value, minute=minute.value)

                    await interation.followup.send('URL has been set')
                else:
                    await interation.followup.send('URL has not been set')



        except Exception as e:
            await interation.followup.send(e)

async def setup(client: commands.Bot):
    await client.add_cog(SetURLCommand(client))