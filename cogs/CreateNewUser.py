import discord 
from discord.ext import commands
from discord import app_commands

import boto3

from datetime import datetime

class CreateNewUser(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    # Connect to database - S3 bucket
    async def connect_to_database(self):
        s3_client = boto3.client('s3')

        # return the bucket
        return s3_client


    # Create a new user Command
    @app_commands.command(name='createuser', description='Innitiate the bot')
    async def createuser(self, interation: discord.Interaction):
        # delay the response
        await interation.response.defer(thinking=True)

        try:

            # get the user-data file from bucket
            client = await self.connect_to_database()

            # get the user-data file from bucket
            client.download_file('facebook-crawler-data', 'user_data.csv', 'user_data.csv')

            # create new line
            current_date = datetime.now().strftime("%Y-%m-%d")
            username = interation.user.name
            user_id = interation.user.id
            channel_id = interation.channel_id
            new_line = f'{current_date},{username},{user_id}, {channel_id}\n'

            # append the new line to the file
            with open('user_data.csv', 'a') as f:
                f.write(new_line)

            # upload the file to the bucket
            client.upload_file('user_data.csv', 'facebook-crawler-data', 'user_data.csv')

            # send the message
            await interation.followup.send('User created successfully', ephemeral=True)
        
        except Exception as e:
            await interation.followup.send(e, ephemeral=True)            




async def setup(client: commands.Bot):
    await client.add_cog(CreateNewUser(client))