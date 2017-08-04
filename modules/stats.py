from discord.ext import commands
import logging
import discord
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
                print(before.display_name+ ' start playing ' + afterGame.name )
                log_game('server', after._user.name, afterGame.name, datetime.now())
            elif afterGame is None:
                #after.send('stop playing')
                print(before.display_name+ ' stopped playing ' + beforeGame.name  )
            else:
                log_game('server', after._user.name, afterGame.name, datetime.now())

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