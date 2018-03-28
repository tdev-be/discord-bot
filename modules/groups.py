from discord.ext import commands
import discord
import logging
import datetime
import psutil
from utils import checks
from utils.db.datatype import *

from config import LOGGING_CHANNEL

log = logging.getLogger(__name__)
client = discord.Client()

class groups:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.group()
    @checks.has_permissions(administrator=True)
    async def group(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid stat command passed...')

    @group.command(hidden=False)
    @checks.has_permissions(administrator=True)
    async def add(self, ctx, group: discord.Role):
        '''add a group to the list'''
        add_group(ctx.guild.name, group.name);

    @group.command(hidden=False)
    @checks.has_permissions(administrator=True)
    async def remove(self, ctx, group: discord.Role):
        '''remove a group from the list'''
        remove_group(ctx.guild.name, group.name);

    @commands.command(hidden=False)
    async def joingroup(self, ctx, group: discord.Role):
        '''join a group'''
        if group.name in list_group(ctx.guild.name):
            await ctx.author.add_roles(group)
        else:
            raise Exception('group not found)')

    @commands.command(hidden=False)
    async def leavegroup(self, ctx, group: discord.Role):
        '''leave a group'''
        await ctx.author.remove_roles(group)

    @commands.command(hidden=False)
    async def listgroup(self, ctx):
        '''list all groups'''
        list=list_group(ctx.guild.name)
        em = discord.Embed(title=None, url=None, colour=0xff0000)
        em.description = ''
        value="No group available"
        if (len(list)) > 0:
            value = '\n'.join(list)
        em.add_field(name="Groups available", value=value)
        await ctx.send(embed=em)


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
    bot.add_cog(groups(bot))
    commands.Bot.on_error = on_error