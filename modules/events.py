from discord.ext import commands
import logging
import discord
import datetime
import psutil
from config import LOGGING_CHANNEL

log = logging.getLogger(__name__)
client = discord.Client()


class event:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @client.event
    async def on_member_join(self, member: discord.Member):
        fmt = 'Welcome {0.mention} to {0.guild} !'
        await member.send( fmt.format(member))

async def on_error(self, event, *args, **kwargs):
    e = discord.Embed(title='Event Error', colour=0xa32952)
    e.add_field(name='Event', value=event)
    e.description = f'```py\n{traceback.format_exc()}\n```'
    e.timestamp = datetime.datetime.utcnow()
    ch = self.get_channel(LOGGING_CHANNEL)
    try:
        await ch.send(embed=e)
    except:
        print(e.description)

def setup(bot):
    bot.add_cog(event(bot))
    commands.Bot.on_error = on_error