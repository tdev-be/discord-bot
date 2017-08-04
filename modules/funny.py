from discord.ext import commands
import discord
import logging
import datetime
import psutil
from utils.db.datatype import *

log = logging.getLogger(__name__)

LOGGING_CHANNEL = 309632009427222529

class funny:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(hidden=False)
    async def fun(self, ctx):
        '''useless'''
        await ctx.send(f'Funny World !')

    @commands.command(hidden=False)
    async def pizza(self, ctx):
        '''Give me a pizza'''
        await ctx.send(':pizza: Here is your pizza ! :pizza:')

    @commands.command(hidden=True)
    async def test(self, ctx):
        '''Give me a pizza'''
        await ctx.send('test ok !')

    @commands.command(hidden=True)
    async def read(self, ctx):
        '''Give me a pizza'''
        games = played_game_repository().read()
        for g in games:
            print(g.game)
            await ctx.send(f"game : {g.game}")

    async def on_message(self, message: discord.Message):
        pass
        #print(f'recu "{message.content}" sur #{message.channel}')
        #print(message.channel.guild)
        #print(self.bot.send_message)
        #msg = await self.bot.send_message(message.channel, 'ok')

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