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
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['Welcome_channel']))
        print(f'>>{member} join<<')
        await channel.send(f'>>{member} join<<')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'>>{member} leave<<')
        channel = self.bot.get_channel(int(jdata['Leave_channel']))
        await channel.send(f'>>{member} leave<<')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("您少輸入必要參數")
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("查無此指令")
        else:
            await ctx.send("無法偵測的錯誤，錯誤代碼為{}".format(error))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content == 'ping':
            await message.channel.send('pong')

def setup(bot):
    bot.add_cog(Event(bot))