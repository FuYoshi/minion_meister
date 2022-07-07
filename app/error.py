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
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class InsertError(DatabaseError):
    """ The base exception type for database errors involving insert. """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class InsertUserError(InsertError):
    """ Exception raised when inserting a user that does exist. """
    def __init__(self, user):
        self.user = user
        super().__init__(f'User {user} is already participating.')


class InsertAdminError(InsertError):
    """ Exception raised when inserting an admin that does exist. """
    def __init__(self, user):
        self.user = user
        super().__init__(f'User {user} is already admin.')


class DeleteError(DatabaseError):
    """ The base exception type for database errors involving delete. """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class DeleteUserError(DeleteError):
    """ Exception raised when inserting a user that does exist. """
    def __init__(self, user):
        self.user = user
        super().__init__(f'User {user} is not participating.')


class DeleteAdminError(DeleteError):
    """ Exception raised when inserting an admin that does exist. """
    def __init__(self, user):
        self.user = user
        super().__init__(f'User {user} is not an admin.')


class SelectError(DatabaseError):
    """ The base exception type for database errors involving select. """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class NoMinionMeisterError(SelectError):
    """ Exception raised when there is no history of Minion Meisters. """
    def __init__(self):
        super().__init__('There are no previous Minion Meisters.')


class NoParticipantsError(SelectError):
    """ Exception raised when there are no participants. """
    def __init__(self):
        super().__init__('There are no participants.')


class NoAdminsError(SelectError):
    """ Exception raised when there are no admins. """
    def __init__(self):
        super().__init__('There are no admins.')


class InvalidDateError(UserInputError):
    """ Exception raised date is not the right format (YYYY-MM-DD). """
    def __init__(self, date):
        self.date = date
        super().__init__(f'Date {date} is not of format YYYY-MM-DD.')
