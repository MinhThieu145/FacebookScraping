import discord 
from discord.ext import commands
from discord import app_commands

class ReactionCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        channel = reaction.message.channel
        # send a message to the channel saying they have react
        user_guild_id = user.guild.id
        user_name = user.name
        await channel.send(f"{user.name} has reacted with {reaction.emoji} from {user_guild_id}")

async def setup(client: commands.Bot):
    await client.add_cog(ReactionCommand(client))