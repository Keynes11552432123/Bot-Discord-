import asyncio
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
        if message.content == '我好帥喔':
            tmpmsg = await message.channel.send('>>你確定你帥嗎？<<')
            await asyncio.sleep(3)
            await tmpmsg.delete()

def setup(bot):
    bot.add_cog(Event(bot))