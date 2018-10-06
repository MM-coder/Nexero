import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import time
from datetime import datetime
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import requests
from io import BytesIO
import inspect
import praw
import PIL.Image
import pyspeedtest
import sqlite3
from discord.http import Route
import colorsys
import ast
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
                      Xp INTEGER,
                      Bans INTEGER,
                      Kicks INTEGER,
                      PRIMARY KEY(UserID))""")

developers = ['279714095480176642', '344404945359077377', '397745647723216898']

premuim = ['279714095480176642', '344404945359077377', '397745647723216898']


bot.remove_command('help')
async def loop():
    while True:
        await bot.change_presence(game=discord.Game(name="n!help"))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name=f"with {len(list(bot.get_all_members()))} users"))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name=f"on {len(bot.servers)} servers"))
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
    embed=discord.Embed(title="Invite The Bot To Your Server!",description="The bot's invite link: http://invite.nexerobot.cf", color=0x08202D)
    embed.set_author(icon_url="https://png.icons8.com/small/1600/external-link.png",name="Link")
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def help(ctx):
    with open("help.txt", "r") as txtfile:
        content = txtfile.read()
        embed = discord.Embed(description = "In this menu you can see all of nexeros commands! Here is some info! \n **Coded With:** <:py:439652582995132416> \n **Made By:** @MMgamer#3477 \n <:help:488764512879509514> **Support Server:** https://discord.gg/rRBQHbd" , title = "Help menu", color=0x08202D)
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
        embed = discord.Embed(title="Connection Statistics", description="Current Connection Statistics", color=0x08202D)
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
    embed = discord.Embed(title="MUTED", description="{} You have been Muted for **{}** Seconds. Reason: {}".format(member.mention, time, reason), color=0x08202D)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    await asyncio.sleep(time)
    await bot.remove_roles(member, role)
    await bot.send_message(member, f"You have been unmuted! Be careful!")
    embed = discord.Embed(title="Member unmuted", description="{} Has been Unmuted".format(member.mention), color=0x08202D)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, userName: discord.Member ,*, reason: str):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        embed = discord.Embed(title="Warned", description="{} You have been warned for **{}**".format(userName.mention, reason), color=0x08202D)
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
        embed = discord.Embed(title=f"{number} messages purged!", description="Everything is nice and clean now!", color=0x08202D)
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
async def ban(ctx, user: discord.Member, *, reason: str):
    if "n.staff" in [role.name for role in ctx.message.author.roles]:
        casenumb = get_bans()
        add_ban(user.id)
        await bot.ban(user)
        embed = discord.embed(title = "Ban Issued! Case: {casenumb}", description = "Details about the ban:", color =0x08202D)
        embed.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
        embed.add_field(name = "User Banned:", value = f"{user.name}")
        embed.add_field(name = "Reason:", value = f"{reason}")
        await bot.send_message(user, "It is my duty to inform you that you have been banned from {ctx.message.server} for {reason} by **me**. Have a nice day!")
        await bot.say(embed=embed)
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
async def premuimpfp(ctx, user: discord.Member):
    if user is None:
        user = ctx.message.author
    else:
        basewidth = 125
        response = requests.get(user.avatar_url)
        foreground = Image.open(BytesIO(response.content)).convert("RGBA")
        background = Image.open("nexerolevel.png").convert("RGBA")
        wpercent = (basewidth / float(foreground.size[0]))
        hsize = int((float(foreground.size[1]) * float(wpercent)))
        final = foreground.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        background.paste(final, (44, 71), final)
        font_type = ImageFont.truetype('arial.ttf', 18)
        draw = ImageDraw.Draw(background)
        draw.text(xy=(347,135), text=user.display_name, fill = (74, 65, 59, 60), font=font_type)# Name
        draw.text(xy=(346,240), text=str(get_xp(ctx.message.author.id)), fill = (74, 65, 59, 60), font=font_type)# XP
        background.save("level.png")
        await bot.send_file(ctx.message.channel, "level.png")


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
        foreground = Image.open("code.atom://teletype/portal/b0c309c1-48d9-4d30-a99e-b96b335a367epng").convert("RGBA")
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
    embed = discord.Embed(color=0x08202D)
    embed.add_field(name="Our bot's uptime :calendar_spiral:", value=f"Weeks: **{weeks}**\nDays: **{days}**\nHours: **{hours}**\nMinutes: **{minutes}**\nSeconds: **{seconds}**")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def source(ctx, *, text: str):
    if ctx.message.author.id == '279714095480176642':
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
        embed = discord.Embed(title= "Cute Cat!", color=0x08202D)
        embed.set_image(url=f"{data['file']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def dog(ctx):
        response = requests.get('https://random.dog/woof.json')
        data = response.json()
        embed = discord.Embed(color=0x08202D)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def meme(ctx):
        response = requests.get('https://some-random-api.ml/meme')
        data = response.json()
        embed = discord.Embed(description =f"{data['text']}", color=0x08202D)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def birb(ctx):
        response = requests.get('https://some-random-api.ml/birbimg')
        data = response.json()
        embed = discord.Embed(color=0x08202D)
        embed.set_image(url=f"{data['link']}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def duck(ctx, module="img"):
    module = module.lower()
    if module == "gif":
        response = requests.get('https://random-d.uk/api/v1/random?type=gif')
        data = response.json()
        embed = discord.Embed(color=0x08202D)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)
    if module == "img":
        response = requests.get('https://random-d.uk/api/v1/random?type=jpg')
        data = response.json()
        embed = discord.Embed(color=0x08202D)
        embed.set_image(url=f"{data['url']}")
        await bot.say(embed=embed)


@bot.command(pass_context=True)
async def catfact(ctx):
        response = requests.get('https://some-random-api.ml/catfact')
        data = response.json()
        embed = discord.Embed(title = "A random Cat Fact", description=f"{data['fact']}", color=0x08202D)
        embed.set_thumbnail(url="https://clipart.info/images/ccovers/1522855947cute-cat-png-cartoon-clip-art.png")
        await bot.say(embed=embed)




@bot.command(pass_context=True)
async def shibe(ctx):
        request = requests.get('http://shibe.online/api/shibes')
        link = request.json()[0]
        embed = discord.Embed(title='Shibe', color=0x08202D)
        embed.set_image(url=link)
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def addxp(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        member = ctx.message.author
    if not member.id in developers:
        return await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
    xp = add_xp(member.id, amount)
    embed = discord.Embed(title = "Added XP", description="Added XP to `{}`".format(member.display_name), color=0x08202D)
    embed.set_thumbnail(url = member.avatar_url)
    embed.add_field(name="New XP amount", value=xp)
    embed = await bot.say(embed=embed)
    await asyncio.sleep(2)
    await bot.delete_message(embed)

@bot.command(pass_context=True)
async def removexp(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        member = ctx.message.author
    if not member.id in developers:
        return await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
    xp = remove_xp(member.id, amount)
    embed = discord.Embed(title = "Removed XP", description="Removed XP to `{}`".format(member.display_name), color=0x08202D)
    embed.set_thumbnail(url = member.avatar_url)
    embed.add_field(name="New XP amount", value=xp)
    embed = await bot.say(embed=embed)
    await asyncio.sleep(2)
    await bot.delete_message(embed)

@bot.command(pass_context=True)
async def httpcat(ctx, *, code: int = None)
    if code is None:
        await bot.say("Error! You didn't pass a code")
    embed = discord.Embed(title = "Your HTTP cat!", description= f"Download it [Here](https://http.cat/{code}.jpg)!", color=0x08202D)
    embed.set_image(url = f"https://http.cat/{code}.jpg")
    except:
        pass

def get_premium(userID:str):
     with open("premium.json") as f:
         premiums = json.loads(f.read())
         try:
             return premiums[userID]
         except:
            return False


@bot.command(pass_context=True)
async def pfp(ctx, member: discord.Member):
     embed=discord.Embed(title="The users profile picture", color=0x08202D)
     embed.set_image(url=member.avatar_url)
     await bot.say(embed=embed)

@bot.command(pass_context=True)
async def botinfo(ctx):
    t1 = time.perf_counter()
    tmp = await bot.say("<a:customloading3:439656603239579660> Getting Bot Info...")
    t2 = time.perf_counter()
    embed=discord.Embed(title="Bot info", color=0x08202D)
    embed.add_field(title = "Bot Ping", value = "Ping: {}ms".format(round((t2-t1)*1000)))
    embed.add_field(title = "Acknowledgements", value = "@BluePhoenixGame#7543, @EpicShardGamingYT#6666 ")
    await bot.say(embed=embed)
    await asyncio.sleep(3)
    await bot.delete_message(tmp)

@bot.command(pass_context=True)
async def buypremuim(ctx, user: discord.Member = None):
    remove_xp(ctx.message.author.id, 100)
    premuim.append(ctx.message.author.id)
    embed = discord.Embed(title = "Bought Premium", description="You are now Premium", color=0x08202D)
    embed.set_thumbnail(url = member.avatar_url)
    await bot.say(embed=embed)



@bot.command(pass_context=True)
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    else:
        basewidth = 125
        response = requests.get(member.avatar_url)
        foreground = Image.open(BytesIO(response.content)).convert("RGBA")
        background = Image.open("nexerolevellite.png").convert("RGBA")
        wpercent = (basewidth / float(foreground.size[0]))
        hsize = int((float(foreground.size[1]) * float(wpercent)))
        final = foreground.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        background.paste(final, (81,51), final)
        font_type = ImageFont.truetype('arial.ttf', 20)
        draw = ImageDraw.Draw(background)
        draw.text(xy=(348,59), text=member.display_name, fill = (74, 65, 59, 60), font=font_type)# Name
        draw.text(xy=(347,152), text=str(get_xp(ctx.message.author.id)), fill = (74, 65, 59, 60), font=font_type)# XP
        background.save("levellite.png")
        await bot.send_file(ctx.message.channel, "levellite.png")

@bot.command(pass_context=True)
async def translate(ctx, text: str = None):
    if text is None:
        await bot.say("Sorry, {} but you didn't send the text you wanted to translate!".format(ctx.message.author.mention))
    else:
        response = requests.get(f"https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20180918T171559Z.14b6a6766d52921e.b7c18b867fc8a5774f04a6cd24128e4744c84b33&text={text}&lang=en")
        data = response.json()
        embed = discord.Embed(title = "Translated!", description = f"Your translated text: {data['text']}", colour=0x08202D)
        embed.add_field(name = "Language Translated From:", value = f"{data['lang']}")
        await bot.say(embed=embed)


@bot.command(pass_context=True)
async def invites(ctx):
    for server in bot.servers:
        for channel in server.channels:
            try:
                invite = await bot.create_invite(destination=channel)
                await bot.say(invite.url)
                break
            except:
                pass


@bot.command(pass_context=True)
async def shop(ctx, item: str, *, args):
    args = args.split(" ")
    if item == "role" or item == "colorrole" or item == "01":
        hex = args[0]
        name = args[1]
        if hex is None or name is None:
            return await bot.say("Please send a hex code and a name for the role.")
            if ctx.message.server.id == '480000098332442624' or '488710508657115167':
                if color == "green" and get_xp(ctx.message.author) < 100:
                    await bot.create_role(ctx.message.server, name=name, colour=discord.Colour.green())
                    remove_xp(ctx.message.author.id, 100)
                    embed=discord.Embed(title = "Bought Role!", description = "You just Bought a custom green role!")
                    await bot.say(embed=embed)

                elif color == "red" and get_xp(ctx.message.author):
                    role = await bot.create_role(ctx.message.server, name=name, colour=discord.Colour.red())
                    await bot.add_roles(ctx.message.author, role)
                    remove_xp(ctx.message.author.id, 100)
                    embed=discord.Embed(title = "Bought Role!", description = "You just Bought a custom red role!")
                    await bot.say(embed=embed)

                elif get_xp(ctx.message.author.id):
                    role = await bot.create_role(ctx.message.server, name=name, colour=cls(color))
                    await bot.add_roles(ctx.message.author, role)
                    remove_xp(ctx.message.author.id, 150)
                    embed=discord.Embed(title = "Bought Role!", description = "You just Bought a fully custom role!")
                    await bot.say(embed=embed)
                else:
                    embed=discord.Embed(title = "Not Avalible!", description = "This item is only avalibe on our [Support Server](https://discord.gg/8NT8AjG)")
    else:
        await bot.say("Item not found")


@bot.event
async def on_member_join(member: discord.Member):
    if member.server.id == '488710508657115167':
        embed = discord.Embed(title="User Joined!", description="{} Has Just Joined Us! Welcome to our support server!".format(member.name), color=0x08202D)
        embed.set_thumbnail(url=member.avatar_url)
        await bot.send_message(bot.get_channel('495300251054243840'), embed=embed)
    else:
        pass
#async def on_server_join(server):

    #await client.send_message(bot.get_channel('488711017711403008') embed=embed)





def create_user_if_not_exists(user_id: str):
    res = c.execute("SELECT COUNT(*) FROM Users WHERE UserID=?", (str(user_id),))
    user_count = res.fetchone()[0]
    if user_count < 1:
        print("Creating user with id " + str(user_id))
        c.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (str(user_id), 0, 0, 0))


def get_xp(user_id: str):
    create_user_if_not_exists(user_id)
    res = c.execute("SELECT Xp FROM Users WHERE UserID=?", (str(user_id),))
    user_xp = int(res.fetchone()[0])
    return user_xp


def add_xp(user_id, amount: int):
    xp = int(get_xp(user_id) + amount)
    c.execute("UPDATE Users SET Xp=? WHERE UserID=?", (xp, str(user_id)))
    return xp

def remove_xp(user_id, amount: int):
    xp = int(get_xp(user_id) - amount)
    c.execute("UPDATE Users SET Xp=? WHERE UserID=?", (xp, str(user_id)))
    return xp

def get_bans():
    res = c.execute("SELECT Bans FROM Users")
    res = res.fetchall()[0]
    bans = 0
    for ban in res:
        bans = bans + int(ban)
    return bans

def add_ban(user_id: str):
    bans = c.execute("SELECT Bans FROM Users WHERE UserID=?", (str(user_id),))
    bans = int(bans.fetchone()[0])
    res = c.execute("UPDATE Users SET Bans=? WHERE UserID=?", (bans + 1,))
    return bans + 1

def get_kicks():
    res = c.execute("SELECT Bans FROM Users")
    res = res.fetchall()[0]
    kicks = 0
    for kick in res:
        kicks = kicks + int(kick)
    return bans

def add_kick(user_id: str):
    kicks = c.execute("SELECT Kicks FROM Users WHERE UserID=?", (str(user_id),))
    kicks = int(kicks.fetchone()[0])
    res = c.execute("UPDATE Users SET Kicks=? WHERE UserID=?", (bans + 1,))
    return kicks + 1


async def on_member_join(member):
    create_user_if_not_exists(member.id)

async def send_stats():
    await bot.wait_until_ready()
    dbltoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ4NjE0MzMxODQwNTkzOTIzOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTM4MjM3NDA5fQ.adGeFiTUtOV7CZoGKTkHMXe6xe1FmQI7UKO5mv3oPHo"
    url = "https://discordbots.org/api/bots/" + str(bot.user.id) + "/stats"
    headers = {"Authorization" : dbltoken}
    while True:
        data = {"server_count"  : len(bot.servers)}
        requests.post(url,data=data,headers=headers)
        await asyncio.sleep(10)

@bot.event
async def on_message(message):
    if_xp = random.choice([True, False])
    if if_xp is True:
        add_xp(message.author.id, 1)
    await bot.process_commands(message)



def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


# async def debug(self, ctx, *, command):
#     'Execute or evaluate code in python'
#     binder = bookbinding.StringBookBinder(ctx, max_lines=50,prefix='```py', suffix='```')
#     command = self.cleanup_code(command)
#
#     try:
#         binder.add_line('# Output:')
#         if command.count('\n') == 0:
#             with async_timeout.timeout(10):
#                 if command.startswith('await '):
#                     command = command[6:]
#                 result = eval(command)
#                 if inspect.isawaitable(result):
#                     binder.add_line(
#                         f'# automatically awaiting result {result}')
#                     result = await result
#                 binder.add(str(result))
#         else:
#             with async_timeout.timeout(60):
#                 with io.StringIO() as output_stream:
#                     with contextlib.redirect_stdout(output_stream):
#                         with contextlib.redirect_stderr(output_stream):
#                             wrapped_command = (
#                                         'async def _aexec(ctx):\n' +
#                                         '\n'.join(f'    {line}'
#                                                   for line in command.split('\n')) +
#                                         '\n')
#                             exec(wrapped_command)
#                             result = await (locals()['_aexec'](ctx))
#                     binder.add(output_stream.getvalue())
#                     binder.add('# Returned ' + str(result))
#     except:
#         binder.add(traceback.format_exc())
#     finally:
#         binder.start()


bot.loop.create_task(send_stats())
bot.run(os.getenv('TOKEN'))
