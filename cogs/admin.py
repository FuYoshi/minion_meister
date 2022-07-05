#!/usr/bin/env python3
"""
Filename: admin.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- AdminCog class that contains all commands for an admin.
- Check if the command invoker is an admin before executing command.
- [TODO]
"""

import discord
from discord.ext import commands
from minion_meister import MinionMeister
from tools import get_database


class AdminCog(commands.Cog, name='Admin Commands'):
    """ Cog with all the commands of an admin. """
    def __init__(self, bot):
        self.bot = bot
        self.MM = MinionMeister(get_database())

    async def cog_check(self, ctx):
        """ Check if the user is an admin (or the owner of the bot). """
        if await self.bot.is_owner(ctx.author):
            return True
        return await self.MM.is_admin(ctx.guild.id, ctx.author.id)

    @commands.command(name='add_user', hidden=True,
                      help="Add user to participants.")
    async def add_user(self, ctx, user: discord.Member = None,
                       name: str = None):
        """ Add user to the participants list.

            Parameters:
                :user: discord.Member, optional
                    user to be added to the participants list.
                    If :user: is not given, add the author.
                :display_name: str, optional
                    name of the user to be added (default: display_name).
        """
        if user is None:
            user = ctx.author

        if name is None:
            name = user.display_name

        await self.MM.add_user(ctx.guild.id, user.id, name)
        await ctx.send(f'User {name} is now participating.')

    @commands.command(name='remove_user',  hidden=True,
                      help="Remove user from participants.")
    async def remove_user(self, ctx, user: discord.Member = None):
        """ Remove user from the participants list.

            Parameters:
                :user: discord.Member, optional
                    user to be removed from the participants list.
                    If :user: is not given, remove the author.
        """
        if user is None:
            user = ctx.author

        await self.MM.remove_user(ctx.guild.id, user.id, user.display_name)
        await ctx.send(f'User {user.display_name} is no longer participating.')

    @commands.command(name='roll', help="Select winner from participants.")
    async def select_winner(self, ctx):
        """ Select a random winner from the participants list. """
        user_id = await self.MM.select_winner(ctx.guild.id)
        await ctx.send(f'The Minion Meister is now <@{user_id}>')


def setup(bot):
    bot.add_cog(AdminCog(bot))
