from discord.ext import commands
import discord
import datetime
import logging
import aiohttp
import modules
import config
import psycopg2

description = """
"""

log = logging.getLogger(__name__)

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ', '!']
    base.append('!')
    base.append('?')
    return base

class Robot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description=description,
                         pm_help=None, help_attrs=dict(hidden=True))

        self.load_extension('modules.utility')
        self.load_extension('modules.funny')
        self.load_extension('modules.events')

        self.con = psycopg2.connect(config.postgresql)

        self.client_id = config.client_id

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