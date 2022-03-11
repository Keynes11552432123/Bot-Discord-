from argparse import Action
import csv
from msilib.schema import File
from attr import get_run_validators
import discord
from discord.ext import commands
import json
import random
from core.classes import Cog_Extension
from cmds.main import Main

with open ('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('說'):
            tmp = message.content.split(" ", 2)
            if len(tmp) == 1:
                await message.channel.send(">>你要我說甚麼啦！<<")
            else:
                await message.channel.send(tmp[1])

def setup(bot):
    bot.add_cog(Event(bot))