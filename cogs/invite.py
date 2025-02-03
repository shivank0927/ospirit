import discord
import DiscordUtils
from discord.ext import commands

class Invite(commands.Cog):

    def error_embed(self, title, description):
        """Generates an error embed with a title and description."""
        return discord.Embed(title=title, description=description, color=0xFF0000) 

    def __init__(self, client):
        self.client = client
        self.tracker = DiscordUtils.InviteTracker(client)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Invite cog is ready!")
        await self.tracker.cache_invites()
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite=invite)
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite=invite)
    
    @commands.Cog.listener()
    async def on_member_join(self, member): 
        try:
            inviter = await self.tracker.fetch_inviter(member=member)
            log_channel = discord.utils.get(member.guild.channels, name="logs", type=discord.ChannelType.text)
            
            if log_channel:
                embed = discord.Embed(title="Member Joined Through Invitation", color=0xFF0000)
                embed.add_field(name="Invited by:", value=inviter.mention if inviter else "Unknown", inline=False)
                embed.add_field(name="Joined User:", value=member.mention, inline=False)
                await log_channel.send(embed=embed)
            else:
                print("Logs channel does not exist!")

        except Exception as e:
            print(f"Error occurred: {e}")

async def setup(client):
    await client.add_cog(Invite(client))
