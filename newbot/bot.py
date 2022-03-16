import discord
from discord.ext import commands

client = commands.Bot(command_prefix='?')

@client.event
async def on_reday():
    print(">>Bot Is Online<<")

client.run('OTUxNzk1OTU5NDgwODU2NjA2.YisrEA.xykQqyz5K4zH6uljvf_hZITAvE4')