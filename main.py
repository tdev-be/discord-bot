from discord.ext import commands
import datetime
import logging
import config
import discord
import sys
import traceback

description = """
"""

from config import LOGGING_CHANNEL
log = logging.getLogger(__name__)

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    base.append(config.prefix)
    return base

class Robot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description=description,
                         pm_help=None, help_attrs=dict(hidden=True))

        self.load_extension('modules.utility')
        self.load_extension('modules.funny')
        self.load_extension('modules.events')
        self.load_extension('modules.stats')
        self.load_extension('modules.rewards')
        self.load_extension('modules.groups')
        self.load_extension('modules.admin')


        self.client_id = config.client_id

    async def on_error(self, event, *args, **kwargs):
        import pdb;pdb.set_trace()
        e = discord.Embed(title='Event Error', colour=0xa32952)
        e.add_field(name='Event', value=event)
        e.description = f'```py\n{traceback.format_tb(sys.exc_info()[2])}\n```'
        e.timestamp = datetime.datetime.utcnow()
        ch = self.get_channel(LOGGING_CHANNEL)
        try:
            await ch.send(embed=e)
        except:
            pass

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def on_resumed(self):
        print('resumed...')


    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(config.token, reconnect=True)


if __name__ == '__main__':
    bot = Robot()
    bot.run()