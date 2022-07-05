#!/usr/bin/env python3
"""
Filename: bot.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Discord bot that handles commands in the text channel of a server.
- Create a MinionMeister object that can handle database calls.
- Send notification messages on command errors.
- [TODO]
"""

import os

from discord.ext import commands
from dotenv import load_dotenv

from error import (DeleteError, InsertError, InvalidDateError, NoAdminsError,
                   NoMinionMeisterError, NoParticipantsError)
from webserver import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


cogs = [
    'cogs.member',
    'cogs.admin',
    'cogs.owner'
]


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    """ Send the corresponding notification on command errors. """
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('I could not find that user. Did you mention them?')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing required argument: {error.param.name}.')
    elif isinstance(error, InsertError):
        await ctx.send(error.message)
    elif isinstance(error, DeleteError):
        await ctx.send(error.message)
    elif isinstance(error, NoParticipantsError):
        await ctx.send('There are no participants.')
    elif isinstance(error, NoAdminsError):
        await ctx.send('There are no admins.')
    elif isinstance(error, NoMinionMeisterError):
        await ctx.send('There are no previous Minion Meisters.')
    elif isinstance(error, InvalidDateError):
        await ctx.send(f'Date {error.date} should be of format: <yyyy-mm-dd>.')


if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


keep_alive()
bot.run(TOKEN)
