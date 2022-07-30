import discord
from discord.ext import commands

client = commands.Bot(command_prefix=';', intents=discord.Intents.all(), help_command=None)

shelp1 = [
    'new', 'nickname', 'info', 'weather', 'dog', 'cat', 'fng'
]

shelp2 = [
    'play', 'fplay', 'pause', 'resume', 'leave', 'skip', 'nowplaying', 'loop', 'qloop', 'search', 'queue', 'cqueue'
]


class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def new(self, ctx):
        embed = discord.Embed(title='Những update mới:',
                              description='**Chức năng**:\n'
                                          '1: Thả ảnh chó, mèo - lệnh cat, dog\n'
                                          '2: Nâng cấp tính năng thời tiết - giờ đây có thể dự báo 5 ngày từ hôm nay - lệnh wt daily\n'
                                          '**Phát nhạc**:\n'
                                          '1: Nâng cấp danh sách phát dễ nhìn hơn\n'
                                          '2: Lệnh để xem bài hát hiện đang phát - lệnh n\n'
                                          '3: Lệnh xóa các bài hiện có trong danh sách phát theo nhiều cách khác nhau\n'
                                          '4: Lệnh loop mới - loop bài hiện tại và loop danh sách phát\n'
                                          '5: Lệnh play ưu tiên, bỏ qua và phát thay bài hiện tại, ko làm ảnh hưởng danh sách phát - lệnh fp\n'
                                          '- Mọi chi tiết khác xem qua lệnh **`help`**',
                              colour=discord.Colour.blue())

        await ctx.send(embed=embed)

    @commands.command(aliases=['help', 'h'])
    async def jhelp(self, ctx, sub=None):
        await ctx.message.add_reaction('👍')
        if sub == None or sub == '0':
            embed = discord.Embed(title=f'⚜️ Danh sách lệnh của **{self.client.user.name}** ⚜️',
                                  description='Prefix: **`;`**',
                                  colour=0x0dff00)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/911864508618788887/913719703493570560/giphy_3.gif')

            fields = [
                ('1️⃣  > **Hành động**',
                 f'`{shelp1[0]}`, `{shelp1[1]}`, `{shelp1[2]}`, `{shelp1[3]}`, `{shelp1[4]}`, `{shelp1[5]}`, `{shelp1[6]}`',
                 False),
                ('2️⃣  > **Phát nhạc youtube**',
                 f'`{shelp2[0]}`, `{shelp2[1]}`, `{shelp2[2]}`, `{shelp2[3]}`, `{shelp2[4]}`, `{shelp2[5]}`, `{shelp2[6]}`, `{shelp2[7]}`, `{shelp2[8]}`, `{shelp2[9]}`, `{shelp2[10]}`, `{shelp2[11]}`',
                 False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=';help 1 \ ;help 2: để biết thêm chi tiết')

            await ctx.send(embed=embed)

        elif sub == '1':
            embed = discord.Embed(title='♦️ Hành động', description='Prefix: **`;`**', colour=0x0dff00)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/911864508618788887/913719703493570560/giphy_3.gif')

            fields = [
                ('**`new`**', 'Xem những thay đổi và cập nhập mới', False),
                ('**`nickname`**', '- Viết tắt: **`nn`** \n- Đổi nickname của người a thành b \n- `;nn @a b`', False),
                ('**`info`**', '- Viết tắt: **`if`** \n- Hiện thông tin của người được tag \n- `;if @a`', False),
                ('**`weather`**',
                 '- Viết tắt: **`wt`** - Thời tiết hiện tại của tp.HCM\nLựa chọn:\n- **`wt daily`**: Xem dự báo thời tiết 5 ngày từ hôm nay',
                 False),
                ('**`dog`**', '- Một tấm ảnh chó ngẫu nhiên', False),
                ('**`cat`**', '- Một tấm ảnh mèo ngẫu nhiên', False),
                ('**`fng`**', '- Show Bitcoin Fear & Greed', False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

        elif sub == '2':
            embed = discord.Embed(title='♥️ Phát nhạc youtube', description='Prefix: **`;`**', colour=0x0dff00)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/911864508618788887/913719703493570560/giphy_3.gif')

            fields = [
                ('**`play`**',
                 '- Viết tắt: **`p`** \n- Auto join và play\n- Có thể play được link và tên\n- Play theo tên sẽ play kết quả đầu tiên tìm được trong search\n- Lưu ý hiện tại **không** play được __playlist__ hay là __stream - live__',
                 False),
                ('**`fplay`**', '- Viết tắt: **`fp`** \n- Ngắt bài hát hiện hại và play bài ưu tiên ngay lập tức',
                 False),
                ('**`pause`**', '- Viết tắt: **`s`** \n- Tạm dừng bài hát hiện tại', False),
                ('**`remuse`**', '- Viết tắt: **`r`** \n- Tiếp tục bài hát hiện tại', False),
                ('**`leave`**', '- Viết tắt: **`l`** \n- Đuổi Johíu khỏi voice', False),
                ('**`skip`**', '- Viết tắt: **`k`** \n- Vote skip bài hát hiện tại', False),
                ('**`nowplaying`**', '- Viết tắt: **`n`** \n- Hiện bài hát đang phát hiện tại', False),
                ('**`loop`**',
                 '- Viết tắt: **`o`**\n- Xem bài hiện tại có đang lặp hay ko\n- Lựa chọn:\n- **`o on`**: Bật loop bài hiện tại\n- **`o off`**: Tắt loop',
                 False),
                ('**`qloop`**',
                 '- Viết tắt: **`qo`**\n- Xem danh sách phát có đang lặp hay ko\n- Lựa chọn:\n- **`qo on`**: Lặp toàn bộ danh sách phát hiện tại\n- **`qo off`**: Tắt loop',
                 False),
                ('**`search`**', '- Viết tắt: **`f`** \n- Tìm kiếm bài hát', False),
                ('**`queue`**', '- Viết tắt: **`q`** \n- Danh sách phát hiện tại', False),
                ('**`cqueue`**',
                 '- Viết tắt: **`cq`** \n- Xóa các bài trong danh sách phát hiện tại\n- Lệnh có nhiều cách xóa\n- Dùng lệnh để biết thêm chi tiết',
                 False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_footer(
                text='Tự động rời phòng nếu ko có hoạt động trong 5 phút, đang tạm dừng phát sẽ là 15 phút')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Lỗi hoặc lệnh không tồn tại', description='**`;help`**  để xem hướng dẫn',
                                  colour=0xff0000)
            await ctx.send(embed=embed)
            return

    @commands.command(aliases=['info', 'if'])
    async def jinfo(self, ctx, target: discord.Member = None):
        if target is None:
            target = ctx.author
        else:
            target = target

        bot_id = ['911855562361278565', '912789977153282109', '913127552829259777']

        created_by = f'*Created by*: [ArtA#3566](https://discordapp.com/users/779359246227472425)' if any(
            id in str(target.id) for id in bot_id) else ''

        embed = discord.Embed(title=f'Infomation of {target.name}',
                              description=created_by,
                              colour=target.colour)
        embed.set_thumbnail(url=target.avatar_url)
        fields = [
            ('ID', target.id, False),
            ('Name', target.name, True),
            ('Nick', target.nick, True),
            ('Bot?', target.bot, True),
            ('Status', str(target.status).title(), True),
            ('Activity',
             f"{target.activity.type.name if target.activity else 'N /'} {target.activity.name if target.activity else 'A'}",
             True),
            ('Top role', target.top_role, True),
            ('Created at', target.created_at.strftime('%d/%m/%Y'), True),
            ('Joined at', target.joined_at.strftime('%d/%m/%Y'), True),
            ('Boosted', bool(target.premium_since), True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(aliases=['nickname', 'nn'])
    async def jnickname(self, ctx, member: discord.Member, nick):
        await member.edit(nick=nick)
        await ctx.send(f'Nickname đã được đổi thành {member.mention} ')


def setup(client):
    client.add_cog(Command(client))
