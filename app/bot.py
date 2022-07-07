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

import argparse
import os

from discord.ext import commands
from dotenv import load_dotenv

import webserver

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, err):
    """ Send the error message in text channel. """
    await ctx.send(err)


def argparser():
    """ Check for commandline arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--webserver', action='store_true',
                        help="Start webserver")
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    cogs = [
        'cogs.member',
        'cogs.admin',
        'cogs.owner'
    ]

    for cog in cogs:
        bot.load_extension(cog)

    args = argparser()
    if args.webserver:
        webserver.keep_alive()

    bot.run(TOKEN)
