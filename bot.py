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

import discord
from discord.ext import commands
from dotenv import load_dotenv

from error import (DeleteError, InsertError, InvalidDateError, NoAdminsError,
                   NoMinionMeisterError, NoParticipantsError)
from minion_meister import MinionMeister
from tools import is_date
from webserver import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_FILE = os.getenv('DATABASE_FILE')
OWNER = os.getenv('OWNER_ID')


bot = commands.Bot(command_prefix='!')
MM = MinionMeister(DB_FILE)


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


def is_admin():
    """ Check if the user is banned from using commands. """
    async def predicate(ctx):
        return await MM.is_admin(ctx.guild.id, ctx.author.id)
    return commands.check(predicate)


@bot.command(name='add', help="Add user to participants.")
@commands.check_any(commands.is_owner(), is_admin())
async def add_member(ctx, user: discord.Member = None, name: str = None):
    """ Add user to the participants list.

        Parameters:
            :user: discord.Member, optional
                user to be added to the participants list.
                If :user: is not given, add the author.
            :name: str, optional
                name of the user to be added (default: display_name).
    """
    if user is None:
        user = ctx.author

    if name is None:
        name = user.display_name

    await MM.add_user(ctx.guild.id, user.id, name)
    await ctx.send(f'User {name} is now participating.')


@bot.command(name='remove', help="Remove user from participants.")
@commands.check_any(commands.is_owner(), is_admin())
async def remove_member(ctx, user: discord.Member = None):
    """ Remove user from the participants list.

        Parameters:
            :user: discord.Member, optional
                user to be removed from the participants list.
                If :user: is not given, remove the author.
    """
    if user is None:
        user = ctx.author

    await MM.remove_user(ctx.guild.id, user.id, user.display_name)
    await ctx.send(f'User {user.display_name} is no longer participating.')


@bot.command(name='roll', help="Select winner from participants.")
@commands.check_any(commands.is_owner(), is_admin())
async def select_winner(ctx):
    """ Select a random winner from the participants list. """
    user_id = await MM.select_winner(ctx.guild.id)
    await ctx.send(f'The Minion Meister is now <@{user_id}>')


@bot.command(name='list', help="Show list with all participants.")
async def list_participants(ctx):
    """ Show a list with all participants. """
    participants = await MM.show_participants(ctx.guild.id)
    participants_str = '\n'.join(participants)
    await ctx.send(f'Participants:\n{participants_str}')


@bot.command(name='history', help="Show list with recent Minion Meisters.")
async def show_history(ctx, limit: int = 5):
    """ Show a list with previous Minion Masters.

        Parameters:
            :limit: int, optional
                amount of history records to show (default: 5).
    """
    names, dates = await MM.show_history(ctx.guild.id, limit)

    history_str = ""
    for i, _ in enumerate(names):
        history_str += f"\n{dates[i]}, {names[i]}"
    await ctx.send(f'Previous Minion Meisters:{history_str}')


@bot.command(name='count',
             help="Show Minion Meister frequency of participants.")
async def show_count(ctx):
    """ Show the Minion Meister frequency count. """
    names, count = await MM.show_count(ctx.guild.id)

    count_str = ""
    for i, _ in enumerate(names):
        count_str += f"\n{count[i]}, {names[i]}"
    await ctx.send(f'Times selected as Minion Meister:{count_str}')


@bot.command(name='insert', hidden=True,
             help="Insert Minion Meister into history.")
@commands.is_owner()
async def insert_history(ctx, user: discord.Member, date: str,
                         name: str = None):
    """ Insert record into history where user became Minion Meister on date.

        Parameters:
            :user: discord.Member, required
                user to make Minion Meister
            :date: str, required
                date user is made Minion Meister (format: yyyy-mm-dd).
            :name: str, optional
                name of the user to be added (default: display_name).
    """
    if name is None:
        name = user.display_name

    if not await MM.is_user(ctx.guild.id, user.id):
        await MM.add_user(ctx.guild.id, user.id, name)

    if not is_date(date):
        raise InvalidDateError(date)

    await MM.insert_history(ctx.guild.id, user.id, date)


@bot.command(name='admin_list', help="Show list with all admins.")
async def show_admins(ctx):
    """ Show a list with all admins. """
    admins = await MM.show_admins(ctx.guild.id)
    admins_str = '\n'.join(admins)
    await ctx.send(f'Admins:\n{admins_str}')


@bot.command(name='admin', hidden=True,
             help="Give permissions to user for certain commands.")
@commands.is_owner()
async def admin(ctx, user: discord.Member):
    """ Add a user to the admins of the server.

        Parameters:
            :user: discord.Member, required
                user to add to the admins of the server.
    """
    await MM.admin_user(ctx.guild.id, user.id, user.display_name)
    await ctx.send(f'User {user.display_name} is now an admin.')


@bot.command(name='unadmin', hidden=True,
             help="Take permissions from user for certain commands.")
@commands.is_owner()
async def unadmin(ctx, user: discord.Member):
    """ Remove a user from the admins of the server.

        Parameters:
            :user: discord.Member, required
                user to remove from the admins of the server.
    """
    await MM.unadmin_user(ctx.guild.id, user.id, user.display_name)
    await ctx.send(f'User {user.display_name} is no longer an admin.')


keep_alive()
bot.run(TOKEN)
