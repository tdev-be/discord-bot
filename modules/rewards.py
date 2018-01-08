from discord.ext import commands

import datetime
import logging
import discord
import psutil

from config import LOGGING_CHANNEL

client = discord.Client()
log = logging.getLogger(__name__)

class rewards:
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.group('invite')
    async def invite(self,ctx):
        pass

    @invite.command(hidden=False)
    async def mine(self, ctx):
        '''get my own invitation link'''
        inv = await ctx.guild.invites()
        inv= list(filter(lambda x: x.inviter == ctx.author and x.max_age==0, inv))
        await ctx.message.author.send("Your personnal link for server {}: {}".format(ctx.guild.name,inv[0]))

    @invite.command(hidden=False)
    async def top(self,ctx):
        '''Top invitation by member'''
        inv = await ctx.guild.invites()
        inv = list(filter(lambda x:x.max_age==0,inv))
        inv.sort(key=lambda x:x.uses, reverse=True)
        values=''
        for i in inv[:3]:
            values+=("{} invited {} members ({})\n".format(i.inviter.name, i.uses,i.url))

        e = discord.Embed(title=None, url=None, colour=0x00ff00)
        e.description = ''
        e.add_field(name="Best member participation", value=values[0:1080])
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(rewards(bot))
    commands.Bot.on_error = on_error

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