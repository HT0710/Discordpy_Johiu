import discord
import os
from discord.ext import commands
from cogs.music import Music

client = commands.Bot(command_prefix=';',
                      intents=discord.Intents.all(),
                      help_command=None)


@client.event
async def on_ready():
    print('{0.user} vừa du hành vào sever'.format(client))
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name='🎵 | ;help'))


@client.listen()
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(
            "Ông trùm Johíu thích nghe nhạc\n**`;help`**: để biết thêm thông tin"
        )


"""
Các chức năng đang có hiện tại

Events:
    on_ready
    on_member_join
    on_member_out
    on_voice_state_update/Feature/Music

Commands:
    new > (new)
    help > (help, h)
    info > (info, if)
    nickname > (nickname, nn)
    
API:
    weather > (weather, wt)
    dog > (dog)
    cat > (cat)
    
Feature:
    music:
        play > (play, p)
        force play > (fplay, fp)
        pause > (pause, s)
        resume > (resume, r)
        leave > (leave, l)
        skip > (skip, k)
        nowplaying > (nowplaying, n)
        loop > (loop, o)
        qloop > (qloop, qo)
        search > (search, f)
        queue > (queue, q)
        clean queue > (cqueue, cq)
        *** Note
            # Auto join khi play
            # Auto thêm vào queue nếu đang play
            # Auto leave sau 10 phút nếu tạm dừng (pause) và 5 phút nếu dừng(stop)
        ***
            
"""

initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename == ('music.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


async def setup():
    await client.wait_until_ready()
    client.add_cog(Music(client))


client.loop.create_task(setup())
client.run(os.environ['TOKEN'])
# https://discord.com/api/oauth2/authorize?client_id=912789977153282109&permissions=8&scope=bot
