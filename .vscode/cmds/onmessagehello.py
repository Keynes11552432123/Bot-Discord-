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
        if message.content.startswith('跟我打聲招呼吧'):
            channel = message.channel
            await channel.send('那你先跟我說你好')
            def checkmessage(m):
                return m.content == '你好' and m.channel == channel
            msg = await self.bot.wait_for('message', check=checkmessage)
            await channel.send('>>嗨，{.author}！<<'.format(msg))

def setup(bot):
    bot.add_cog(Event(bot))