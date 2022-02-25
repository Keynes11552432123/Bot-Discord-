import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='cd', intents = intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(880437833641394267)
    print(f'>>{member} join<<')
    await channel.send(f'>>{member} join<<')

@bot.event
async def on_member_remove(member):
    print(f'>>{member} leave<<')
    channel = bot.get_channel(880437860761759784)
    await channel.send(f'>>{member} leave<<')

bot.run("Token")