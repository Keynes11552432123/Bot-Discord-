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
    async def on_raw_reaction_add(self, payload):
        print(payload.emoji)
        if payload.message_id == 949288922737954816:
            if str(payload.emoji) == "<:photo:948190348579057686>":
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(877580013900292149)
                await payload.member.add_roles(role)
                await payload.member.send(f">>你取得了{role}身分組<<")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 949288922737954816:
            if str(payload.emoji) == "<:photo:948190348579057686>":
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(877580013900292149)
                await user.remove_roles(role)
                await user.send(f">>你移除了{role}身分組<<")

def setup(bot):
    bot.add_cog(Event(bot))