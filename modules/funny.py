from discord.ext import commands
from collections import Counter
import logging
import discord
import datetime
import traceback
import psutil

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
        await ctx.send_message(self.bot.default_channel, 'test ok !')

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        beforeGame = before.game
        afterGame = after.game
        if beforeGame != afterGame:
            if beforeGame is None:
                #self.bot.start_private_message(after._user)
                #await self.bot.send_message(self.bot.dafult_channel,'start playing')
                await print(before.display_name+ ' start playing ' + afterGame.name )
            elif afterGame is None:
                #after.send('stop playing')
                await print(before.display_name+ ' stopped playing ' + beforeGame.name  )
            else:
                #after.send('changed game')
                await print(before.display_name+ ' changed game for ' + afterGame.name  )

    async def on_message(self, message: discord.Message):
        print(f'recu "{message.content}" sur #{message.channel}')
        print(message.channel.guild)
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