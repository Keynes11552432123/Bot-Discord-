import discord
from discord.ext import commands
import json

with open ('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='cd ', intents = intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['Welcome_channel']))
    print(f'>>{member} join<<')
    await channel.send(f'>>{member} join<<')

@bot.event
async def on_member_remove(member):
    print(f'>>{member} leave<<')
    channel = bot.get_channel(int(jdata['Leave_channel']))
    await channel.send(f'>>{member} leave<<')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')

bot.run(jdata['TOKEN'])