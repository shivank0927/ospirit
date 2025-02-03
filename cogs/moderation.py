import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument
import datetime

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    def error_embed(self, title, description):
        """Generates an error embed with a title and description."""
        return discord.Embed(title=title, description=description, color=0xFF0000) 


    @commands.Cog.listener() 
    async def on_ready(self):
        """Runs when the cog is ready and bot is online."""
        print("Moderation cog is ready!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kicks a member from the server.
        
        Parameters:
        - member: The member to be kicked.
        - reason: The reason for kicking the member (optional).
        """
        print('initiating kick of a member')
        if not reason: # addup?
            reason = "No reason provided."
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member} has been kicked by {ctx.message.author.name}. Reason: {reason}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @kick.error
    async def kick_error(self, ctx, error):
        """Handles errors for the kick command."""
        await self.handle_error(ctx, error)

    # ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        Bans a member from the server.
        
        Parameters:
        - member: The member to be banned.
        - reason: The reason for banning the member (optional).
        """
        print("initiating ban of a member")
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member} has been banned by {ctx.message.author.name}. Reason: {reason or 'No reason provided.'}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @ban.error
    async def ban_error(self, ctx, error):
        """Handles errors for the ban command."""
        await self.handle_error(ctx, error)

    # unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):
        """
        Unbans a member from the server.
        
        Parameters:
        - id: The user ID of the banned member.
        - reason: The reason for unbanning (optional).
        """
        print("initiating unbanning")
        if id:
            try:
                user = await self.client.fetch_user(id)
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="Member Unbanned",
                    description=f'{user} has been unbanned by {ctx.message.author.name}',
                    color=0x00FF00
                )
                await ctx.send(embed=embed)
            except Exception as e:
                await self.handle_error(ctx, e)

    @unban.error
    async def unban_error(self, ctx, error):
        """Handles errors for the unban command."""
        await self.handle_error(ctx, error)

    # purge command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 1):
        """
        Purges messages from the server.
        
        Parameters:
        - limit: The number of messages to purge (default is 1).
        """
        print("initiating purge")
        try:
            await ctx.channel.purge(limit=limit, bulk=True)
            embed = discord.Embed(
                title="Messages Purged",
                description=f"{limit} messages were removed by {ctx.message.author.name}",
                color=0x00FF00
            )
            await ctx.channel.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @purge.error
    async def purge_error(self, ctx, error):
        """Handles errors for the purge command."""
        await self.handle_error(ctx, error)

    # timeout command
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, timeLimit='0s', *, reason=None):
        """
        Mutes a member from the text channel for a specific time.
        
        Parameters:
        - member: The member to be muted.
        - timeLimit: The time duration for which the member will be muted (default is '0s').
        - reason: The reason for muting the member (optional).
        """
        await ctx.send("timeout cmd initiated")
        try:
            if 's' in timeLimit and timeLimit.isalnum():
                if timeLimit == '0s' or timeLimit == '0':
                    await member.edit(timed_out_until=None)
                    embed = discord.Embed(
                        title="Member Unmuted",
                        description=f"{member} has been unmuted",
                        color=0x00FF00
                    )
                    await ctx.send(embed=embed)
                else:
                    gettime = int(timeLimit.strip('s'))
                    if gettime > 241900:
                        embed = discord.Embed(
                            title="Error",
                            description="Time limit cannot be larger than 28 days",
                            color=0xFF0000
                        )
                        await ctx.send(embed=embed)
                    else:
                        FormatTime = datetime.timedelta(seconds=gettime)
                        await member.edit(timed_out_until=discord.utils.utcnow() + FormatTime)
                        embed = discord.Embed(
                            title="Member Muted",
                            description=f'{member} has been muted for {FormatTime} seconds by {ctx.message.author.name}',
                            color=0xFF0000
                        )
                        await ctx.send(embed=embed)
            elif timeLimit.isdigit():
                gettime = int(timeLimit)
                FormatTime = datetime.timedelta(seconds=gettime)
                await member.edit(timed_out_until=discord.utils.utcnow() + FormatTime)
                embed = discord.Embed(
                    title="Member Muted",
                    description=f'{member} has been muted for {FormatTime} seconds by {ctx.message.author.name}',
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Invalid Command Format",
                    description="Enter command in the correct format, type `.help` for options",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        except Exception as e:
            """ """
            await self.handle_error(ctx, e)

    # create category command
    @commands.command(aliases=['cat', 'crtcat', 'ccat'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def createcategory(self, ctx, role: discord.Role, *, name):
        """
        Creates a new category in the server.
        
        Parameters:
        - role: The role that will have permissions to view the category.
        - name: The name of the category to be created.
        """
        print("creating category command initiated")
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            category = await ctx.guild.create_category(name=name, overwrites=overwrites)
            embed = discord.Embed(
                title="Category Created",
                description=f"Created a category named {category.name}",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    # create channel command
    @commands.command(aliases=["crchan", "chan", "cchan"]) # for the command itself
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def createchanel(self, ctx, role: discord.Role, *, name):
        """
        Creates a new channel in the server.
        
        Parameters:
        - role: The role that will have permissions to view the channel.
        - name: The name of the channel to be created.
        """
        print("creating channel command initiated")
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
            embed = discord.Embed(
                title="Channel Created",
                description=f"Created a channel named {channel.name}",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    # create a logs command
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def logs(self, ctx, role: discord.Role):
        """
        Creates a moderation logs category and channel.
        
        Parameters:
        - role: The role that will have access to the logs.
        """
        print("setting up logs for moderation, please wait")
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            LogCategory = await ctx.guild.create_category(name="Moderation", overwrites=overwrites, position=200)
            LogChannel = await ctx.guild.create_text_channel(name="logs", overwrites=overwrites, category=LogCategory)
            embed = discord.Embed(
                title="Logs Created",
                description="Logs have been created! WARNING: If you didn't ping the role with admin perms, the logs will be public!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await self.handle_error(ctx, e)

    
    # exceptions
    async def handle_error(self, ctx, error):
        print(f'Error occurred: {error}')
        embed = None
        if isinstance(error, discord.Forbidden):
            embed = self.error_embed("Permission Denied", "I do not have permission to perform this action.")
        elif isinstance(error, discord.HTTPException):
            embed = self.error_embed("HTTP Error", "An error occurred, please try again.")
        elif isinstance(error, discord.NotFound):
            embed = self.error_embed("Not Found", "The requested resource was not found.")
        elif isinstance(error, ValueError):
            embed = self.error_embed("Invalid Input", "Please provide the correct format. Use `.help` for guidance.")
        elif isinstance(error, MissingPermissions):
            embed = self.error_embed("Missing Permissions", "You don't have the required permissions!")
        elif isinstance(error, MissingRequiredArgument):
            embed = self.error_embed("Missing Argument", f"Please provide the `{error.param.name}` argument.")
        else:
            embed = self.error_embed("Unexpected Error", "An unexpected error occurred. Please contact the admin.")
            print(f"Unexpected error: {error}") 

        await ctx.send(embed=embed)

# add cog to bot
async def setup(client):
    await client.add_cog(Moderation(client))