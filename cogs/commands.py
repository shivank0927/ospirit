import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
from quotes_library import get_quotes, get_authors, get_categories



class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands cog is ready...")

    def error_embed(self, title, description): # for creating embed with handle_error fn.
        """error embeds."""
        return discord.Embed(title=title, description=description, color=0xFF0000)

    @commands.command(aliases=['stats', 'cs', 'cstats'])
    @commands.bot_has_guild_permissions()
    async def channelstats(self, ctx):
        """
        Command to check out information related to the channel.
        Displays information like channel ID, topic, position, slowmode, etc.
        """
        print("stats cmd initiated")
        channel = ctx.channel
        try:
            if channel.category:
                embed = discord.Embed(title=f"Stats for Channel: **{channel.name}**", description=f"Category: {channel.category.name}")
                embed.add_field(name="Channel id", value=channel.id, inline=False)
                embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No Topic Given!'}", inline=False)
                embed.add_field(name="Channel Position", value=channel.position+1, inline=False)
                embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
                embed.add_field(name="Channel Environment", value="NSFW" if channel.is_nsfw() else "Not NSFW", inline=False)
                embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
                embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d, %H:%M:%S"), inline=False)
            else:
                raise Exception("Channel does not belong to a category.")
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)        

    @commands.command(aliases=['info', 'who tf is'])
    @commands.bot_has_guild_permissions()
    async def about(self, ctx, member: discord.Member):
        """
        Command to view information about a member in the server.
        Displays member creation date, joining date, roles, and more.
        """
        print("member about cmd initiated")
        try:
            embed = discord.Embed(title=f"Information About: **{member.display_name}**")
            embed.add_field(name="Created on", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="Joined on", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="Global Name", value=member.global_name or "N/A", inline=False)
            roles = ', '.join([role.mention for role in member.roles if role != ctx.guild.default_role]) or 'No roles'
            embed.add_field(name="Roles", value=roles, inline=False)
            embed.add_field(name="ID:", value=member.id, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)
    
    @commands.command(aliases=['av'])
    @commands.bot_has_guild_permissions()
    async def avatar(self, ctx, member: discord.Member = None):
        """
        Command to view the avatar of a member.
        If no member is mentioned, it shows the avatar of the user who invoked the command.
        """
        print("av command initiated")
        try:
            member = ctx.author if member == None else member
            embed = discord.Embed(title=f"Avatar for {member.display_name}", color=0x00FF00)
            embed.set_image(url=member.display_avatar.url)
            embed.description = f"[Avatar URL]({member.display_avatar.url})"
            embed.set_footer(text="created by ospirit")
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['p'])
    async def ping(self, ctx, arg=None):
        try:
            await ctx.send(f"Here's Your ping... {round(self.client.latency * 1000)}ms")
        except Exception as e:
            self.handle_error(ctx, e)


    @commands.command(aliases=['q'])
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def quote(self, ctx, category: str = None):
        """Fetches and sends a quote (random or from a category)."""
        print("Quote command initiated")

        try:
            if category:
                quote_data = get_quotes(category=category)
            else:
                quote_data = get_quotes(random=True)
            if not quote_data or "data" not in quote_data or not quote_data['data']:
                raise ValueError("No quotes found for the given category.")

            for key in quote_data['data']:
                    embed = discord.Embed(title="", color=0xFFFFFF)
                    embed.add_field(name="", value=key['quote'], inline=False)
                    embed.set_footer(text=f"- {key['author']}")
                    await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_error(ctx, e)

    async def handle_error(self, ctx, error):
        """ Error handler """
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

    def cog_unload(self):
        self.client.loop.create_task(self.reddit.close())

async def setup(client):
    await client.add_cog(Commands(client))
