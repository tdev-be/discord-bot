from discord.ext import commands
from collections import Counter
from utils import checks
from utils.db.datatype import *

import logging
import discord
import datetime
import psutil

from config import LOGGING_CHANNEL

client = discord.Client()
log = logging.getLogger(__name__)

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret

class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        ban_list = await ctx.guild.bans()

        try:
            member_id = int(argument, base=10)
            entity = discord.utils.find(lambda u: u.user.id == member_id, ban_list)
        except ValueError:
            entity = discord.utils.find(lambda u: str(u.user.name) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument("Not a valid previously-banned member.")
        return entity

class utility:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(hidden=False)
    async def ping(self, ctx):
        await ctx.send('pong !')

    @commands.command(hidden=False)
    async def back(self, ctx):
        '''Set an afk reason'''
        afk_back(str(ctx.guild.id), ctx.author.name)
        await ctx.send(f"{ctx.author.mention} is back !")

    @commands.command(hidden=False)
    async def afk(self, ctx):
        reason = "Afk"
        if len(ctx.message.content.split(' ')[1:]):
            reason = " ".join(ctx.message.content.split(' ')[1:])
        afk_reason(str(ctx.guild.id), ctx.author.name, reason)
        await ctx.send(f"{ctx.author.name} is afk :\"{reason}\"")

    @client.event
    async def on_message(self, message: discord.Message):
        if message.author == message.guild.me:
            return
        for mention in message.mentions:
            reason = is_afk(message.guild.id, mention.name)
            if reason:
               await message.channel.send( f'{mention.name} is AFK : {reason}')

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: ActionReason = None):
        """Kicks a member from the server.

        In order for this to work, the bot must have Kick Member permissions.

        To use this command you must have Kick Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await member.kick(reason=reason)
        await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: ActionReason = None):
        """Ban a member from the server.

        In order for this to work, the bot must have Ban Member permissions.

        To use this command you must have Ban Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await member.ban(reason=reason)
        await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason: ActionReason = None):
        """Unbans a member from the server.

        You can pass either the ID of the banned member or the Name#Discrim
        combination of the member. Typically the ID is easiest to use.

        In order for this to work, the bot must have Ban Member permissions.

        To use this command you must have Ban Members permissions.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.unban(member.user, reason=reason)
        if member.reason:
            await ctx.send(f'Unbanned {member.user} (ID: {member.user.id}), previously banned for {member.reason}.')
        else:
            await ctx.send(f'Unbanned {member.user} (ID: {member.user.id}).')

    async def _full_cleanup_strategy(self, ctx, search):
        prefixes = tuple('!') # thanks startswith

        def check(m):
            return m.pinned == False

        deleted = await ctx.channel.purge(limit=search, check=check, before=ctx.message)
        return Counter(m.author.display_name for m in deleted)

    @commands.command()
    @checks.has_permissions(manage_messages=True)
    async def clear(self, ctx, search=100):
        """Cleans up the bot's messages from the channel.

        If a search number is specified, it searches that many messages to delete.
        If the bot has Manage Messages permissions then it will try to delete
        messages that look like they invoked the bot as well.

        After the cleanup is completed, the bot will send you a message with
        which people got their messages deleted and their count. This is useful
        to see which users are spammers.

        You must have Manage Messages permission to use this.
        """

        strategy = self._full_cleanup_strategy

        spammers = await strategy(ctx, search)
        deleted = sum(spammers.values())
        messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
        if deleted:
            messages.append('')
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f'- **{author}**: {count}' for author, count in spammers)

        await ctx.message.delete()
        await ctx.send('\n'.join(messages), delete_after=10)

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
    if not hasattr(bot, 'command_stats'):
        bot.command_stats = Counter()

    if not hasattr(bot, 'socket_stats'):
        bot.socket_stats = Counter()

    bot.add_cog(utility(bot))
    commands.Bot.on_error = on_error