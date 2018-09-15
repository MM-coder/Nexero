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
import pyspeedtest
import sqlite3

bot = commands.Bot(command_prefix='n!')
reddit = praw.Reddit(client_id='u3zBVRAgVJ8eOw',
                     client_secret='_TeCQvme4Nj3GEpUCgS5nwgeJZE',
                     user_agent='discord:u3zBVRAgVJ8eOw:v1.0 (by /u/BoringJelly)')
bot.launch_time = datetime.utcnow()
st = pyspeedtest.SpeedTest()
conn = sqlite3.connect('users.db', isolation_level=None)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                      UserID TEXT,
                      Xp INT,
                      PRIMARY KEY(UserID))""")

developers = ['279714095480176642', '344404945359077377']




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

@bot.command(pass_context=True)
async def connection(ctx):
    async with channel.typing():
        ping = str(int(round(st.ping(), 0)))
        down = round((st.download()/1000000), 2)
        up = round((st.upload()/1000000), 2)
        embed = discord.Embed(title="Connection Statistics", description="Current Connection Statistics", color=0x23272A)
        embed.add_field(name="Ping", value="`%sms`" % ping)
        embed.add_field(name="Download", value="`%s mbps`" % down)
        embed.add_field(name="Upload", value="`%s mbps`" % up)
        await bot.say(embed=em)

@bot.command(pass_context=True)
async def mute(ctx, member: discord.Member, time: int, *, reason):
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
    await bot.send_message(member, f"You have been muted for {time} Seconds in {ctx.message.server.name}! Be sure to read the rules again! ")
    role = discord.utils.get(ctx.message.server.roles, name="Muted")
    await bot.add_roles(member, role)
    embed = discord.Embed(title="MUTED", description="{} You have been Muted for **{}** Seconds. Reason: {}".format(member.mention, time, reason), color=0x23272A)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    await asyncio.sleep(time)
    await bot.remove_roles(member, role)
    await bot.send_message(member, f"You have been unmuted! Be careful!")
    embed = discord.Embed(title="Member unmuted", description="{} Has been Unmuted".format(member.mention), color=0x23272A)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, userName: discord.Member ,*, reason: str):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        embed = discord.Embed(title="Warned", description="{} You have been warned for **{}**".format(userName.mention, reason), color=0x23272A)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await bot.say(embed=embed)
        await bot.send_message(userName, "You Have Been Warned. Reason: {}".format(reason))
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def purge(ctx, number):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        msgs = []
        number = int(number)
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            msgs.append(x)
        await bot.delete_messages(msgs)
        embed = discord.Embed(title=f"{number} messages purged!", description="Everything is nice and clean now!", color=0x23272A)
        test = await bot.say(embed=embed)
        await asyncio.sleep(10)
        await bot.delete_message(test)
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def kick(ctx, user: discord.User, *, reason: str):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        await bot.kick(user)
        await bot.say(f"boom, user has been kicked for reason: {reason}")
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        await bot.ban(user)
        await bot.say(f"{user.name} Has been Banned! Let's hope he will never come back again lol.")
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

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
async def accept(ctx):
    if ctx.message.channel == "480002978049425427":
        role = discord.utils.get(ctx.message.server.roles, name='Coder')
        await bot.add_roles(ctx.message.author, role)
        await bot.whisper("Thanks for Passing Through The Gate!")
        await bot.delete_message(ctx.message)

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
    if ctx.message.author.id == 279714095480176642:
        """Shows source code of a command."""
        nl2 = '`'
        nl = f"``{nl2}"
        source_thing = inspect.getsource(bot.get_command(text).callback)
        await bot.say(f"{nl}py\n{source_thing}{nl}")
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))


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

@bot.command(pass_context=True)
async def shibe(ctx):
        request = requests.get('http://shibe.online/api/shibes')
        link = request.json()[0]
        embed = discord.Embed(title='Shibe', color=0x23272A)
        embed.set_image(url=link)
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def addxp(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        member = ctx.message.author
    if not "owner" in [i.name.lower() for i in ctx.message.author.roles]:
        return await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
    xp = add_xp(member.id, amount)
    embed = discord.Embed(title = "Added XP", description="Added XP to `{}`".format(member.display_name), color=0x23272A)
    embed.set_thumbnail(url = member.avatar_url)
    embed.add_field(name="New XP amount", value=xp)
    embed = await bot.say(embed=embed)
    await asyncio.sleep(2)
    await bot.delete_message(embed)

@bot.command(pass_context=True)
async def removexp(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        member = ctx.message.author
    if not "owner" in [i.name.lower() for i in ctx.message.author.roles]:
        return await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
    xp = remove_xp(member.id, amount)
    embed = discord.Embed(title = "Removed XP", description="Removed XP to `{}`".format(member.display_name), color=0x23272A)
    embed.set_thumbnail(url = member.avatar_url)
    embed.add_field(name="New XP amount", value=xp)
    embed = await bot.say(embed=embed)
    await asyncio.sleep(2)
    await bot.delete_message(embed)

@bot.command(pass_context=True)
async def pfp(ctx, member: discord.Member):
     embed=discord.Embed(title="The users profile picture", color=0x23272A)
     embed.set_image(url=member.avatar_url)
     await bot.say(embed=embed)

@bot.command(pass_context=True)
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    embed = discord.Embed(title = "The User's Profile", description="User's current XP {}".format(get_xp(member.id)), color=0x23272A)
    embed.set_thumbnail(url = member.avatar_url)
    await bot.say(embed=embed)


def create_user_if_not_exists(user_id: str):
    print(user_id)
    res = c.execute("SELECT COUNT(*) FROM Users WHERE UserID=?", (user_id,))
    user_count = res.fetchone()[0]
    print(user_count)
    if user_count < 1:
        print("Creating user with id " + str(user_id))
        c.execute("INSERT INTO Users VALUES (?, ?)", (user_id, 0))


def get_xp(user_id: str):
    create_user_if_not_exists(user_id)
    res = c.execute("SELECT Xp FROM Users WHERE UserID=?", (user_id,))
    user_xp = int(res.fetchone()[0])
    return int(user_xp)


def add_xp(user_id, amount: int):
    xp = int(get_xp(user_id) + amount)
    c.execute("UPDATE Users SET Xp=? WHERE UserID=?", (xp, user_id))
    return xp

def remove_xp(user_id, amount: int):
    xp = int(get_xp(user_id) - amount)
    c.execute("UPDATE Users SET Xp=? WHERE UserID=?", (xp, user_id))
    return xp


async def on_member_join(member):
    create_user_if_not_exists(member.id)

async def on_message(message):
    add_xp(message.author.id, 1)
    await bot.process_commands(message)



bot.run(os.getenv('TOKEN'))
