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
async def invite(ctx):
    embed=discord.Embed(title="Invite The Bot To Your Server!",description="The bot's invite link: http://invite.nexerobot.cf", color=0x23272A)
    embed.set_author(icon_url="https://png.icons8.com/small/1600/external-link.png",name="Link")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    with open("help.txt", "r") as txtfile:
        content = txtfile.read()
        embed = discord.Embed(description = "In this menu you can see all of nexeros commands! Here is some info! \n **Coded With:** <:py:439652582995132416> \n **Made By:** @MMgamer#3477 \n <:help:488764512879509514> **Support Server:** https://discord.gg/rRBQHbd" , title = "Help menu", color=0x23272A)
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
async def on_message(message):
    if message.content == "<@486143318405939238>":
            await bot.say("Hey, I'm nexero!")
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def add(ctx, a: int, b: int):
    await bot.say(a+b)

@bot.command(pass_context=True)
async def accept(ctx, member: message.author):
        role = discord.utils.get(member.server.roles, name='Coder')
        await bot.add_roles(member, role)
        await bot.whisper("Thanks for Passing Through The Gate!")
        await bot.delete_message("1")

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
async def rulessetup(ctx):
    if ctx.message.author.id == '279714095480176642':
        #embed.add_field(name="", value="")
        lowsev = discord.Embed(color =0x00FF00, title = "Low Severity [Warn]")
        lowsev.add_field(name="Use english in all channels unless stated otherwise", value="Makes it easier for staff to moderate chat")
        lowsev.add_field(name="Don't be annoying ", value="Includes minimoding and treating other users/staff unniceley")
        lowsev.add_field(name="Don't undo what a staff member has done ", value="Name changes, etc")
        lowsev.add_field(name="False/ Spam pings", value="Like ghost pinging, pinging staff for your meme, etc")
        lowsev.add_field(name="Spamming of any sort", value="Includes Character Spam, Flooding Chat, Emoji Spam, Reaction Spam and ASCII text")
        medsev = discord.Embed(color =0xffa500, title = "Medium Severity Kick and or Ban]")
        medsev.add_field(name="Advertising of any sort", value="Servers (Inc DM), Products, etc")
        medsev.add_field(name="Selfbotting", value="Its against the TOS don't do it.")
        medsev.add_field(name="Sharing of illegal or false information", value="Untrue Rumors, etc")
        maxserv = discord.Embed(color =0xff0000, title = "High serverity [Permanent Ban]")
        maxserv.add_field(name="Sending NSFW ", value="Porn, Hentai, boobs, etc")
        maxserv.add_field(name="Alts", value="We don't know what you do with them.")
        maxserv.add_field(name="Sending files or programs that can damage another user's device", value="Viruses, Trojans, Adware, etc")
        maxserv.add_field(name="Raiding", value="Ban and report to discord's trust and saftey team")
        maxserv.add_field(name="Racism, Homofobia", value="We **must** respect everyone independent of race, sexuallity or country of residance")
        await bot.say(embed=lowsev)
        await bot.say(embed=medsev)
        await bot.say(embed=maxserv)
    else:
        await bot.say("no. just no")




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
async def balance(ctx, user: discord.Member):
    if user is None:
        pass
    else:
        basewidth = 125
        response = requests.get(user.avatar_url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open("balancebase.png").convert("RGBA")
        wpercent = (basewidth / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        background = background.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        background.paste(foreground, (0, 0), foreground)
        background.save("balancepfp.png")
        await bot.send_file(ctx.message.channel, "balancepfp.png")

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
