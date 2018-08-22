from discord.ext import commands
import discord
import logging
import datetime
import psutil
import threading
from asyncio import sleep
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

    @commands.command(hidden=False)
    async def beer(self, ctx, member: discord.Member=None):
        '''Give me a beer'''
        if member==None:
            member= ctx.author
        await ctx.send(f':beer: Here is your beer {member.mention}! :beer:')

    @commands.command(hidden=False)
    async def tea(self, ctx, timer=0):
        '''Tea time'''
        member = ctx.author
        await sleep(timer*60)

        await ctx.send(f'Your tea is ready {member.mention}!')
        # async def sendDM(ctx, member):
        #     print('TEST')
        #     await ctx.send(f'Your tea is ready {member.mention}!')
        # job = threading.Timer(timer, sendDM, (ctx, member))
        # job.start()

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