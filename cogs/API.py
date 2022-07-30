import asyncio
import discord
from discord.ext import commands
import requests
import json
import datetime
from tinydb import TinyDB, Query

client = commands.Bot(command_prefix=';', intents=discord.Intents.all(), help_command=None)

db = TinyDB('cogs/wtlist.json')
User = Query()


class API(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wtdata = {
            'main': {
                'Rain': 'Có mưa',
                'Thunderstorm': 'Mưa dông',
                'Drizzle': 'Mưa phùn',
                'Clouds': 'Có mây',
                'Snow': 'Có tuyết',
                'Mist': 'Sương mỏng',
                'Smoke': 'Sương khói',
                'Haze': 'Sương bụi',
                'Dust': 'Bụi',
                'Fog': 'Sương mù',
                'Sand': 'Cát',
                'Ash': 'Tro',
                'Squall': 'Mưa đá',
                'Tornado': 'Lốc xoáy',
                'Clear': 'Trời đẹp',
            },

            'description': {
                'thunderstorm with light rain': 'Giông bão có mưa nhẹ',
                'thunderstorm with rain': 'Giông bão có mưa',
                'thunderstorm with heavy rain': 'Giông bão có mưa nặng hạt',
                'light thunderstorm': 'Giông bão nhẹ',
                'thunderstorm': 'Dông',
                'heavy thunderstorm': 'Giông bão lớn',
                'ragged thunderstorm': 'Giông bão',
                'thunderstorm with light drizzle': 'Giông bão với mưa phùn nhẹ',
                'thunderstorm with drizzle': 'Giông bão với mưa phùn',
                'thunderstorm with heavy drizzle': 'Giông bão với mưa phùn lớn',

                'light intensity drizzle': 'Mưa phùn nhẹ',
                'light intensity drizzle rain': 'Mưa phùn nhẹ',
                'heavy intensity drizzle': 'Mưa phùn lớn',
                'drizzle': 'Mưa phùn',
                'drizzle rain': 'Mưa phùn',
                'heavy intensity drizzle rain': 'Mưa phùn lớn',
                'shower rain and drizzle': 'Mưa rào và mưa phùn',
                'heavy shower rain and drizzle': 'Mưa rào và mưa phùn lớn',
                'shower drizzle': 'Mưa phùn vừa',

                'rain and drizzle': 'Mưa bụi và mưa phùn',

                'light rain': 'Mưa nhẹ',
                'moderate rain': 'Mưa vừa',
                'heavy intensity rain': 'Mưa nặng hạt',
                'very heavy rain': 'Mưa rất lớn',
                'extreme rain': 'Mưa cực lớn',
                'freezing rain': 'Mưa tuyết',
                'light intensity shower rain': 'Mưa rào nhẹ',
                'shower rain': 'Mưa rào',
                'heavy intensity shower rain': 'Mưa rào lớn',
                'ragged shower rain	': 'Mưa rào theo đợt',

                'clear sky': 'Trời không mây',
                'few clouds': 'Ít mây',
                'scattered clouds': 'Mây rải rác',
                'broken clouds': 'Mây thưa thớt',
                'overcast clouds': 'Mây u ám',
            }

        }
        self.day_info = {}

    async def get_time(self, time):
        url2 = f'https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp={time}'
        get = requests.get(url2)
        data = json.loads(get.text)

        return data

    async def get_current_weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather?id=1566083&appid=d13bb2aaa7a539db226d1fc9109fb387'
        get = requests.get(url)
        data = json.loads(get.text)

        return data

    async def get_daily_weather(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=10.8327836&lon=106.6062948&exclude=minutely,hourly,current&appid=d13bb2aaa7a539db226d1fc9109fb387'
        get = requests.get(url)
        data = json.loads(get.text)

        return data

    async def get_dog(self):
        url = 'https://dog.ceo/api/breeds/image/random'
        request = requests.get(url)
        data = json.loads(request.text)

        return data

    async def get_cat(self):
        url = 'https://api.thecatapi.com/v1/images/search'
        request = requests.get(url)
        data = json.loads(request.text)

        return data

    async def get_fng(self):
        url = 'https://api.alternative.me/fng/?limit=1'
        request = requests.get(url)
        data = json.loads(request.text)

        return data

    async def get_day_info(self, day):
        get = await self.get_daily_weather()
        daily = get['daily'][day]

        await asyncio.sleep(1)
        time = await self.get_time(daily['dt'])
        date_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        today = date_time.strftime('%d/%m')

        await asyncio.sleep(2)
        rise1 = await self.get_time(daily['sunrise'])
        rise2 = rise1.split(' ')[1].split(':')
        sunrise = f'{str(int(rise2[0]) - 17)}:{rise2[1]}'

        await asyncio.sleep(2)
        set1 = await self.get_time(daily['sunset'])
        set2 = set1.split(' ')[1].split(':')
        sunset = f'{str(int(set2[0]) + 7)}:{set2[1]}'

        for data in self.wtdata['main']:
            if data == daily['weather'][0]['main']:
                main = self.wtdata['main'][data]

        for data in self.wtdata['description']:
            if data == daily['weather'][0]['description']:
                description = self.wtdata['description'][data]

        self.day_info['day'] = today
        self.day_info['detail'] = {}
        add = self.day_info['detail']

        icon = daily['weather'][0]['icon']
        iurl = f'http://openweathermap.org/img/wn/{icon}@2x.png'
        add['icon'] = iurl
        add['main'] = main
        add['description'] = description
        add['temp'] = str(round(daily['temp']['eve'] - 273.15)) + '°C'
        add['uvi'] = daily['uvi']
        add['humidity'] = str(daily['humidity']) + '%'
        add['wind_speed'] = str(round(float(daily['wind_speed']) * 3.6, 2)) + 'km/h'
        add['sunrise'] = sunrise
        add['sunset'] = sunset
        add['moon_phase'] = daily['moon_phase']

    async def check_wtlist(self):
        get_today = datetime.datetime.today()
        today = get_today.strftime('%d/%m')

        # check nếu ngày hôm nay vượt quá 5 ngày lưu trong list
        # loại bỏ toàn bộ cái cũ
        # chạy từ đầu, thêm 5 ngày tính từ hôm nay
        if db.search(User['day'] == today) == []:

            db.truncate()  # xóa toàn bộ

            for i in range(0, 5):  # thêm từ đầu tới 4 (wtinfo chạy từ 0)
                await self.get_day_info(i)
                db.insert(self.day_info)

        # còn nếu ngày hôm nay còn trong 5 ngày lưu trước đó thì lấy id ngày cuối trừ id hôm nay ra được số ngày đã có
        # sau đó chỉ loại bỏ các ngày trước đó
        # thêm số ngày còn thiếu
        else:
            for i in range(0, 5):
                if db.all()[i]['day'] == today:
                    order = i + 1

            available = 5 - order + 1  # số ngày đã có
            final = 5 - available  # số ngày cần xóa và cần thêm

            remove = []  # trữ những id cần xóa
            for i in range(final):  # xóa từ đầu tới final
                remove.append(i + 1)  # id bắt đầu từ 1 nên +1 vào (range chạy từ 0)
            db.remove(doc_ids=remove)  # xóa các id đó

            for i in range(available, 5):  # thêm từ số ngày đã có VD: đã có 3 thì thêm 3 4 (wtinfo chạy từ 0)
                await self.get_day_info(i)
                db.insert(self.day_info)

    @commands.command(aliases=['weather', 'wt'])
    async def jweather(self, ctx, sub=None):
        if sub is not None:
            if sub == 'daily':
                await ctx.send('Vài giây...', delete_after=10)
                await self.check_wtlist()
                embed = discord.Embed(title='Thời tiết tp.HCM >**5**< ngày từ hôm nay', colour=discord.Color.blue())
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                await asyncio.sleep(0.5)

                for i in range(5):
                    day = db.all()[i]
                    detail = day['detail']

                    embed = discord.Embed(title=f"Ngày: **`{day['day']}`**", colour=0xB5F4FF)
                    fields = [
                        ('**Chính**', detail['main'], True),
                        ('**Mô tả**', detail['description'], True),
                        ('**Nhiệt độ trung brình**', detail['temp'], True),
                        ('**Tia UV**', detail['uvi'], True),
                        ('**Độ ẩm**', detail['humidity'], True),
                        ('**Sức gió**', detail['wind_speed'], True),
                        ('**Mặt trời mọc**', detail['sunrise'], True),
                        ('**Mặt trời lặn**', detail['sunset'], True),
                        ('**Chu kì trăng**', detail['moon_phase'], True),
                    ]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    embed.set_thumbnail(url=detail['icon'])

                    await ctx.send(embed=embed)
                    await asyncio.sleep(0.5)

                return
            else:
                embed = discord.Embed(title='Hướng dẫn dùng Weather',
                                      description='- Prefix: **`;`**',
                                      colour=discord.Color.blue())
                embed.description += '\n- **`wt`**: thời tiết hiện tại'
                embed.description += '\n- **`wt daily`**: dự báo thời tiết 5 ngày từ hôm nay'

                return await ctx.send(embed=embed)
        else:
            get = await self.get_current_weather()

            embed = discord.Embed(title='Thời tiết **tp.HCM** hiện tại', colour=0xB5F4FF)

            main = get['weather'][0]['main']
            description = get['weather'][0]['description']
            icon = get['weather'][0]['icon']
            iurl = f'http://openweathermap.org/img/wn/{icon}@2x.png'
            temp = str(round(get['main']['temp'] - 273.15)) + '°C'
            humidity = str(get['main']['humidity']) + '%'
            visibility = str(round(float(get['visibility']) / 1000)) + 'km'
            wind_speed = str(round(float(get['wind']['speed']) * 3.6, 2)) + 'km/h'

            for data in self.wtdata['main']:
                if data == main:
                    main = self.wtdata['main'][data]

            for data in self.wtdata['description']:
                if data == description:
                    description = self.wtdata['description'][data]

            fields = [
                ('Chính', main, True),
                ('Mô tả', description, True),
                ('Nhiệt độ', temp, True),
                ('Độ ẩm', humidity, True),
                ('Tầm nhìn', visibility, True),
                ('Sức gió', wind_speed, True)
            ]

            embed.set_thumbnail(url=iurl)
            embed.timestamp = datetime.datetime.utcnow()

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

    @commands.command(aliases=['dog'])
    async def jdog(self, ctx):

        get = await self.get_dog()
        embed = discord.Embed(title='Random Dog Picture', colour=discord.Colour.random())
        embed.set_image(url=get['message'])
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.command(aliases=['cat'])
    async def jcat(self, ctx):

        get = await self.get_cat()
        embed = discord.Embed(title='Random Cat Picture', colour=discord.Colour.random())
        embed.set_image(url=get[0]['url'])
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.command(aliases=['fng'])
    async def jfng(self, ctx):
        await asyncio.sleep(5)
        get = await self.get_fng()
        index = get['data'][0]['value']
        time = float(get['data'][0]["time_until_update"])
        time = datetime.datetime.utcfromtimestamp(time).strftime('%Hh %Mm %Ss')
        des = color = get['data'][0]['value_classification']
        if color == 'Too Greedy':
            color = discord.Color.dark_green()
        elif color == 'Greedy':
            color = discord.Color.green()
        elif color == 'Neutral':
            color = discord.Color.gold()
        elif color == 'Fear':
            color = discord.Color.orange()
        elif color == 'Extreme Fear':
            color = discord.Color.red()
        else:
            color = discord.Color.dark_gray

        embed = discord.Embed(title='Feer & Greed', description=f"**{index} - {des}**", color=color)
        embed.set_image(url='https://alternative.me/crypto/fear-and-greed-index.png')
        embed.set_footer(text=f"Until next update:  {time}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(API(client))
