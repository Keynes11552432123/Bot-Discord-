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
    async def on_message_delete(self, msg):
        counter = 1
        async for audilog in msg.guild.audit_logs(action=discord.AuditLogAction.message_delete):
            if counter == 1:
                await msg.channel.send(f"刪除者：{audilog.user.name}#{audilog.user.discriminator}")
                counter += 1
        await msg.channel.send("刪除內容：" + str(msg.content))
        await msg.channel.send("被刪除的訊息作者：" + str(msg.author))

def setup(bot):
    bot.add_cog(Event(bot))