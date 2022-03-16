from msilib.schema import File
from pickle import TRUE
import discord
from discord.ext import commands
import json
import random
import os
from discord_slash import SlashCommand

with open ('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>', intents = intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(">>✅Bot is online<<")
    print('Ready!')
    print('Logged in as ---->', bot.user)
    print('ID:', bot.user.id)

@bot.command(aliases=['l'])
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'>>Loaded {extension} done<<')

@bot.command(aliases=['ul'])
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'>>Un-Loaded {extension} done<<')

@bot.command(aliases=['rl'])
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'>>Re-Loaded {extension} done<<')

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])