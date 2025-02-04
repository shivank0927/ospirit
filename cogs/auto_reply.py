import discord
from discord.ext import commands

# file for auto reponse system through ai api maybe??

class AutoReply(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self): # cog listener
        print("auto replying cog is ready")

async def setup(client):
    await client.add_cog(AutoReply(client))