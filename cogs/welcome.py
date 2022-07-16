import discord
import datetime
from discord.ext import commands

client = commands.Bot(command_prefix=';', intents=discord.Intents.all(), help_command=None)

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} vừa du hành vào sever')
        embed = discord.Embed(
            title=f'Chào mừng {member.name}  🎉',
            colour=0x0dff00
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f'Đã đến với **{member.guild.name}!**',
                        value=f'*thuộc quyền sở hữu của {member.guild.owner.name}*', inline=False)
        embed.set_footer(text='🎉')
        embed.timestamp = datetime.datetime.utcnow()
        await member.guild.system_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_out(self, member):
        print(f'{member} vừa bay màu khỏi sever')
        embed = discord.Embed(
            title=f'Tạm biệt {member.name}',
            colour=0x0dff00
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f'Đã bay màu khỏi **{member.guild.name}!**',
                        value=f'*thuộc quyền sở hữu của {member.guild.owner.name}*', inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        await member.guild.system_channel.send(embed=embed)


def setup(client):
    client.add_cog(Welcome(client))