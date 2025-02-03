import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix='.', intents=intents)

def error_embed(title, description):
    """ Error Handler """
    return discord.Embed(title=title, description=description, color=0xFF0000)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print("Bot started and ready!")

@client.event
async def on_message_delete(message):
    if not message.guild or message.author.bot:
        return
    LogChannel = discord.utils.get(message.guild.channels, name="logs", type=discord.ChannelType.text)
    if LogChannel:
        if LogChannel.permissions_for(message.guild.me).send_messages:
            embed = discord.Embed(title=f"{message.author} deleted a message in {message.channel}", description=f"**Content:** {message.content}", color=0xFF0000)
            await LogChannel.send(embed=embed)
        else:
            print(f"Bot doesn't have permission to send messages in the logs channel.")
    else:
        print(f"No logs channel in {message.guild.name}")

@client.event
async def on_message_edit(message_before, message_after):
    if not message_before.guild or message_before.author.bot:
        return
    LogChannel = discord.utils.get(message_before.guild.channels, name='logs', type=discord.ChannelType.text)
    if LogChannel:
        if LogChannel.permissions_for(message_before.guild.me).send_messages:
            embed = discord.Embed(title=f"{message_before.author.name} has edited a message in {message_before.channel}", color=0xFF0000)
            embed.add_field(name="Message Before: ", value=f"{message_before.content}", inline=False)
            embed.add_field(name="Message After:", value=f"{message_after.content}", inline=False)
            await LogChannel.send(embed=embed)
        else:
            print(f"Bot doesn't have permission to send messages in the logs channel.")
    else:
        print(f"No logs channel in {message_before.guild.name}")

@client.command()
async def hello(ctx):
    """ Says hello """
    embed = discord.Embed(
        title="Hello",
        description="Hello!, How are you doing?",
        color=0x00FF00
    )
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    await client.process_commands(message) 

async def load_cogs():
    print("Loading cogs...")
    cogs_directory = "./cogs"
    for filename in os.listdir(cogs_directory):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

async def main():
    await load_cogs()
    async with client:
        await client.start(os.getenv("token"))

asyncio.run(main())
