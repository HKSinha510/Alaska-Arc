import os

try:
    import asyncio
    import discord
    from discord import app_commands
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
    from PIL import Image
    from art import generate_art

except ImportError:
    print("Import failed, intalling modules")
    os.system("pip3 install discord")
    os.system("pip3 install requests")
    os.system("pip3 install pytz")
    os.system("pip3 install psutil")
    os.system("pip3 install GPUtil")
    os.system("pip3 install tabulate")
    os.system("pip3 install Pillow")

else:
    print("try out, except out, else in")


#variables
intents = discord.Intents().all()
client = commands.Bot(command_prefix = "_", intents=intents)
#tree = app_commands.CommandTree(client)
words = ['fuck', 'dick', 'shit', 'bastard', 'dickhead', 'asshole', 'penis', 'vagina', 'chut', 'maa ka chut', 'gand ', 'dead chat', 'dead server', 'ded chat', 'ded server', 'bitch', 'n word', 'harami', 'kutta', 'kutte']


def time():
    pst = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(pst)
    return timestamp

def exception_error(exception, location):
    print(exception)

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

def average_color(img):
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0
 
    count = 0
 
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (r_total/count, g_total/count, b_total/count)

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
    #await channel.trigger_typing()

    subReddit = ['SaimanSays', 'memes', 'bakchodi', 'IndianDankMemes', 'me_irl', 'meme', "unexpected", "meme", "memes", "CarryMinati", "dankinindia", "desimemes"]

    link = f'https://meme-api.com/gimme/{choice(subReddit)}'

    response = requests.get(link)
    json_data = json.loads(response.text)
    title = json_data['title']
    #description = json_data['description']
    url = json_data['url']
    postLink = json_data['postLink']
    author = json_data['author']
    votes = json_data['ups']

    #print(data)
    myfile = requests.get(url)
    extension = url[-3:]
    open(f"meme.{extension}", 'wb').write(myfile.content)

    file = discord.File(f"meme.{extension}")

    img = Image.open(f"meme.{extension}")
    img = img.convert('RGB')
    r, g, b = average_color(img)
    
    embed = discord.Embed(title = title, url = postLink, description = "** **", color = discord.Color.from_rgb(int(r), int(g), int(b)))
    try:
        embed.set_image(url=f"attachment://meme.{extension}")

    except Exception as e:
        exception_error(e, f"Line 89, Can't set image in meme's embed")

    embed.set_footer(text=f'Meme by {author} | 👍 {votes}')
    await channel.send(embed=embed, file=file)

@tasks.loop(hours=1)
async def edit_message():
    channel = client.get_channel(853545849261916181)
    msg_id = 895290072600035360
    msg = await channel.fetch_message(msg_id)
    guild = client.get_guild(853536444278767626)
    nevada = guild.get_member(797066760229617697)
    nevada_premium = guild.get_member(896093862207049750)
    berlin = guild.get_member(854406530576023604)
    await msg.edit(content=f'__Status__\nNevada: {str(nevada.status).title()}\nNevada Premium: {str(nevada_premium.status).title()}\nAlaska: Me always online, never offline\nBerlin: {str(berlin.status).title()}')

@client.event
async def on_connect():
    print("Lmao, just connected")

@client.event
async def on_disconnect():
    exception_error('Disconected', "Line 143 | on_disconnect()")

@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity=discord.Game(name = 'Painting'))
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
    edit_message.start()

@client.event
async def on_message_delete(message):
    channel = client.get_channel(835206762936008745)
    embed = discord.Embed(title = 'Message Deleted', description = f"A message from <@{message.author.id}>[{message.author}] in <#{message.channel.id}>[{message.channel}] was deleted\n\nMessage:\n```ml\n{message.content}\n```")
    await channel.send(embed = embed)

@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(835206762936008745)

    for word in words:
        if word in after.content.lower():
            if after.author.id != 720308779220074557:
                if after.author.id != 745849641395814521:
                    #await after.channel.()
                    await after.delete()
                    await after.channel.send(f"Holy frick, stop abusing {after.author.mention}")
                    non = after.content.replace(word, "")
                    if non != "":
                        await after.channel.send(f"Sentence without abuse\n```ml\n{non}\n```")

    a = after.content
    b = before.content

    embed = discord.Embed(title = "Message Edited", description = f"A Message from {before.author.mention}[{before.author}] has been edited in {before.channel.mention}[{before.channel}]")
    embed.add_field(name = "Before", value = f"```ml\n{b}\n```")
    embed.add_field(name = "After", value = f"```ml\n{a}\n```")
    takeOne = a.replace(b, "")
    takeTwo = b.replace(a, "")
    print(takeOne)
    print(takeTwo) 
    if takeOne == a:
        rep = takeTwo

    elif takeTwo == b:
        rep = takeOne

    else:
        rep = takeOne

    if rep != "":
        embed.add_field(name = "Difference", value = f"```ml\n{rep}\n```", inline=False)
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

@client.command()
@has_permissions(administrator=True)
async def ban(ctx, member: commands.MemberConverter, *, reason = ""):
    await member.ban(reason = reason)
    await ctx.send(f"<@{member.id}> has been banned by {ctx.author.mention}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("No ||s||perms")

@client.command()
@has_permissions(administrator=True)
async def kick(ctx, member: commands.MemberConverter, *, reason = ""):
    await ctx.send("lockdown hai, kick kidhar karega?")

@client.command(aliases=["sd"])
@has_permissions(administrator=True)
async def send_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)
    await ctx.add_reaction("✅")

@send_dm.error
async def send_dm_error(ctx, error):
    exception_error(error, f"{ctx} | Line 133, start_error() -> {error}")
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"They talk to each other while driving")

#SLASH COMMAND 🤯
@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def addition(interaction: discord.Interaction, first_value: float, second_value: float):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

@client.tree.command(guild=discord.Object(id='752904939029921912'))
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

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

@client.command(
    aliases=["sm", "send"]
)
@has_permissions(administrator=True)
async def send_message(ctx, channel: commands.TextChannelConverter, *, message):
    print(channel)
    #channel = client.get_channel(channel.id)
    await channel.send(message)

@client.command(
    aliases = ["ext", "info"]
)
@commands.cooldown(2, 60, commands.BucketType.user)
async def extension(ctx):
    try:
        msg = ""
        response = requests.get("http://hksinha.webhop.me:8800/systeminfo", timeout=5)
        json_data = json.loads(response.text)
        for key, value in json_data.items():
            msg += f"{key}: {value}\n"

    except Exception as e:
        exception_error(e, "extension, ln 441")
        msg = "Offline"
        
    await ctx.send(msg)

@client.command(
    aliases = ["ca"]
)
@has_permissions(administrator=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def change_activity(ctx, *, activity):
    await client.change_presence(activity=discord.Game(name = activity))
    await ctx.add_reaction("✅")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def art(ctx):
    generate_art()
    await ctx.send(file=discord.File('Final.png'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}Sec')

@client.event
async def on_message(m):
    if m.author == client.user:
        return

    if m.author.bot:
        return

    if isinstance(m.channel, discord.channel.DMChannel):
        channel = client.get_channel(815283467817975818)
        embed = discord.Embed(title = "DM", description = f"Just recieved a dm from {m.author.mention}[{m.author}]:\n```ml\n{m.content}\n```")
        await channel.send(embed = embed)

    ms = m.content.lower()
    
    for word in words:
        if word in ms:
            if m.author.id != 720308779220074557:
                if m.author.id != 745849641395814521:
                    #await m.channel.trigger_typing()
                    await m.delete()
                    await m.channel.send(f"Holy frick, stop abusing {m.author.mention}")
                    non = m.content.replace(word, "")
                    if non != "":
                        await m.channel.send(f"Sentence without abuse\n```ml\n{non}\n```")

    if m.content.lower() == '!d bump':
        await asyncio.sleep(7200)
        #channel = client.get_channel(860573666974761030)
        await m.channel.send("<@&795538188655394817>\nTime for a bump\nPls write `!d bump`")
        #bump_reminder.start()

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

client.run('my-bot-token')
