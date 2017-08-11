from discord.ext import commands
import discord
import logging
import datetime
import psutil
from utils.db.datatype import *

log = logging.getLogger(__name__)

LOGGING_CHANNEL = 309632009427222529

class stats:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        beforeGame = before.game
        afterGame = after.game
        if beforeGame != afterGame:
            if beforeGame is None:
                log_game(after.guild.name, after._user.name, afterGame.name, datetime.now())
            elif afterGame is None:
                log_end_game(before.guild.name, before._user.name, beforeGame.name, datetime.now())
            else:
                log_end_game(before.guild.name, before._user.name, beforeGame.name, datetime.now())
                log_game(after.guild.name, after._user.name, afterGame.name, datetime.now())

    @commands.group()
    async def stat(self, ctx):
        '''Get stats from the server'''
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid stat command passed...')

    @stat.command(hidden=False)
    async def game(self, ctx):
        '''Stats per game on thi server'''
        list = stats_per_game(ctx.guild.name, ctx)
        for (game, count)  in list:
            await ctx.send (f"{game} was used {count} times")

    @stat.command(hidden=False)
    async def user(self, ctx):
        '''Stats per user and per game on this server'''
        list = stats_per_user(ctx.guild.name, ctx)
        for (user, game, count) in list:
            await ctx.send(f"{user} played \"{game}\" {count} times")


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