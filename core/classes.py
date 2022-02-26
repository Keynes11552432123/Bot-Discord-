from msilib.schema import File
import discord
from discord.ext import commands
import json
import random

class Cog_Extension(commands.Cog):
    def __init__(selF, bot):
        selF.bot = bot