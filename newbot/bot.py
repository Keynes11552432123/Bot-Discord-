from itertools import cycle
import json
from logging import exception
from turtle import title
import discord
from discord import user
from discord import activity
from discord.client import Client
from discord.ext import commands, tasks
import random
from discord.member import Member
from discord.user import User
import os
from PIL import Image
from io import BytesIO
import asyncio

os.chdir('D:\\code\\newbot')

def get_prefix(client, message):
    with open('prefixes.json', 'r', encoding='utf8') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, intents = discord.Intents.all())
client.remove_command("help")

status = cycle([
    'Watching Cat_Youkai_Sho',
    'Watching You',
    'Having Fun!',
    '?help'
])

@tasks.loop(seconds=10)
async def status_swap():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
    print(">>Bot Is Online<<")
    status_swap.start()

@client.event
async def on_member_join(member):

    welcome_embed = discord.Embed(title = f'New Member!!!', description = f'{member.mention} has join the server', color = discord.Color.blue())
    await client.get_channel(880437833641394267).send(embed = welcome_embed)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r', encoding='utf8') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '?'

    with open('prefixes.json', 'w', encoding='utf8') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r', encoding='utf8') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w', encoding='utf8') as f:
        json.dump(prefixes, f, indent=4)

@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(aliases=['prefix'])
async def setprefix(ctx, prefixset = None):
    if (not ctx.author.guild_permissions.manage_channels):
        await ctx.send('This command requires ``Mange Channels`` permissions')
        return

    if (prefixset == None):
        prefixset = '?'

    with open('prefixes.json', 'r', encoding='utf8') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w', encoding='utf8') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'The bot prefix has been changed to ``{prefixset}``')

@client.command(aliases=['h'])
async def help(ctx):
    helpEmbed = discord.Embed(title = "Help is on the way!", color = discord.Color.blue())
    helpEmbed.add_field(name = "Moderation", value = "`ban`,`kick`,`mute`,`unmute`,`clear`,`pingtime`,`gcreate`")
    helpEmbed.add_field(name = "Fun", value="`wanted`,`ping`,`8ball`,`avatar`")
    await ctx.send(embed = helpEmbed)

@client.command(aliases=['ava'])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        if member == None:
            member = ctx.author

    memberAvatar = member.avatar_url

    avaEmbed = discord.Embed(title = f"{member.name}'s Avatar")
    avaEmbed.set_image(url = memberAvatar)

    await ctx.send(embed = avaEmbed)

@client.command(aliases=['8ball', '8b', 'eb'])
async def eightball(ctx, *, question):
    responses=["It is certain.",
               "It is decidedly so.",
               "Without a doubt.",
               "Yes - definitely.",
               "You may rely on it.",
               "As I see it, yes.",
               "Most likely.",
               "Outlook good.",
               "Yes.",
               "Signs point to yes.",
               "Replay hazy, try again.",
               "IDK but you should sub to glowstik.",
               "Better not tell you now.",
               "Cannot predict now.",
               "Concentrate and ask again.",
               "Don't count on it.",
               "My reply is no.",
               "My sources say no.",
               "Outlook not so good",
               "Very doubtful."]
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')

@client.command(aliases=['s'])
async def say(ctx, *, saymsg=None):
    if saymsg == None:
        return await ctx.send('You must tell me a message to say!')
    sayEmbed = discord.Embed(title = f'{ctx.author} Says', description = f"{saymsg}", color = discord.Color.red())
    await ctx.send(embed = sayEmbed)

@client.command(aliases=['k'])
async def kick(ctx, member:discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('This command requires ``Kick Members`` permissions')
        return
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked')

@client.command(aliases=['b'])
@commands.cooldown(1, 60, commands.cooldowns.BucketType.user)
async def ban(ctx, member:discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('This command requires ``Ban Members`` permissions')
        return
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned')

@client.command(aliases=['ub'])
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(aliases=['purge', 'clean', 'c'])
async def clear(ctx, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This command requires ``Mange Messages`` permissions')
        return
    amount = amount+1
    if amount >= 101:
        await ctx.send('Can not delete more than 100 messages')
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Clear {amount} messages')

@client.command(aliases=['gc'])
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        return await ctx.send('Please include a time!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    gcembed = discord.Embed(title='New Giveaway', description=f'{ctx.author.mention} is giving away **{prize}**!!', color=discord.Color.blue())
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    gawtime = int(time[:-1]) * time_convert[time[-1]]
    gcembed.set_footer(text=f'Giveaway ends in {time}')
    gaw_msg = await ctx.send(embed = gcembed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(int(gawtime))

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"YAYYY!!! {winner.mention} has won the giveaway for **{prize}**!!!")

@client.command(aliases=['m'])
@commands.cooldown(1, 30, commands.cooldowns.BucketType.user)
async def mute(ctx, member: discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This command requires ``Manage Messages`` permissions')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name="Muted")

    if not muteRole:
        await ctx.send('No mute role has been found. Creating mute role...')
        muteRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
    await member.add_roles(muteRole, reason=reason)
    await ctx.send('User has been muted!')
    await member.send(f'You have been muted from **{guild.name}** | Reason: **{reason}**')

@client.command(aliases = ['sm'])
async def slowmode(ctx, time=0):
   if (not ctx.author.guild_permissions.manage_messages):
       await ctx.send('This command requires ``Manage Messages`` premissions')
       return
   try:
       if time == 0:
           await ctx.send('Slowmode Off')
           await ctx.channel.edit(slowmode_delay = 0)
       elif time > 21600:
            await ctx.send('You can not set the slowmode above 6 hours')
            return
       else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(f'Slowmode set to {time} senconds!')
   except exception:
       await print('Oops! That is something wrong with this command!')

@client.command(aliases=['si'])
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = discord.Embed(timstamp=ctx.message.created_at, color=ctx.author.color)
    serverinfoEmbed.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name="Highest Role", value=ctx.guild.roles[-1], inline=False)
    serverinfoEmbed.add_field(name="Number of Roles", value=str(role_count), inline=False)
    serverinfoEmbed.add_field(name="Bots", value=', '.join(list_of_bots), inline=False)

    await ctx.send(embed = serverinfoEmbed)

@client.command(aliases=['w'])
async def wanted(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    wanted = Image.open("wanted.jpg")

    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    profilepic = Image.open(data)

    profilepic = profilepic.resize((300, 300))

    wanted.paste(profilepic, (78, 219))

    wanted.save("wantedpic.jpg")

    await ctx.send(file = discord.File("wantedpic.jpg"))

    os.remove("wantedpic.jpg")

@client.command(aliases=['um'])
async def unmute(ctx, member: discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This command requires ``Manage Messages`` permissions')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name="Muted")

    if not muteRole:
        await ctx.send("The muted role has not been found")
        return

    await member.remove_roles(muteRole, reason=reason)
    await ctx.send('User is unmuted')
    await member.send(f'You have been unmuted from **{guild.name}** | Reason: **{reason}** | Please Press ``Ctrl+r`` to reload, thank you')

@eightball.error
async def eightball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a question')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a member')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member is not found")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a member')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member is not found")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a member')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member is not found")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a member')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member is not found")

@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include a prefix')

@client.command(aliases=['pt'])
async def pingtime(ctx):
  await ctx.send(F'{round(client.latency*1000)} (ms)')

@ban.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Take it easy! Please try this command in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

client.run('OTUxNzk1OTU5NDgwODU2NjA2.YisrEA.xykQqyz5K4zH6uljvf_hZITAvE4')
