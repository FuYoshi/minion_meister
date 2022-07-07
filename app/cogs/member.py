#!/usr/bin/env python3
"""
Filename: members.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- MemberCog class that contains all commands for a member.
- [TODO]
"""

import os

import minion_meister
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DB_FILE = os.getenv('DATABASE_FILE')


class MemberCog(commands.Cog):
    """ Cog with all the commands of a member. """
    def __init__(self, bot):
        self.bot = bot
        self.MM = minion_meister.MinionMeister(DB_FILE)

    @commands.command(name='add',
                      help="Add yourself to participants with name.")
    async def add(self, ctx, name: str = None):
        """ Add the command invoker to the participants list with name.

            Parameters:
                :name: str, optional
                    name of the user for notifications.
        """
        user = ctx.author
        if name is None:
            name = user.display_name

        await self.MM.add_user(ctx.guild.id, user.id, name)
        await ctx.send(f'User {name} is now participating.')

    @commands.command(name='remove', help="Remove yourself from participants.")
    async def remove(self, ctx):
        """ Remove the command invoker from the participants list. """
        user = ctx.author
        await self.MM.remove_user(ctx.guild.id, user.id, user.display_name)
        await ctx.send(f'User {user.display_name} is no longer participating.')

    @commands.command(name='list', help="Show list with all participants.")
    async def list_participants(self, ctx):
        """ Show a list with all participants. """
        participants = await self.MM.show_participants(ctx.guild.id)
        participants_str = '\n'.join(participants)
        await ctx.send(f'Participants:\n{participants_str}')

    @commands.command(name='history',
                      help="Show list with recent Minion Meisters.")
    async def show_history(self, ctx, limit: int = 5):
        """ Show a list with previous Minion Masters.

            Parameters:
                :limit: int, optional
                    amount of history records to show (default: 5).
        """
        names, dates = await self.MM.show_history(ctx.guild.id, limit)

        history_str = ""
        for i, _ in enumerate(names):
            history_str += f"\n{dates[i]}, {names[i]}"
        await ctx.send(f'Previous Minion Meisters:{history_str}')

    @commands.command(name='count',
                      help="Show Minion Meister frequency of participants.")
    async def show_count(self, ctx):
        """ Show the Minion Meister frequency count. """
        names, count = await self.MM.show_count(ctx.guild.id)

        count_str = ""
        for i, _ in enumerate(names):
            count_str += f"\n{count[i]}, {names[i]}"
        await ctx.send(f'Times selected as Minion Meister:{count_str}')

    @commands.command(name='admin_list', help="Show list with all admins.")
    async def show_admins(self, ctx):
        """ Show a list with all admins. """
        admins = await self.MM.show_admins(ctx.guild.id)
        admins_str = '\n'.join(admins)
        await ctx.send(f'Admins:\n{admins_str}')


def setup(bot):
    bot.add_cog(MemberCog(bot))
