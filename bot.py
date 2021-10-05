import os

# os.system("pip3 install discord")
# os.system("pip3 install requests")
# os.system("pip3 install pytz")
# os.system("pip3 install psutil")
# os.system("pip3 install GPUtil")
# os.system("pip3 install tabulate")
# os.system("pip3 install pillow")


import asyncio
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import requests
import json
from random import choice
from datetime import datetime
import pytz
import platform
import psutil
import GPUtil
from tabulate import tabulate
from PIL import Image, ImageChops, ImageFilter, ImageOps
#import textwrap
#import urllib
#import aiohttp
import topgg
import arting

#variables
intents = discord.Intents().all()
client = commands.Bot(command_prefix = "_", intents=intents)



def time():
    pst = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(pst)
    return timestamp

def exception_error(exception, location):
    e_data = open("log.txt", 'r').read()
    write_data = f"{time()} ~ [{location}]{exception}"
    print(write_data)
    new_data = f"{e_data}\n{write_data}"
    open("log.txt", 'w').write(new_data)

def get_meme():
    subred = ['SaimanSays', 'memes', 'india', 'IncredibleIndia', 'bakchodi', 'indianpeoplequora', 'unitedstatesofindia']

    link = [f'http://aio-api-discord.herokuapp.com/reddit/hot?subreddit={choice(subred)}']#, f'http://aio-api-discord.herokuapp.com/reddit/new?subreddit={choice(subred)}', f'http://aio-api-discord.herokuapp.com/reddit/random?subreddit={choice(subred)}']

    #RESPONSE = {"title":"","description":"","url":"*.jpg","post_url":"redd.it","author":"","score":182,"spoilers":true,"nsfw":false}

    try: 
        response = requests.get(choice(link))
        json_data = json.loads(response.text)
        title = json_data['title']
        description = json_data['description']
        url = json_data['url']
        post_url = json_data['post_url']
        author = json_data['author']
        votes = json_data['score']
        spoilers = json_data['spoilers']
        data = [title, description, url, post_url, author, votes, spoilers]

    # FORMAT = [title, description, url, post_url, author, votes, spoilers, nsfw]

    except Exception as e:
        exception_error(e, "Line 48, While fetching meme in def meme()")
        data = ['API Error', 'error', 'https://cdn.discordapp.com/attachments/795547584604143646/846637578233184256/PicsArt_05-03-10.png', 'https://cdn.discordapp.com/attachments/795547584604143646/846637578233184256/PicsArt_05-03-10.png', "Scam", "0", "True"]

    return data

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@tasks.loop(hours=24)
async def morning_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    quote_a = quote.translate({ord(i): None for i in '.'})
    author = json_data[0]['a']
    p_q = quote_a + " - " + author
    channel = client.get_channel(752904939029921915)
    await channel.send(f"> {p_q}\n\nGood Morning People")

@tasks.loop(minutes=30)
async def meme():
    channel = client.get_channel(858690426117816321)
    await channel.trigger_typing()
    data = get_meme()

    while data[0] == "API Error":
        exception_error("Recieved API Error", "Line 89, Task loop meme()")

        data = get_meme()

    print(data)
    myfile = requests.get(data[2])
    open("meme.png", 'wb').write(myfile.content)

    file = discord.File("meme.png")
    embed = discord.Embed(title = data[0], url = data[3], description = data[1])
    try:
        embed.set_image(url="attachment://meme.png")

    except Exception as e:
        exception_error(e, f"Line 89, Can't set image in meme's embed")

    embed.set_footer(text=f'Meme by {data[4]} | 👍 {data[5]}')
    await channel.send(embed=embed, file=file)

"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/attachments/795547584604143646/870700034163875860/0001-0250.mp4") as af:
            if 300 > af.status >= 200:
                fp = io.BytesIO(await af.read())
                file = discord.File(fp, f"horny.png")
                em = discord.Embed(title="Test", color=0xf1f1f1)
                em.set_image(url=f"attachment://horny.png")
                await channel.send(embed=em, file=file)
            else:
                await channel.send('')
        await session.close()


 PART 1
    print("ug")
    embed = discord.Embed(title = data[0], url = data[3], description = data[1])
    try:
        embed.set_image(url = data[2])

    except Exception as e:
        print(f"##{e}")

    await channel.send(embed = embed)
"""

@client.event
async def on_dbl_vote(data):
    print(data)

@client.event
async def on_connect():
    print("Lmao, just connected")

@client.event
async def on_disconnect():
    exception_error('Disconected', "Line 143 | on_disconnect()")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name = 'Only on this server, LMAO'))
    channel = client.get_channel(835206762936008745)  #Alaska-Log 835206762936008745

    uname = platform.uname()
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    embed = discord.Embed(title = "All Service are starting", description = "System Info:")
    embed.add_field(name = "OS Information", value = f"```ml\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}\n```", inline = False)
    embed.add_field(name = "Boot Time", value = f"```ml\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n```", inline = False)
    embed.add_field(name = "Memory Information", value = f"```ml\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}\nUsed: {get_size(svmem.used)}\nPercentage: {svmem.percent}\n```", inline = True)
    embed.add_field(name = "Swap Memory Information", value = f"```ml\nTotal: {get_size(swap.total)}\nAvailable: {get_size(swap.free)}\nUsed: {get_size(swap.used)}\nPercentage: {swap.percent}\n```", inline = True)
    embed.add_field(name = "CPU Information", value = f"```ml\nPhysical Cores: {psutil.cpu_count(logical=False)}\nTotal Cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {cpufreq.max:.2f} Mhz\nMin Frequency: {cpufreq.min:.2f} Mhz\nCurrent Frequency: {cpufreq.current:.2f} Mhz\nTotal CPU Usage: {psutil.cpu_percent()}%\n```", inline=False)
    embed.add_field(name = "Disk Information", value = f"```ml\nTotal read: {get_size(disk_io.read_bytes)}\nTotal write: {get_size(disk_io.write_bytes)}\n```", inline = True)
    embed.add_field(name = "Network Information", value = f"```ml\nTotal Bytes sent: {get_size(net_io.bytes_sent)}\nTotal Bytes recieved: {get_size(net_io.bytes_recv)}\n```", inline = True)

    await channel.send(embed=embed)
    print(f'We have logged in as {client.user}')

@client.event
async def on_message_delete(message):
    channel = client.get_channel(835206762936008745)
    embed = discord.Embed(title = 'Message Deleted', description = f"A message from <@{message.author.id}>[{message.author}] in <#{message.channel.id}>[{message.channel}] was deleted\n\nMessage:\n```ml\n{message.content}\n```")
    await channel.send(embed = embed)

@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(835206762936008745)
    embed = discord.Embed(title = "Message Edited", description = f"A Message from {before.author.mention}[{before.author}] has been edited in {before.channel.mention}[{before.channel}]")
    embed.add_field(name = "Before", value = f"```ml\n{before.content}\n```")
    embed.add_field(name = "After", value = f"```ml\n{after.content}\n```")
    await channel.send(embed = embed)

@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_command_error(ctx, error):
    exception_error(error, f"{ctx} | Line 120, on_command_error() -> {error}")


@client.command()
@has_permissions(administrator=True)
async def start(ctx, component : int):
    if component == 1:
        morning_quote.start()

    elif component == 2:
        meme.start()

    else:
        await ctx.trigger_typing()
        await ctx.send("Its been a long day")
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("without you, my friend")
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send("And I'll tell you all about it when I see you again")
        await ctx.trigger_typing()
        await asyncio.sleep(3)
        await ctx.send("We've come a long way from where we began.......")
        await ctx.trigger_typing()
        await asyncio.sleep(3)
        await ctx.send("Oh, I'll tell you all about it when I see you again")
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send("When I see you again")
        await ctx.send("Don't dm for full song")

@start.error
async def start_error(ctx, error):
    exception_error(error, f"{ctx} | Line 133, start_error() -> {error}")
    
    if isinstance(error, commands.CheckFailure):
        await ctx.trigger_typing()
        await ctx.send("Fly like an eagle")
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send("Even if I do it very legal")
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send("Flyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send(",...............................")

@client.command(aliases=["sd"])
@has_permissions(administrator=True)
async def send_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

@send_dm.error
async def send_dm_error(ctx, error):
    exception_error(error, f"{ctx} | Line 133, start_error() -> {error}")
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"lmfao, i don't work for stupid people like {ctx.author.mention}")

@client.command(aliases=["si", "sysinfo"])
async def system_info(ctx, embed : bool = True):
    uname = platform.uname()
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    partitions = psutil.disk_partitions()
    disk_io = psutil.disk_io_counters()
    if_addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()
    if embed:
        embed = discord.Embed(title = "All Services are running", description = "System Info:")
        embed.add_field(name = "OS Information", value = f"```ml\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}\n```", inline = False)
        embed.add_field(name = "Boot Time", value = f"```ml\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n```", inline = False)
        embed.add_field(name = "Memory Information", value = f"```ml\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}\nUsed: {get_size(svmem.used)}\nPercentage: {svmem.percent}\n```", inline = True)
        embed.add_field(name = "Swap Memory Information", value = f"```ml\nTotal: {get_size(swap.total)}\nAvailable: {get_size(swap.free)}\nUsed: {get_size(swap.used)}\nPercentage: {swap.percent}\n```", inline = True)
        embed.add_field(name = "CPU Information", value = f"```ml\nPhysical Cores: {psutil.cpu_count(logical=False)}\nTotal Cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {cpufreq.max:.2f} Mhz\nMin Frequency: {cpufreq.min:.2f} Mhz\nCurrent Frequency: {cpufreq.current:.2f} Mhz\nTotal CPU Usage: {psutil.cpu_percent()}%\n```", inline=False)
        embed.add_field(name = "Disk Information", value = f"```ml\nTotal read: {get_size(disk_io.read_bytes)}\nTotal write: {get_size(disk_io.write_bytes)}\n```", inline = True)
        embed.add_field(name = "Network Information", value = f"```ml\nTotal Bytes sent: {get_size(net_io.bytes_sent)}\nTotal Bytes recieved: {get_size(net_io.bytes_recv)}\n```", inline = True)
        await ctx.send(embed = embed)        

    elif embed == False:
        if ctx.author.id == 720308779220074557 or ctx.author.id == 745849641395814521:
            await ctx.send(f"__**OS Information**__\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}")

            await ctx.send(f"__**Boot Information**__\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

            await ctx.send(f"__**CPU Information**__\nPhysical Cores: {psutil.cpu_count(logical=False)}\nTotal Cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {cpufreq.max:.2f} Mhz\nMin Frequency: {cpufreq.min:.2f} Mhz\nCurrent Frequency: {cpufreq.current:.2f} Mhz")
            await ctx.send("CPU Usage Per Core:")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                await ctx.send(f"Core {i}: {percentage}%")
            await ctx.send(f"Total CPU Usage: {psutil.cpu_percent()}%")

            await ctx.send(f'__**Memory Information**__\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}\nUsed: {get_size(svmem.used)}\nPercentage: {svmem.percent}')

            await ctx.send(f'__**Swap Information**__\nTotal: {get_size(swap.total)}\nAvailable: {get_size(swap.free)}\nUsed: {get_size(swap.used)}\nPercentage: {swap.percent}')

            await ctx.send("__**Disk Information**__")
            for partition in partitions:
                await ctx.send(f"=== Device: {partition.device} ===")
                await ctx.send(f"  Mountpoint: {partition.mountpoint}")
                await ctx.send(f"  File system type: {partition.fstype}")

                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    continue

                await ctx.send(f"  Total Size: {get_size(partition_usage.total)}")
                await ctx.send(f"  Used: {get_size(partition_usage.used)}")
                await ctx.send(f"  Free: {get_size(partition_usage.free)}")
                await ctx.send(f"  Percentage: {partition_usage.percent}%")
            await ctx.send(f"Total read: {get_size(disk_io.read_bytes)}\nTotal write: {get_size(disk_io.write_bytes)}")

            await ctx.send(f"__**Network Information**__")
            for interface_name, interface_addresses in if_addrs.items():
                for address in interface_addresses:
                    await ctx.send(f"=== Interface: {interface_name} ===")
                    if str(address.family) == 'AddressFamily.AF_INET':
                        await ctx.send(f"  IP Address: {address.address}")
                        await ctx.send(f"  Netmask: {address.netmask}")
                        await ctx.send(f"  Broadcast IP: {address.broadcast}")
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        await ctx.send(f"  MAC Address: {address.address}")
                        await ctx.send(f"  Netmask: {address.netmask}")
                        await ctx.send(f"  Broadcast MAC: {address.broadcast}")
            await ctx.send(f"Total Bytes sent: {get_size(net_io.bytes_sent)}\nTotal Bytes recieved: {get_size(net_io.bytes_recv)}")

            await ctx.send('__**GPU Information**__')
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
    # get the GPU id
                gpu_id = gpu.id
    # name of GPU
                gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
                gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
                gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
                gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
                gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))

            await ctx.send(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")))

'''
@client.command(aliases = ['l', 'lyrc', 'lyric']) # adding aliases to the command so they they can be triggered with other names
async def lyrics(ctx, *, search = None):
    """A command to find lyrics easily!"""
    if not search: # if user hasnt given an argument, throw a error and come out of the command
        embed = discord.Embed(
            title = "No search argument!",
            description = "You havent entered anything, so i couldnt find lyrics!"
        )
        return await ctx.reply(embed = embed)
        # ctx.reply is available only on discord.py version 1.6.0, if you have a version lower than that use ctx.send
    
    song = urllib.parse.quote(search) # url-encode the song provided so it can be passed on to the API
    
    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata: # define jsondata and fetch from API
            if not 300 > jsondata.status >= 200: # if an unexpected HTTP status code is recieved from the website, throw an error and come out of the command
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')

            lyricsData = await jsondata.json() # load the json data into its json form

    error = lyricsData.get('error')
    if error: # checking if there is an error recieved by the API, and if there is then throwing an error message and returning out of the command
        return await ctx.send(f'Recieved unexpected error: {error}')

    songLyrics = lyricsData['lyrics'] # the lyrics
    songArtist = lyricsData['author'] # the author's name
    songTitle = lyricsData['title'] # the song's title
    songThumbnail = lyricsData['thumbnail']['genius'] # the song's picture/thumbnail

    # sometimes the song's lyrics can be above 4096 characters, and if it is then we will not be able to send it in one single message on Discord due to the character limit
    # this is why we split the song into chunks of 4096 characters and send each part individually
    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace = False):
        embed = discord.Embed(
            title = songTitle,
            description = chunk,
            color = discord.Color.blurple(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url = songThumbnail)
        await ctx.send(embed = embed)'''

@client.command(aliases=["pixel", 'p'])
async def pixelify(ctx, *,  member : commands.MemberConverter=None):
    if member == None:
        member = ctx.author

    myfile = requests.get(member.avatar_url)
    open("avatar.png", 'wb').write(myfile.content)

    avatar = Image.open('avatar.png')
    pixeled = avatar.convert("1")
    pixeled.save('avatar.png')

    await ctx.send(file=discord.File('avatar.png'))

@client.command()
async def invert(ctx, *,  member : commands.MemberConverter=None):
    if member == None:
        member = ctx.author

    myfile = requests.get(member.avatar_url_as(format='png'))
    open("avatar.png", 'wb').write(myfile.content)

    ava = Image.open('avatar.png')
    avatar = ava.convert("RGB")
    invert = ImageOps.invert(avatar)
    
    invert.save('invert.png')

    await ctx.send(file=discord.File('invert.png'))

@client.command()
async def blur(ctx, *,  member : commands.MemberConverter=None):
    if member == None:
        member = ctx.author

    myfile = requests.get(member.avatar_url_as(format='png'))
    open("avatar.png", 'wb').write(myfile.content)

    ava = Image.open('avatar.png')
    avatar = ava.convert("RGB")
    blur = avatar.filter(ImageFilter.GaussianBlur(radius=10))
    blur.save('blur.png')

    await ctx.send(file=discord.File('blur.png'))

@client.command()
async def ascii(ctx, *,  member : commands.MemberConverter=None):
    if member == None:
        member = ctx.author

    myfile = requests.get(member.avatar_url_as(format='png'))
    open("avatar.png", 'wb').write(myfile.content)

    arting.main()

    location = 'ascii.txt'
    ascii = open(location, 'r').read()
    myobj = {'api_dev_key': 'PI2u64XcoQ_BtZtBDsFTJ_P6F_cU1TlC', 'api_paste_code': ascii, 'api_paste_private': '0', 'api_paste_name': 'ascii.txt', 'api_option': 'paste', 'api_paste_expire_date': '1D'}
    x = requests.post('https://pastebin.com/api/api_post.php', data = myobj)

    await ctx.send(x.text, file=discord.File('drawn_image.jpg'))


@client.event
async def on_message(m):
    if m.author == client.user:
        return

    if isinstance(m.channel, discord.channel.DMChannel):
        channel = client.get_channel(815283467817975818)
        embed = discord.Embed(title = "DM", description = f"Just recieved a dm from {m.author.mention}[{m.author}]:\n```ml\n{m.content}\n```")
        await channel.send(embed = embed)

    ms = m.content.lower()
    words = ['fuck', 'dick', 'shit', 'bastard', 'dickhead', 'asshole', 'penis', 'vagina', 'chut', 'maa ka chut', 'gand ', 'dead chat', 'dead server', 'ded chat', 'ded server', 'bitch', 'n word']
    
    for word in words:
        if word in ms:
            if m.author.id != 720308779220074557:
                if m.author.id != 745849641395814521:
                    await m.channel.trigger_typing()
                    await m.delete()
                    await m.channel.send(f"Holy frick, stop abusing {m.author.mention}")
                    non = m.content.replace(word, "")
                    if non != "":
                        await m.channel.send(f"Sentence without abuse\n```ml\n{non}\n```")

    if m.channel.id == 861241740043485244:
        channel = client.get_channel(838479073675444264)
        await channel.send(f'Achievement:\n{m.content}')

    if m.channel.id == 829382807872077914:
        id = m.author.id
        response = requests.get(f'http://api.brainshop.ai/get?bid=159075&key=Ujc9sNl9ylej6yKA&uid={id}&msg={m.content}')
        json_data = json.loads(response.text)
        msg = json_data['cnt']
        await m.reply(msg)

    if m.channel.id == 847159488586842152:
        msg = m.content
        auth = m.author
        id = m.author.id
        await m.delete()

        channel = client.get_channel(860575836592013322)
        await channel.send(f'Message from {auth} in <#847159488586842152>\n```ml\n{msg}\n```')

        cha = client.get_channel(752904939029921915)
        await cha.send(f'<@{id}> Your application has been successfully submitted')

    if m.channel.id == 836302732876578836:
        msg = m.content
        auth = m.author
        id = m.author.id
        await m.delete()

        channel = client.get_channel(860575836592013322)
        await channel.send(f'Message from {auth} in <#836302732876578836>\n```ml\n{msg}\n```')

        cha = client.get_channel(752904939029921915)
        await cha.send(f'<@{id}> Your application has been successfully submitted')

    if m.channel.id == 862007739291140158:
        msg = m.content
        auth = m.author
        id = m.author.id
        await m.delete()

        channel = client.get_channel(860575836592013322)
        await channel.send(f'Message from {auth} in <#862007739291140158>\n```ml\n{msg}\n```')

        cha = client.get_channel(752904939029921915)
        await cha.send(f'<@{id}> Your verification has been successfully submitted, you will get notified if you get verified')

    if (m.channel.id == 816185865633005590) or (m.channel.id == 853546769265721396):
        await m.add_reaction('⬆️')
        await m.add_reaction('⬇️')

    await client.process_commands(m)

client.run('NzkzMDkxNjk3ODI3MTE5MTM0.X-nOMw.0Hw7xiD8ae0v7kU0b6o3amLcFkw')