#!/usr/bin/env python3
"""
Filename: exception.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- All Discord command errors the Discord bot raises.
- [TODO]
"""

from discord.ext.commands import CommandError, UserInputError


class DatabaseError(CommandError):
    """ The base exception type for errors that involve a database. """
    ...


class InsertError(DatabaseError):
    """ Exception raised when inserting a record that does exist. """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)


class DeleteError(DatabaseError):
    """ Exception raised when deleting a record that does not exist. """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)


class NoMinionMeisterError(DatabaseError):
    """ Exception raised when there is no history of Minion Meisters. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoParticipantsError(DatabaseError):
    """ Exception raised when there are no participants. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoAdminsError(DatabaseError):
    """ Exception raised when there are no admins. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidDateError(UserInputError):
    """ Exception raised date is not the right format (yyyy-mm-dd). """
    def __init__(self, date, *args, **kwargs):
        self.date = date
        super().__init__(*args, **kwargs)
