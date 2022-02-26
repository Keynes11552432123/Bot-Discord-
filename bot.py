from msilib.schema import File
import discord
from discord.ext import commands
import json
import random
import os

with open ('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/cd ', intents = intents)

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
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'>>Loaded {extension} done<<')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'>>Un-Loaded {extension} done<<')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'>>Re-Loaded {extension} done<<')

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])