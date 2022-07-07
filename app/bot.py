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

import error
import tools
import webserver

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
async def on_command_error(ctx, err):
    """ Send the corresponding notification on command errors. """
    if isinstance(err, commands.MemberNotFound):
        await ctx.send('I could not find that user. Did you mention them?')
    elif isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f'Missing required argument: {err.param.name}.')
    elif isinstance(err, error.InsertError):
        await ctx.send(err.message)
    elif isinstance(err, error.DeleteError):
        await ctx.send(err.message)
    elif isinstance(err, error.NoParticipantsError):
        await ctx.send('There are no participants.')
    elif isinstance(err, error.NoAdminsError):
        await ctx.send('There are no admins.')
    elif isinstance(err, error.NoMinionMeisterError):
        await ctx.send('There are no previous Minion Meisters.')
    elif isinstance(err, error.InvalidDateError):
        await ctx.send(f'Date {err.date} should be of format: <yyyy-mm-dd>.')


if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


args = tools.argparser()
if args.webserver:
    webserver.keep_alive()

bot.run(TOKEN)
