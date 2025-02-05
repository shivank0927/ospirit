import os
import discord
from discord.ext import commands
import asyncio

# Bot intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Bot instance
client = commands.Bot(command_prefix='.', intents=intents)

# Error Embed Utility
def error_embed(title, description):
    """Creates an error embed message."""
    return discord.Embed(title=title, description=description, color=0xFF0000)

@client.event
async def on_ready():
    """Triggered when the bot is ready."""
    await client.change_presence(status=discord.Status.idle)
    print("Bot started and ready!")

@client.event
async def on_message_delete(message):
    """Logs deleted messages in a 'logs' channel."""
    if not message.guild or message.author.bot:
        return
    
    log_channel = discord.utils.get(message.guild.channels, name="logs", type=discord.ChannelType.text)
    
    if log_channel and log_channel.permissions_for(message.guild.me).send_messages:
        embed = discord.Embed(
            title=f"Message Deleted in #{message.channel}",
            description=f"**Author:** {message.author}\n**Content:** {message.content}",
            color=0xFF0000
        )
        await log_channel.send(embed=embed)
    else:
        print(f"Log channel missing or bot lacks permissions in {message.guild.name}")

@client.event
async def on_message_edit(before, after):
    """Logs edited messages in a 'logs' channel."""
    if not before.guild or before.author.bot or before.content == after.content:
        return
    
    log_channel = discord.utils.get(before.guild.channels, name="logs", type=discord.ChannelType.text)

    if log_channel and log_channel.permissions_for(before.guild.me).send_messages:
        embed = discord.Embed(
            title=f"Message Edited in #{before.channel}",
            color=0xFFA500
        )
        embed.add_field(name="Before:", value=before.content, inline=False)
        embed.add_field(name="After:", value=after.content, inline=False)
        embed.set_footer(text=f"Edited by {before.author}")
        await log_channel.send(embed=embed)
    else:
        print(f"Log channel missing or bot lacks permissions in {before.guild.name}")

@client.event
async def on_message(message):
    """Processes commands and prevents bot from responding to itself."""
    if message.author.bot:
        return
    await client.process_commands(message)

async def load_cogs(): # Loads all cogs from directory "cogs"
    print("Loading cogs...")
    cogs_directory = "./cogs"
    for filename in os.listdir(cogs_directory):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

async def main(): # Start the bot
    await load_cogs()
    async with client:
        await client.start(os.getenv("TOKEN"))

asyncio.run(main())
