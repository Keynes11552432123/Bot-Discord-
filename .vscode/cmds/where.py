import discord
import time
from core.classes import Cog_Extension
from discord.ext import commands

class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '群組':
            guilds = await self.bot.fetch_guilds(limit=150).flatten()
            for i in guilds:
                await message.channel.send(i.name)

def setup(bot):
    bot.add_cog(Event(bot))