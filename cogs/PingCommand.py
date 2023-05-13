import discord 
from discord.ext import commands
from discord import app_commands

class PingCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='choosecolor', description='Choose a color')
    @app_commands.describe(colors='The color you want to choose')
    @app_commands.choices(colors = [
        app_commands.Choice(name='Red', value='red'),
        app_commands.Choice(name='Blue', value='blue'),
        app_commands.Choice(name='Green', value='green'),
    ])
    async def choosecolor(self, interation: discord.Interaction, colors: app_commands.Choice[str]):
        await interation.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms, color selected {colors.name}")

async def setup(client: commands.Bot):
    await client.add_cog(PingCommand(client))