from discord.ext import commands
import logging
import discord
import datetime
import psutil

log = logging.getLogger(__name__)

LOGGING_CHANNEL = 309632009427222529

class event:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    async def on_member_join(member):
        server = member.server
        fmt = 'Welcome {0.mention} to {1.name}!'
        await bot.send_message(server, fmt.format(member, server))

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
    bot.add_cog(event(bot))
    commands.Bot.on_error = on_error