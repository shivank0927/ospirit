import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
import datetime

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    def error_embed(self, title, description):
        """Generates an error embed."""
        return discord.Embed(title=title, description=description, color=0xFF0000)

    @commands.Cog.listener()
    async def on_ready(self):
        """Triggered when the cog is ready."""
        print("Moderation cog is ready!")

    # Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not reason:
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
        await self.handle_error(ctx, error)

    # Ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
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
        await self.handle_error(ctx, error)

    # Unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):
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
        await self.handle_error(ctx, error)

    # Purge command (delete messages)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 1):
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
        await self.handle_error(ctx, error)

    # Mute command (timeout)
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, timeLimit='0s', *, reason=None):
        try:
            if timeLimit.isdigit() or ('s' in timeLimit and timeLimit[:-1].isdigit()):
                gettime = int(timeLimit.strip('s'))
                if gettime > 241900:
                    embed = discord.Embed(
                        title="Error",
                        description="Time limit cannot be larger than 28 days",
                        color=0xFF0000
                    )
                    await ctx.send(embed=embed)
                    return
                FormatTime = datetime.timedelta(seconds=gettime)
                await member.edit(timed_out_until=discord.utils.utcnow() + FormatTime if gettime else None)
                embed = discord.Embed(
                    title="Member Muted" if gettime else "Member Unmuted",
                    description=f'{member} has been muted for {FormatTime} seconds by {ctx.message.author.name}' if gettime else f'{member} has been unmuted',
                    color=0xFF0000 if gettime else 0x00FF00
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
            await self.handle_error(ctx, e)

    # Create category command
    @commands.command(aliases=['cat', 'crtcat', 'ccat'])
    @commands.has_permissions(manage_channels=True)
    async def createcategory(self, ctx, role: discord.Role, *, name):
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            await ctx.guild.create_category(name=name, overwrites=overwrites)
        except Exception as e:
            await self.handle_error(ctx, e)

    # Error handling
    async def handle_error(self, ctx, error):
        print(f'Error occurred: {error}')
        embed = None
        if isinstance(error, discord.Forbidden):
            embed = self.error_embed("Permission Denied", "I do not have permission to perform this action.")
        elif isinstance(error, discord.HTTPException):
            embed = self.error_embed("HTTP Error", "An error occurred, please try again.")
        elif isinstance(error, discord.NotFound):
            embed = self.error_embed("Not Found", "The requested resource was not found.")
        elif isinstance(error, MissingPermissions):
            embed = self.error_embed("Missing Permissions", "You don't have the required permissions!")
        elif isinstance(error, MissingRequiredArgument):
            embed = self.error_embed("Missing Argument", f"Please provide the `{error.param.name}` argument.")
        else:
            embed = self.error_embed("Unexpected Error", "An unexpected error occurred. Please contact the admin.")
            print(f"Unexpected error: {error}")
        await ctx.send(embed=embed)

# Add cog to bot
async def setup(client):
    await client.add_cog(Moderation(client))
