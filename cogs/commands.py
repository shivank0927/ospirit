import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
import datetime
from quotes_library import get_quotes, get_authors, get_categories


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands cog is ready...")

    def error_embed(self, title, description):
        """Creates an embed for error messages."""
        return discord.Embed(title=title, description=description, color=0xFF0000)

    @commands.command(aliases=['stats', 'cs', 'cstats'])
    @commands.bot_has_guild_permissions()
    async def channelstats(self, ctx):
        """Displays information about the current channel."""
        print("Stats command initiated")
        channel = ctx.channel

        try:
            if channel.category:
                embed = discord.Embed(
                    title=f"Stats for Channel: **{channel.name}**",
                    description=f"Category: {channel.category.name}"
                )
                embed.add_field(name="Channel ID", value=channel.id, inline=False)
                embed.add_field(name="Channel Topic", value=channel.topic or 'No Topic Given!', inline=False)
                embed.add_field(name="Channel Position", value=channel.position + 1, inline=False)
                embed.add_field(name="Slowmode Delay", value=channel.slowmode_delay, inline=False)
                embed.add_field(name="Environment", value="NSFW" if channel.is_nsfw() else "Not NSFW", inline=False)
                embed.add_field(name="Permissions Synced", value=channel.permissions_synced, inline=False)
                embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d, %H:%M:%S"), inline=False)
            else:
                raise Exception("Channel does not belong to a category.")

            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['info'])
    @commands.bot_has_guild_permissions()
    async def about(self, ctx, member: discord.Member):
        """Displays information about a server member."""
        print("Member info command initiated")

        try:
            embed = discord.Embed(title=f"Information About: **{member.display_name}**")
            embed.add_field(name="Created on", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="Joined on", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="Global Name", value=member.global_name or "N/A", inline=False)
            roles = ', '.join([role.mention for role in member.roles if role != ctx.guild.default_role]) or 'No roles'
            embed.add_field(name="Roles", value=roles, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['av'])
    @commands.bot_has_guild_permissions()
    async def avatar(self, ctx, member: discord.Member = None):
        """Displays the avatar of a member. Defaults to the command caller if no member is specified."""
        print("Avatar command initiated")

        try:
            member = member or ctx.author
            embed = discord.Embed(title=f"Avatar for {member.display_name}", color=0x00FF00)
            embed.set_image(url=member.display_avatar.url)
            embed.description = f"[Avatar URL]({member.display_avatar.url})"
            embed.set_footer(text="Created by ospirit")
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        """Displays bot latency in milliseconds."""
        try:
            await ctx.send(f"Here's your ping: {round(self.client.latency * 1000)}ms")
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['q'])
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def quote(self, ctx, category: str = None):
        """Fetches and sends a random or categorized quote."""
        print("Quote command initiated")

        try:
            quote_data = get_quotes(category=category) if category else get_quotes(random=True)

            if not quote_data or "data" not in quote_data or not quote_data['data']:
                raise ValueError("No quotes found for the given category.")

            for key in quote_data['data']:
                embed = discord.Embed(color=0xFFFFFF)
                embed.add_field(name="", value=key['quote'], inline=False)
                embed.set_footer(text=f"- {key['author']}")
                await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['cap'])
    @commands.bot_has_guild_permissions(read_messages=True)
    async def caption(self, ctx):
        """Creates a caption from a replied message."""
        print("Caption command initiated")

        try:
            if ctx.message.reference:
                reference = ctx.message.reference.resolved or await ctx.channel.fetch_message(ctx.message.reference.message_id)
                message, author, url = reference.content, reference.author, reference.jump_url

                print(url)
                print(message, author)

                embed = discord.Embed()
                embed.add_field(name="", value=f"**{message.title()}**\n\n> *-by {author}*", inline=False)
                embed.set_footer(text=f"Requested by: {ctx.author}")
                embed.set_author(name=author)
                embed.add_field(name="Source", value=f"[Jump]({url})", inline=False)
                embed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(str(e))

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
            embed = self.error_embed("Invalid Input", "Please provide the correct format. Use `.help`.")
        elif isinstance(error, MissingPermissions):
            embed = self.error_embed("Missing Permissions", "You don't have the required permissions!")
        elif isinstance(error, MissingRequiredArgument):
            embed = self.error_embed("Missing Argument", f"Please provide the `{error.param.name}` argument.")
        else:
            embed = self.error_embed("Unexpected Error", "An unexpected error occurred!")
            print(f"Unexpected error: {error}")

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Commands(client))
