import asyncio
import youtube_dl
import discord
import random

from discord.ext import commands

client = commands.Bot(command_prefix=';',
                      intents=discord.Intents.all(),
                      help_command=None)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_id = 0
        self.song_queue = {}
        self.current = {}
        self.loop = {}
        self.previous = {}
        self.setup()

    def setup(self):
        for guild in self.client.guilds:
            self.song_queue[guild.id] = []
            self.current[guild.id] = {}
            self.loop[guild.id] = {}
            self.previous[guild.id] = False

    async def hyphen(self, ctx, sub):  # khi sub.find('-') trả về -1 (False)
        sub = sub.split('-')  # tách thành list

        try:  # check có nhập đúng int hay ko
            for i in range(len(sub)):  # biến list str thành list int
                sub[i] = int(sub[i])

            sub.sort()  # chắc chắn a < b

            if len(
                    sub
            ) > 2:  # check nhập đúng a-b hay ko, list phai == 2 ['a', 'b']
                await ctx.send(
                    'Nhập cho đúng chứ. Lệnh **`help`** để biết thêm')

            else:
                for i in range(
                        sub[0] - 1, sub[1]
                ):  # bắt đầu, chạy từ a-1 đến b(b đã tự -1), -1 vì list tính từ 0
                    self.song_queue[ctx.guild.id].pop(
                        sub[0] - 1
                    )  # xóa ở vị trí (a-1) (b) lần vì mỗi lần xóa thứ tự đôn lên
        except:
            await ctx.send('Nhập cho đúng chứ. Lệnh **`help`** để biết thêm'
                           )  # lỗi nhập chữ, không int đc,...

    async def comma(self, ctx, sub):
        sub = sub.split(',')  # tách thành list

        try:  # check có nhập đúng hay ko
            for i in range(len(sub)):  # biến list str thành list int
                sub[i] = int(sub[i])

            copy = self.song_queue[ctx.guild.id].copy(
            )  # tạo một bản copy vì length sẽ thay đổi khi pop thành ra lỗi (cách tạm thời)

            sub.sort()  # sắp xếp a cho dễ pop

            sub = list(dict.fromkeys(sub))  # loại bỏ trùng lặp

            for i in reversed(
                    range(len(sub))
            ):  # chạy trong length a từ lớn đến bé tránh khi pop bị đôn lên
                for j in range(len(copy)):  # chạy hết length bản copy
                    if sub[i] - 1 == j:
                        self.song_queue[ctx.guild.id].pop(j)
        except:
            await ctx.send('Nhập cho đúng chứ. Lệnh **`help`** để biết thêm'
                           )  # lỗi nhập chữ, không int đc,...

    async def check_queue(self, ctx):
        if ctx.guild.voice_client.is_playing():
            return

        if self.loop[self.channel_id]['q'] == True:
            self.song_queue[ctx.guild.id].append(self.current[self.channel_id])

        id = random.randint(
            0,
            len(self.song_queue[ctx.guild.id]) -
            1) if self.loop[self.channel_id]['r'] == True else 0
        await self.play_song(ctx, self.song_queue[ctx.guild.id][id])
        self.song_queue[ctx.guild.id].pop(id)

        if not self.song_queue[ctx.guild.id]:
            embed = discord.Embed(
                title='Đang phát bài hát cuối cùng!', colour=discord.Color.dark_grey())
            await self.client.get_channel(self.channel_id).send(embed=embed)

    async def search_song(self, amount, song, get_url=False):
        info = await self.client.loop.run_in_executor(
            None, lambda: youtube_dl.YoutubeDL({
                "format": "bestaudio",
                "quiet": True
            }).extract_info(f"ytsearch{amount}:{song}",
                            download=False,
                            ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0:
            return None

        return [entry["webpage_url"]
                for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTIONS = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            def extract(x=0):
                if x == 3:
                    return None
                try:
                    info = ydl.extract_info(song['mp4'], download=False)
                    return info
                except:
                    x += 1
                    extract(x)

            info = extract()
            if info is None:
                if not self.song_queue[ctx.guild.id]:
                    return await self.client.get_channel(
                        self.channel_id
                    ).send(f"Current song is error! Change to other song or try again later.")
                await self.client.get_channel(
                    self.channel_id
                ).send(f"Current song is error! Change to next song.")

            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(
                url2, **FFMPEG_OPTIONS)
            self.previous[ctx.guild.id] = True
            ctx.guild.voice_client.play(source)
            await self.client.get_channel(
                self.channel_id
            ).send(f"Now playing: {song['d']}")
            self.current[self.channel_id] = song

    @commands.command()
    async def test(self, ctx, sub=None):
        return await ctx.send(self.channel_id)

    @commands.command()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()

    @commands.command(aliases=['play', 'p'])
    async def jplay(self, ctx, *, song=None):
        await ctx.message.add_reaction('▶️')
        try:
            if ctx.author.voice is None:
                await ctx.send('Chui vào voice đi cái đã')
                return
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
        except:
            pass

        def setup():
            self.channel_id = ctx.channel.id
            self.loop[self.channel_id] = {'1': '', 'r': '', 'q': ''}
            self.loop[self.channel_id]['1'] = False
            self.loop[self.channel_id]['r'] = False
            self.loop[self.channel_id]['q'] = False

        if "youtube.com/playlist?" in song:
            await ctx.send("Loading playlist...")
            await ctx.send("Longer playlist take more time")
            pre_queue_len = len(
                self.song_queue[ctx.guild.id])

            info = youtube_dl.YoutubeDL({
                "format": "bestaudio",
                "quiet": True
            }).extract_info(song, download=False)

            for s in info['entries']:
                mp4 = s['formats'][0][
                    'url'] if ".googlevideo.com/videoplayback" in s['formats'][
                        0]['url'] else s['formats'][0]['fragment_base_url']
                self.song_queue[ctx.guild.id].append({
                    's': s['title'],
                    'd': s['webpage_url'],
                    'mp4': mp4
                })

            if ctx.voice_client.is_playing():
                return await ctx.send(
                    f"Hiện có bài đang phát, playlist sẽ được thêm vào cuối danh sách phát! Tổng: **`{len(self.song_queue[ctx.guild.id])}`**"
                )

            await ctx.send(
                f"{len(self.song_queue[ctx.guild.id])-pre_queue_len} bài hát được thêm vào danh sách phát! Tổng: **`{len(self.song_queue[ctx.guild.id])}`**."
            )

            return setup()

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Đang tìm kiếm... mất một vài giây.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send(
                    "Không tìm thấy kết quả, hãy thử dùng lệnh **` ;search hoặc ;s `**."
                )

            song = result[0]

        # check any song is playing
        queue_len = len(self.song_queue[ctx.guild.id])
        info = youtube_dl.YoutubeDL({
            "format": "bestaudio",
            "quiet": True
        }).extract_info(song, download=False)

        if ctx.voice_client.is_playing():
            mp4 = info['formats'][0][
                'url'] if ".googlevideo.com/videoplayback" in info['formats'][
                    0]['url'] else info['formats'][0]['fragment_base_url']
            self.song_queue[ctx.guild.id].append({
                's': info['title'],
                'd': song,
                'mp4': mp4
            })
            return await ctx.send(
                f"Hiện có bài đang phát **`{info['title']}`** sẽ được thêm vào danh sách phát ở vị trí: **`{queue_len + 1}`**."
            )

        setup()
        mp4 = info['formats'][0][
            'url'] if ".googlevideo.com/videoplayback" in info['formats'][0][
                'url'] else info['formats'][0]['fragment_base_url']
        song = {"s": info['title'], "d": song, "mp4": mp4}
        await self.play_song(ctx, song)

    @ commands.command(aliases=['fplay', 'fp'])
    async def jforceplay(self, ctx, *, song=None):
        if song is None:
            embed = discord.Embed(
                title='Hướng dẫn dùng force play - phát ưu tiên',
                description='',
                colour=discord.Color.orange())
            embed.description += '\n- **`fplay`** hay **`fp`**'
            embed.description += '\n- **`fp [stt]`**: ưu tiên play bài hát có stt trong queue'
            embed.description += '\n- **`fp [bài hát hoặc link]`**: tìm kiếm bài hát nếu không phải link và play nó ngay lập tức'
            return await ctx.send(embed=embed)

        await ctx.message.add_reaction('▶️')
        try:
            if ctx.author.voice is None:
                await ctx.send('Chui vào voice đi cái đã')
                return
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
        except:
            pass

        try:
            id = int(song) - 1
            check = True
        except:
            check = False

        if check <= len(self.song_queue[ctx.guild.id]):
            try:
                ctx.voice_client.stop()
                self.loop[self.channel_id]['1'] = False
                await self.play_song(ctx, self.song_queue[ctx.guild.id][id])
                return self.song_queue[ctx.guild.id].pop(id)
            except:
                pass

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Đang tìm kiếm... mất một vài giây.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send(
                    "Không tìm thấy kết quả, hãy thử dùng lệnh **search**.")

            song = result[0]

        info = youtube_dl.YoutubeDL({
            "format": "bestaudio",
            "quiet": True
        }).extract_info(song, download=False)
        mp4 = info['formats'][0][
            'url'] if ".googlevideo.com/videoplayback" in info['formats'][0][
                'url'] else info['formats'][0]['fragment_base_url']
        self.loop[self.channel_id]['1'] = False
        song = {'s': info['title'],
                'd': info['webpage_url'],
                'mp4': mp4}
        ctx.voice_client.stop()
        await self.play_song(ctx, song)

    @ commands.command(aliases=['replay', 'rp'])
    async def jreplay(self, ctx):
        try:
            if ctx.author.voice is None:
                await ctx.send('Chui vào voice đi cái đã')
                return
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
        except:
            pass

        if not self.current[self.channel_id]:
            return await ctx.send('Không có bài nào đang play cả!')

        await ctx.message.add_reaction('🔄')
        ctx.voice_client.stop()
        current = self.current[self.channel_id]
        self.loop[self.channel_id]['1'] = False
        await self.play_song(ctx, current)

    @ commands.command(aliases=['leave', 'l'])
    async def jleave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.message.add_reaction('🆗')
            ctx.voice_client.pause()
            return await ctx.voice_client.disconnect()

        await ctx.send("Có đang ở trong voice đâu?.")

    @ commands.command(aliases=['pause', 's'])
    async def jpause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("Đang dừng rồi mà?")

        ctx.voice_client.pause()
        await ctx.message.add_reaction('🆗')
        await ctx.send("Đã tạm dừng ⏸️")

    @ commands.command(aliases=['resume', 'r'])
    async def jresume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice đâu?")

        if ctx.voice_client.is_playing():
            return await ctx.send("Vẫn đang play mà?")

        if not ctx.voice_client.is_paused():
            return await ctx.send("Có đang play gì đâu?")

        ctx.voice_client.resume()
        await ctx.message.add_reaction('🆗')
        await ctx.send("Bài hát hiện tại đã được tiếp tục ▶️")

    @ commands.command(aliases=['loop', 'o'])
    async def jloop(self, ctx, sub=None):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice đâu?")

        if sub is None:
            if self.loop[self.channel_id]['1'] == False:
                await ctx.send('Hiện loop đang **`Tắt\off`**')
            else:
                await ctx.send(f"Hiện loop đang **`Bật\on`**")
        else:
            if sub == 'on':
                await ctx.message.add_reaction('🔂')
                self.loop[self.channel_id]['1'] = True
                desc = f"Current: [{self.current[self.channel_id]['s']}]({self.current[self.channel_id]['d']})" if not \
                    self.current[self.channel_id] else ""
                embed = discord.Embed(title="Bắt đầu loop!",
                                      description=desc,
                                      colour=discord.Colour.teal())
                return await ctx.send(embed=embed)
            elif sub == 'off':
                await ctx.message.add_reaction('❌')
                self.loop[self.channel_id]['1'] = False
                embed = discord.Embed(title='Đã dừng loop!',
                                      colour=discord.Colour.dark_teal())
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Sai lệnh! Thử lại xem")

    @ commands.command(aliases=['random', 'qr'])
    async def queue_random(self, ctx, sub: str = None):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice đâu?")

        check = self.loop[self.channel_id]['r']
        status = {
            'name': 'Bật\on',
            'icon': '⭕',
            'color': discord.Colour.gold()
        } if check is True else {
            'name': 'Tắt\off',
            'icon': '❌',
            'color': discord.Colour.dark_gold()
        }

        async def send_status(already=False):
            str = f"Queue Random đang **`{status['name']} {status['icon']}`**"
            embed = discord.Embed(title=str if not already else str +
                                  " rồi mà!",
                                  colour=status['color'])
            await ctx.send(embed=embed)

        async def turn_on():
            await ctx.message.add_reaction('🔀')
            self.loop[self.channel_id]['r'] = True
            embed = discord.Embed(title="Bắt đầu Random!",
                                  colour=discord.Colour.gold())
            await ctx.send(embed=embed)

        async def turn_off():
            await ctx.message.add_reaction('❌')
            self.loop[self.channel_id]['r'] = False
            embed = discord.Embed(title='Đã dừng Random!',
                                  colour=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

        if sub is None:
            if check:
                return await turn_off()
            return await turn_on()

        if sub.lower() in ['s', 'status']:
            await ctx.message.add_reaction('🆗')
            return await send_status()

        if sub.lower() == 'on':
            if check:
                return await send_status(already=True)
            return await turn_on()

        if sub.lower() == 'off':
            if not check:
                return await send_status(already=True)
            return await turn_off()

        return await ctx.send(embed=discord.Embed(
            title="Sai lệnh! Thử lại xem | **` ;help `**"))

    @ commands.command(aliases=['qloop', 'qo'])
    async def jqueueloop(self, ctx, sub=None):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice đâu?")

        if sub is None:
            if self.loop[self.channel_id]['q'] == False:
                await ctx.send('Hiện queue loop đang **`Tắt\off`**')
            else:
                await ctx.send('Hiện queue loop đang **`Bật\on`**')
        else:
            if sub == 'on':
                await ctx.message.add_reaction('🔁')
                self.loop[self.channel_id]['q'] = True
                embed = discord.Embed(title='Bắt đầu loop!',
                                      colour=discord.Colour.purple())
                return await ctx.send(embed=embed)
            elif sub == 'off':
                await ctx.message.add_reaction('❌')
                self.loop[self.channel_id]['q'] = False
                embed = discord.Embed(title='Đã dừng loop!',
                                      colour=discord.Colour.dark_purple())
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Sai lệnh! Thử lại xem")

    @ commands.command(aliases=['nowplaying', 'n'])
    async def jnowplaying(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice đâu?")

        if not ctx.guild.voice_client.is_playing():
            return await ctx.send("Có đang play gì đâu?")

        await ctx.message.add_reaction('🆗')
        await ctx.send(
            f"Now playing: **`{self.current[self.channel_id]['s']}`** ({self.current[self.channel_id]['d']})"
        )

    @ commands.command(aliases=['search', 'f'])
    async def jsearch(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("Search gì mới được.")

        await ctx.message.add_reaction('🆗')
        await ctx.send("Đang tìm kiếm... mất một vài giây.")

        info = await self.search_song(5, song)

        embed = discord.Embed(
            title=f"Kết quả cho '{song}':",
            description="*Lấy link(url) trực tiếp từ tên bài hát nếu không phải là bài đầu tiên.*\n",
            colour=discord.Colour.red())

        amount = 0
        for entry in info['entries']:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"{amount} kết quả đầu tiên tìm được.")
        await ctx.send(embed=embed)

    @ commands.command(aliases=['skip', 'k'])
    async def jskip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Đã ở trong voice nào đâu?")

        if ctx.author.voice is None:
            return await ctx.send("Vào voice đi cái đã.")

        if not ctx.guild.voice_client.is_playing():
            return await ctx.send("Có đang play gì đâu mà skip?")

        await ctx.message.add_reaction('🆗')
        poll = discord.Embed(
            title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}",
            description="**__60%__ của voice channel đồng ý để skip.**",
            colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Vote kết thúc trong 10 giây.")

        poll_msg = await ctx.send(
            embed=poll
        )  # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no

        await asyncio.sleep(10)  # 10 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] +
                    votes[u"\U0001F6AB"]) > 0.59:  # 60% or higher
                skip = True
                embed = discord.Embed(
                    title="Skip ***Thành công***",
                    description="***Chuyển bài ngay bây giờ...***",
                    colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(
                title="Skip ***Thất bại***",
                description="***Cần ít nhất __60%__ phiếu đồng ý để skip.***",
                colour=discord.Colour.red())

        embed.set_footer(text="Vote kết thúc.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            self.loop[self.channel_id]['1'] = False
            await self.check_queue(ctx)

    @ commands.command(aliases=['queue', 'q'])
    async def jqueue(self, ctx):  # display the current guilds queue
        try:
            if len(self.song_queue[ctx.guild.id]) == 0 and self.current[
                    self.channel_id] == {}:
                return await ctx.send(
                    "Không có bài nào trong danh sách hiện tại cả.")
        except:
            return await ctx.send(
                "Không có bài nào trong danh sách hiện tại cả.")

        await ctx.message.add_reaction('🆗')

        end = '' if len(
            self.song_queue[ctx.guild.id]
        ) == 0 else '-  -  -  -  -  -  -  -  -  -  **NEXT**  -  -  -  -  -  -  -  -  -  -\n'

        embed = discord.Embed(
            title="**Danh sách phát**",
            description=f"**`Now playing`** 🔸 **[ [{self.current[self.channel_id]['s']}]({self.current[self.channel_id]['d']}) ]** 🔹\n{end}",
            colour=0x0dff00)

        i = 1
        for info in self.song_queue[ctx.guild.id]:
            embed.description += f"**{i}** > [{info['s']}]({info['d']})\n"
            i += 1

        embed.add_field(
            name='Lặp một bài ',
            value=f'{"**`Tắt/off`** ❌" if self.loop[self.channel_id]["1"] == False else "**`Bật/on`** 🔂"}',
            inline=True)
        embed.add_field(
            name=' Random',
            value=f'{"**`Tắt/off`** ❌" if self.loop[self.channel_id]["r"] == False else "**`Bật/on`** 🔀"}',
            inline=True)
        embed.add_field(
            name=' Lặp danh sách phát',
            value=f'{"**`Tắt/off`** ❌" if self.loop[self.channel_id]["q"] == False else "**`Bật/on`** 🔁"}',
            inline=True)
        embed.set_footer(
            text=f"Số lượng: [ {len(self.song_queue[ctx.guild.id])} ]")
        await ctx.send(embed=embed)

    @ commands.command(aliases=['clean_queue', 'cq'])
    async def jclean_queue(self, ctx, *, sub=None):
        if sub is None:
            embed = discord.Embed(
                title='Hướng dẫn dùng clean queue - xóa danh sách phát',
                description='',
                colour=discord.Color.blue())
            embed.description += '\n- **`cq all`**: xóa toàn bộ danh sách hiện tại'
            embed.description += '\n- **`cq [stt]`**: xóa bài hát cụ thể theo stt trong queue'
            embed.description += '\n- **`cq [3-7]`**: xóa các bài có stt trong khoảng từ 3 tới 7'
            embed.description += '\n- **`cq [2,3,9,...]`**: xóa các bài có stt 2, 3, 9,...'
            return await ctx.send(embed=embed)

        if not self.song_queue[ctx.guild.id]:
            return await ctx.send('Không có gì để xóa cả')

        await ctx.message.add_reaction('🆗')
        hyp = sub.find('-')  # doan
        com = sub.find(',')  # rieng le

        if sub == 'all':
            self.song_queue[ctx.guild.id].clear()
            self.previous[ctx.guild.id] = False
            return await ctx.send('Đã xóa toàn bộ thành công')

        elif hyp > 0:
            await self.hyphen(ctx, sub)
            return await ctx.send('Đã xóa đoạn thành công')

        elif com > 0:
            await self.comma(ctx, sub)
            return await ctx.send('Đã xóa các bài thành công')
        else:
            try:  # check có nhập đúng hay ko
                self.song_queue[ctx.guild.id].pop(
                    int(sub) - 1)  # pop ở đúng vị trí đó -1 vì list đi từ 0
                return await ctx.send('Đã xóa bài hát thành công')

            except:
                await ctx.send(
                    'Nhập cho đúng chứ. Lệnh **`help`** để biết thêm'
                )  # lỗi nhập chữ, không int đc,...

    @ commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.client.user.id:
            return
        elif before.channel is None:
            voice = after.channel.guild.voice_client
            while True:
                while True:
                    await asyncio.sleep(3)
                    if (voice.is_playing() is False) and (voice.is_paused() is True):
                        a = 0
                        for i in range(900):
                            await asyncio.sleep(1)
                            if voice.is_playing():
                                a = 1
                                break
                        if a == 1:
                            continue
                        else:
                            voice = after.channel.guild.voice_client
                            await voice.disconnect()
                            self.current[self.channel_id] = {}
                            break
                    elif (voice.is_playing() is False) and (voice.is_paused() is False):
                        await asyncio.sleep(2)
                        if self.loop[self.channel_id]['1'] == True:
                            await self.play_song(
                                member, self.current[self.channel_id])

                        elif len(self.song_queue[member.guild.id]) > 0:
                            await asyncio.sleep(3)
                            if voice.is_playing():
                                continue
                            await self.check_queue(member)

                        else:
                            await asyncio.sleep(3)
                            if voice.is_playing():
                                continue
                            if self.previous[member.guild.id]:
                                embed = discord.Embed(title='Đã phát bài cuối cùng - Danh sách phát trống!',
                                                      description='**` ;p [link or name]`**: để play | **` ;s [name]`**: để tìm thêm.', colour=discord.Color.dark_grey())
                                await self.client.get_channel(self.channel_id).send(embed=embed)
                                self.previous[member.guild.id] = False
                            self.current[self.channel_id] = {}
                            b = 0
                            for i in range(300):
                                await asyncio.sleep(1)
                                if len(self.song_queue[member.guild.id]
                                       ) > 0 or (voice.is_playing()):
                                    b = 1
                                    break
                            if b == 1:
                                continue
                            else:
                                await voice.disconnect()
                                break

                    if not voice.is_connected:
                        break
