import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import time
from datetime import datetime
from PIL import Image, ImageFilter
import requests
from io import BytesIO
import inspect
import praw
import PIL.Image

bot = commands.Bot(command_prefix='n!')
reddit = praw.Reddit(client_id='u3zBVRAgVJ8eOw',
                     client_secret='_TeCQvme4Nj3GEpUCgS5nwgeJZE',
                     user_agent='discord:u3zBVRAgVJ8eOw:v1.0 (by /u/BoringJelly)')
bot.launch_time = datetime.utcnow()
bot.remove_command('help')
async def loop():
    while True:
        await bot.change_presence(game=discord.Game(name="n!help", url="https://twitch.tv/MMgamerBOT", type=1))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="some memez", url="https://twitch.tv/MMgamerBOT", type=1))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="prefix -> n!", url="https://twitch.tv/MMgamerBOT", type=1))
        await asyncio.sleep(15)

@bot.event
async def on_ready():
    print ("Bot has Booted!")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
    await bot.change_presence(game=discord.Game(name="mmgamerbot.com", url="https://twitch.tv/MMgamerBOT", type=1))
    allokreq = requests.get("https://i.imgur.com/eS920kh.png")
    allok = Image.open(BytesIO(allokreq.content)).convert("RGBA")
    allok.show
    await loop()


#welcome to nexus

#general commands

@bot.command(pass_context=True)
async def ping(ctx):
        t1 = time.perf_counter()
        tmp = await bot.say("<a:discordloading:439643878803505162> pinging...")
        t2 = time.perf_counter()
        await bot.say("Ping: {}ms".format(round((t2-t1)*1000)))
        await bot.delete_message(tmp)

@bot.command(pass_context=True)
async def help(ctx):
    with open("help.txt", "r") as txtfile:
        content = txtfile.read()
        embed = discord.Embed(description = "In this menu you can see all of nexeros commands! Here is some info! \n **Coded With:** <:py:439652582995132416> \n **Made By:** @MMgamer#3477", title = "Help menu", color=0x23272A)
        embed.add_field(name="\u200b", value=f"```{content}```")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def changelog(ctx):
    with open("changelog.txt", "r") as txtfile:
        content = txtfile.read()
    await bot.say("```{0}```".format(content))
    txtfile.close()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(ctx, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title="Welp! Some old memes have cut the power cord!",
                              description="That command was not found! We suggest you do `n!help` to see all of the commands",
                              colour=0xe73c24)
        await bot.send_message(error.message.channel, embed=embed)
    else:
        embed = discord.Embed(title="Welp! Someone was playing mineplex when this happened!",
                              description=f"{ctx}",
                              colour=0xe73c24)
        await bot.send_message(error.message.channel, embed=embed)
        raise(ctx)

@bot.command(pass_context=True)
async def add(ctx, a: int, b: int):
    await bot.say(a+b)


@bot.command(pass_context=True)
async def multiply(ctx, a: int, b: int):
    await bot.say(a*b)

@bot.command(pass_context=True)
async def lostshibe(ctx, user: discord.Member=None):
    if user is None:
        user = ctx.message.author
    base = Image.open(BytesIO(requests.get('https://i.imgur.com/MRFa2n5.jpg%27').content)).convert('RGBA')
    img = Image.open(BytesIO(requests.get(user.avatar_url).content)).convert("RGBA").resize((200, 200))
    img = img.rotate(2, expand=1)
    base.paste(img, (135, 170), img)
    base.save("lostshibe.png")
    await bot.send_file(ctx.message.channel, "lostshibe.png")




@bot.command(pass_context=True)
async def jail(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("jail.png").convert("RGBA")
        background.paste(foreground, (0, 0), foreground)
        background.save("jailed.png")
        await bot.send_file(ctx.message.channel, "jailed.png")


@bot.command(pass_context=True)
async def gay(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("gay.png").convert("RGBA")
        foreground.putalpha(128)
        background.paste(foreground, (0, 0), foreground)
        background.save("gaypfp.png")
        await bot.send_file(ctx.message.channel, "gaypfp.png")

@bot.command(pass_context=True)
async def coder(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("code.png").convert("RGBA")
        foreground.putalpha(128)
        background.paste(foreground, (0, 0), foreground)
        background.save("codepfp.png")
        await bot.send_file(ctx.message.channel, "codepfp.png")

@bot.command(pass_context=True)
async def brave(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        basewidth = 125
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("bravebase.png").convert("RGBA")
        wpercent = (basewidth / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        background = background.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        background.paste(foreground, (0, 0), foreground)
        background.save("braverypfp.png")
        await bot.send_file(ctx.message.channel, "braverypfp.png")

@bot.command(pass_context=True)
async def brilliance(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        basewidth = 125
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("brilliancebase.png").convert("RGBA")
        wpercent = (basewidth / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        background = background.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        background.paste(foreground, (0, 0), foreground)
        background.save("brilliancepfp.png")
        await bot.send_file(ctx.message.channel, "brilliancepfp.png")

@bot.command(pass_context=True)
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    embed = discord.Embed(color=0x23272A)
    embed.add_field(name="Our bot's uptime :calendar_spiral:", value=f"Weeks: **{weeks}**\nDays: **{days}**\nHours: **{hours}**\nMinutes: **{minutes}**\nSeconds: **{seconds}**")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def source(ctx, *, text: str):
    """Shows source code of a command."""
    nl2 = '`'
    nl = f"``{nl2}"
    source_thing = inspect.getsource(bot.get_command(text).callback)
    await bot.say(f"{nl}py\n{source_thing}{nl}")

@bot.command(pass_context=True)
async def discordmeme(ctx):
    discordmemes_submissions = reddit.subreddit('discordmemes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in discordmemes_submissions if not x.stickied)
        await bot.say(submission.url)


@bot.command(pass_context=True)
async def cat(ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()
        embed = discord.Embed(title= "Cute Cat!", color=0x23272A)
        embed.set_image(url=f"{data['file']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def dog(ctx):
        response = requests.get('https://random.dog/woof.json')
        data = response.json()
        embed = discord.Embed(color=0x23272A)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def meme(ctx):
        response = requests.get('https://some-random-api.ml/meme')
        data = response.json()
        embed = discord.Embed(description =f"{data['text']}", color=0x23272A)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def birb(ctx):
        response = requests.get('https://some-random-api.ml/birbimg')
        data = response.json()
        embed = discord.Embed(color=0x23272A)
        embed.set_image(url=f"{data['link']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def catfact(ctx):
        response = requests.get('https://some-random-api.ml/catfact')
        data = response.json()
        embed = discord.Embed(title = "A random Cat Fact", description=f"{data['fact']}", color=0x23272A)
        embed.set_thumbnail(url="https://clipart.info/images/ccovers/1522855947cute-cat-png-cartoon-clip-art.png")
        await bot.say(embed=embed)


bot.run(os.getenv('TOKEN'))