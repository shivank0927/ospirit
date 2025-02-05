import discord
import DiscordUtils
from discord.ext import commands

class Invite(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tracker = DiscordUtils.InviteTracker(client)

    def error_embed(self, title, description):
        """Generates an error embed with a title and description."""
        return discord.Embed(title=title, description=description, color=0xFF0000)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Invite cog is ready!")
        await self.tracker.cache_invites()
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):    # Updates cache when invite is created
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):  # Removes from cache when invite is deleted
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_member_join(self, member):  # Tracks member joined by link of someone else's
        try:
            inviter = await self.tracker.fetch_inviter(member)
            log_channel = discord.utils.get(member.guild.channels, name="logs", type=discord.ChannelType.text)

            if log_channel and log_channel.permissions_for(member.guild.me).send_messages:
                embed = discord.Embed(title="Member Joined Through Invitation", color=0x00FF00)
                embed.add_field(name="Invited by:", value=inviter.mention if inviter else "Unknown", inline=False)
                embed.add_field(name="Joined User:", value=member.mention, inline=False)
                await log_channel.send(embed=embed)
            else:
                print(f"Logs channel missing or bot lacks permissions in {member.guild.name}")

        except Exception as e:
            print(f"Error tracking inviter: {e}")

async def setup(client):
    await client.add_cog(Invite(client))
