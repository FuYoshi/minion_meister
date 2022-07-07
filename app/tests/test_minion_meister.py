#!/usr/bin/env python3
"""
Filename: test_minion_meister.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Contains unit tests for the database.
- [TODO]
"""

import pytest
from discord import DiscordException


def test_connection(mm):
    """ Test if the MinionMeister connection fixture works. """
    assert mm.database
    assert isinstance(mm.database, str)
    assert mm.database.endswith('.db')


@pytest.mark.asyncio
async def test_add_user(mm, mm_data: dict):
    """ Test if a user is added to database. """
    await mm.add_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert await mm.is_user(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_add_user_error(mm, mm_data: dict):
    """ Test if adding the user again, gives InsertError. """
    try:
        await mm.add_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
        assert False
    except DiscordException:
        assert True


@pytest.mark.asyncio
async def test_select_winner(mm, mm_data: dict):
    """ Test if selecting a MinionMeister works. """
    uid = await mm.select_winner(mm_data['sid'])
    assert uid == mm_data['uid']


@pytest.mark.asyncio
async def test_show_participants(mm, mm_data: dict):
    """ Test if listing all participants works. """
    names = await mm.show_participants(mm_data['sid'])
    assert isinstance(names, list)
    assert isinstance(names[0], str)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_show_history(mm, mm_data: dict):
    """ Test if showing history works. """
    history = await mm.show_history(mm_data['sid'], mm_data['limit'])
    assert isinstance(history, tuple)
    assert len(history) == 2
    names, dates = history
    assert isinstance(names, tuple)
    assert isinstance(dates, tuple)
    assert isinstance(names[0], str)
    assert isinstance(dates[0], str)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_show_count(mm, mm_data: dict):
    """ Test if showing counts works. """
    counts = await mm.show_count(mm_data['sid'])
    assert isinstance(counts, tuple)
    assert len(counts) == 2
    names, count = counts
    assert isinstance(names, tuple)
    assert isinstance(count, tuple)
    assert isinstance(names[0], str)
    assert isinstance(count[0], int)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_insert_history(mm, mm_data: dict):
    """ Test if inserting history works. """
    await mm.insert_history(mm_data['sid'], mm_data['uid'], mm_data['date'])
    names = await mm.show_participants(mm_data['sid'])
    assert mm_data['name'] in names
    names, dates = await mm.show_history(mm_data['sid'], mm_data['limit'])
    assert mm_data['name'] in names
    assert mm_data['date'] in dates
    names, _count = await mm.show_count(mm_data['sid'])
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_delete_history(mm, mm_data: dict):
    """ Test if deleting history works. """
    await mm.delete_history(mm_data['sid'], mm_data['uid'], mm_data['date'])
    _names, dates = await mm.show_history(mm_data['sid'], mm_data['limit'])
    assert not mm_data['date'] in dates


@pytest.mark.asyncio
async def test_admin_user(mm, mm_data: dict):
    """ Test if user can be given admin permissions. """
    await mm.admin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert await mm.is_admin(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_admin_user_error(mm, mm_data: dict):
    """ Test if giving user admin permissions again, gives InsertError. """
    try:
        await mm.admin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
        assert False
    except DiscordException:
        assert True


@pytest.mark.asyncio
async def test_show_admins(mm, mm_data: dict):
    """ Test if listing all admins works. """
    names = await mm.show_admins(mm_data['sid'])
    assert isinstance(names, list)
    assert isinstance(names[0], str)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_unadmin_user(mm, mm_data: dict):
    """ Test if taking admin from user works. """
    await mm.unadmin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert not await mm.is_admin(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_unadmin_user_error(mm, mm_data: dict):
    """ Test if taking admin from user again, gives DeleteError. """
    try:
        await mm.unadmin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
        assert False
    except DiscordException:
        assert True


@pytest.mark.asyncio
async def test_remove_user(mm, mm_data: dict):
    """ Test if removing user from database works. """
    await mm.remove_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert not await mm.is_user(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_remove_user_error(mm, mm_data: dict):
    """ Test if removing user from database again, gives DeleteError. """
    try:
        await mm.remove_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
        assert False
    except DiscordException:
        assert True
