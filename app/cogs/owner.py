#!/usr/bin/env python3
"""
Filename: owner.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- OwnerCog class that contains all commands for an owner.
- Check if the command invoker is the owner before executing command.
- [TODO]
"""

import discord
import error
import minion_meister
import tools
from discord.ext import commands


class OwnerCog(commands.Cog, name='Owner Commands'):
    """ Cog with all the commands of an owner. """
    def __init__(self, bot):
        self.bot = bot
        self.MM = minion_meister.MinionMeister(tools.get_database())

    async def cog_check(self, ctx):
        """ Check if the user is the owner of the bot. """
        return await self.bot.is_owner(ctx.author)

    @commands.command(name='admin', hidden=True,
                      help="Give permissions to user for certain commands.")
    async def admin(self, ctx, user: discord.Member):
        """ Add a user to the admins of the server.

            Parameters:
                :user: discord.Member, required
                    user to add to the admins of the server.
        """
        await self.MM.admin_user(ctx.guild.id, user.id, user.display_name)
        await ctx.send(f'User {user.display_name} is now an admin.')

    @commands.command(name='unadmin', hidden=True,
                      help="Take permissions from user for certain commands.")
    async def unadmin(self, ctx, user: discord.Member):
        """ Remove a user from the admins of the server.

            Parameters:
                :user: discord.Member, required
                    user to remove from the admins of the server.
        """
        await self.MM.unadmin_user(ctx.guild.id, user.id, user.display_name)
        await ctx.send(f'User {user.display_name} is no longer an admin.')

    @commands.command(name='insert', hidden=True,
                      help="Insert Minion Meister entry into history.")
    async def insert_history(self, ctx, user: discord.Member, date: str,
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

        if not await self.MM.is_user(ctx.guild.id, user.id):
            await self.MM.add_user(ctx.guild.id, user.id, name)

        if not tools.is_date(date):
            raise error.InvalidDateError(date)

        await self.MM.insert_history(ctx.guild.id, user.id, date)

    @commands.command(name='delete', hidden=True,
                      help="Delete Minion Meister entry from history.")
    async def delete_history(self, ctx, user: discord.Member, date: str,
                             name: str = None):
        """ Delete record from history where user became Minion Meister on date.

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

        if not tools.is_date(date):
            raise error.InvalidDateError(date)

        await self.MM.delete_history(ctx.guild.id, user.id, date)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
