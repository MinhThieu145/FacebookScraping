import discord 
from discord.ext import commands
from discord import app_commands

class TestSCraping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='testscraping', description='Use to test scraping Facebook Marketplace')
    async def choosecolor(self, interation: discord.Interaction, url: str):
        await interation.response.send_message('I am testing scraping Facebook Marketplace')
        

async def setup(client: commands.Bot):
    await client.add_cog(TestSCraping(client))