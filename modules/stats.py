from discord.ext import commands
import discord
import logging
import datetime
from datetime import timedelta
import psutil
from utils.db.datatype import *

log = logging.getLogger(__name__)

from config import LOGGING_CHANNEL

class stats:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        beforeGame = before.game
        afterGame = after.game
        if beforeGame != afterGame:
            if beforeGame is None:
                print('start game')
                log_game(after.guild.name, after._user.name, afterGame.name, datetime.now())
            elif afterGame is None:
                print ('stop game')
                log_end_game(before.guild.name, before._user.name, beforeGame.name, datetime.now())
            else:
                print('change game')
                log_end_game(before.guild.name, before._user.name, beforeGame.name, datetime.now())
                log_game(after.guild.name, after._user.name, afterGame.name, datetime.now())

    @commands.group()
    async def stat(self, ctx):
        '''Get stats from the server'''
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid stat command passed...')

    @stat.command(hidden=False)
    async def game(self, ctx, game=None):
        '''Stats per game on thi server'''
        if game == None:
            return
        try:
            list = gamestat(ctx.guild.name, game, ctx)
        except Exception as e:
            em = discord.Embed(title=None, url=None, colour=0xff0000)
            em.description = ''
            em.add_field(name="Error", value=e)
            await ctx.send(embed=em)

        values = ''
        for (user, count, time) in list:
            values += "**{}** played {} times (total {})\n".format(user, count, timedelta(seconds=time))

        e = discord.Embed(title=None, url=None, colour=0x00ff00)
        e.description = ''
        e.add_field(name="Stats for {}".format(game), value=values[0:1080])
        await ctx.send(embed=e)

    @stat.command(hidden=False)
    async def user(self, ctx, user:discord.Member=None):
        '''Stats per game on thi server'''
        if user == None:
            return
        try:
            list = userstat(ctx.guild.name, user._user.name, ctx)
        except Exception as e:
            em = discord.Embed(title=None, url=None, colour=0xff0000)
            em.description = ''
            em.add_field(name="Error", value=e)
            await ctx.send(embed=em)

        values = ''
        for (game, count, time) in list:
            values += "**{}** played {} times (total {})\n".format(game, count, timedelta(seconds=time))

        e = discord.Embed(title=None, url=None, colour=0x00ff00)
        e.description = ''
        e.add_field(name="Stats for {}".format(user._user.name), value=values[0:1080])
        await ctx.send(embed=e)

    @stat.command(hidden=False)
    async def topgame(self, ctx, limit=10):
        '''Stats per game on thi server'''
        list = stats_per_game(ctx.guild.name, ctx)
        values = ''
        for (game, count, time)  in list[0:limit]:
            values += f"**{game}** was used **{count}** times (total {timedelta(seconds=time)})\n"

        e = discord.Embed(title='Stats per game played', url=None, colour=0x00ff00)
        e.description = ''
        e.add_field(name=f'**Top {limit}**', value=values)
        await ctx.send(embed=e)

    @stat.command(hidden=False)
    async def topuser(self, ctx, limit=10):
        '''Stats per user and per game on this server'''
        list = stats_per_user(ctx.guild.name, ctx)
        values = ''
        for (user, game, count, time) in list[0:limit]:
            values += f"*{user}* played \"**{game}**\" {count} times (total : {timedelta(seconds=time)})\n"

        e = discord.Embed(title='Stats per game played by user', url=None, colour=0x00ff00)
        e.description = ''
        e.add_field(name=f'**Top {limit}**', value=values)
        await ctx.send(embed=e)

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
    bot.add_cog(stats(bot))
    commands.Bot.on_error = on_error