from discord.ext import commands
import discord
import logging
import datetime
import psutil
from utils.db.datatype import *

from config import LOGGING_CHANNEL

log = logging.getLogger(__name__)
client = discord.Client()

class funny:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(hidden=False)
    async def pizza(self, ctx, member: discord.Member=None):
        '''Give me a pizza'''
        if member==None:
            member= ctx.author
        await ctx.send(f':pizza: Here is your pizza {member.mention}! :pizza:')

async def on_error(self, event, *args, **kwargs):
    e = discord.Embed(title='Event Error', colour=0xa32952)
    e.add_field(name='Event', value=event)
    e.description = f'```py\n{traceback.format_exc()}\n```'
    e.timestamp = datetime.datetime.utcnow()
    ch = self.get_channel(LOGGING_CHANNEL)
    try:
        await ch.send(embed=e)
    except:
        pass

def setup(bot):
    bot.add_cog(funny(bot))
    commands.Bot.on_error = on_error