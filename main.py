import discord
from discord.ext import commands
import pytz
from datetime import datetime

client = commands.Bot(command_prefix = "_")

def time():
    timestamp = datetime.now()
    pst = pytz.timezone('Asia/Kolkata')
    t1 = timestamp.astimezone(pst).strftime("%I:%M %p")
    return t1

def meme(subreddit):
    title = "hey"
    image = "https"
    return [title, image]

def quote():
    quote = "one day"
    msg = "Gm"
    return [quote, msg]

@client.event
async def on_ready():
    print('Ok')

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def start(ctx, component):
    try:
        component = int(component)
        avaiable_commands = (1, 2)
        sub = "google"
        task = [meme(sub), quote()]
        id = [865883985757863957, 865883985757863957]

        if avaiable_commands in component:
            channel = client.get_channel(id[component - 1])
            
            channel.send(task[component - 1][0])
            channel.send(task[component - 1][1])

    except Exception:
        print(Exception.text)
        channel = client.get_channel(865883985757863957)
        await channel.send(f"INT convert error, {component} has been passed\nMessage from {ctx.author} at {time()}")

@client.command()
async def timezone(ctx):
    a = ""
    b = "\n"
    for tz in pytz.all_timezones:
        a += tz + b

    for chunk in [a[i:i+1900] for i in range(0, len(a), 1900)]:
        await ctx.send(f">>> ```ml\n{chunk}\n```")


client.run("ODM3MzEyOTY0MzE0MDA1NTM1.YIqudw.yx1VByUvllAKUNs0xr-tgHzoae4")