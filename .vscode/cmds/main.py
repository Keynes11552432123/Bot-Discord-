import imp
from msilib.schema import File, SelfReg
from sqlite3 import Timestamp

import discord_slash
from typing_extensions import Self
import discord
from discord.ext import commands
import datetime
import json
import random
from core.classes import Cog_Extension
from discord import Status
from discord_slash import SlashCommand

class Main(Cog_Extension):
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send('1234567890')

    @commands.command(aliases=['eb'])
    async def embed(self, ctx):
        embed=discord.Embed(title="貓妖", url="https://catyoukaisho.soci.vip", description="貓妖的介紹", color=0x322e76, timestamp= datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))))
        embed.set_author(name="Cat_Youkai_Sho", url="https://catyoukaisho.soci.vip", icon_url="https://cdn.psee.pw/2dd6b920-15b9-4d0f-84ee-399d411224eb.png")
        embed.set_thumbnail(url="https://cdn.psee.pw/2dd6b920-15b9-4d0f-84ee-399d411224eb.png")
        embed.add_field(name="1", value="11", inline=False)
        embed.add_field(name="2", value="22", inline=True)
        embed.add_field(name="3", value="33", inline=True)
        embed.add_field(name="4", value="44", inline=True)
        embed.set_footer(text="Ya!")
        await ctx.send(embed=embed)

    @commands.command(aliases=['rs'])
    async def resay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(aliases=['clear', 'c'])
    async def clean(self, ctx, num=11):
        await ctx.channel.purge(limit=num+1)

    @commands.command()
    async def random_squad(self, ctx):
        online = []
        for member in ctx.guild.members:
            if str(member.status) == 'online'and member.bot == False:
                online.append(member.name)
        
        random_online = random.sample(online, k=3)      #k=要抽出多少人
        for squad in range(3):                          #要抽多少組
            random_online_squad = random.sample(random_online, k=1)
            await ctx.send(f"第{squad+1}小隊" + str(random_online_squad))
            print(random_online_squad)                  #k=要抽出多少人
            for name in random_online_squad:
                random_online.remove(name)

    @commands.group(aliases=['ct'])
    async def codetest(self, ctx):
        pass

    @codetest.command(aliases=['py'])
    async def python(self, ctx):
        await ctx.send("Python")

    @codetest.command(aliases=['js'])
    async def javascript(self, ctx):
        await ctx.send("JavaScript")

    @codetest.command(aliases=['c++'])
    async def cpp(self, ctx):
        await ctx.send("C++")

    @clean.error
    async def clean_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("請輸入需要清理的訊息數(條)")

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        await ctx.send(F'{round(self.bot.latency*1000)} (ms)')

def setup(bot):
    bot.add_cog(Main(bot))