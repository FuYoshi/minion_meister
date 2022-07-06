#!/usr/bin/env python3
"""
Filename: test_minion_meister.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Contains unit tets for the database.
- [TODO]
"""

import pytest
from minion_meister import MinionMeister


def test_connection(mm: MinionMeister):
    assert mm.database
    assert isinstance(mm.database, str)
    assert mm.database.endswith('.db')


@pytest.mark.asyncio
async def test_add_user(mm: MinionMeister, mm_data: dict):
    await mm.add_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert await mm.is_user(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_select_winner(mm: MinionMeister, mm_data: dict):
    uid = await mm.select_winner(mm_data['sid'])
    assert uid == mm_data['uid']


@pytest.mark.asyncio
async def test_show_participants(mm: MinionMeister, mm_data: dict):
    names = await mm.show_participants(mm_data['sid'])
    assert isinstance(names, list)
    assert isinstance(names[0], str)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_show_history(mm: MinionMeister, mm_data: dict):
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
async def test_show_count(mm: MinionMeister, mm_data: dict):
    counts = await mm.show_count(mm_data['sid'])
    assert isinstance(counts, tuple)
    assert len(counts) == 2
    names, count = counts
    assert isinstance(names, tuple)
    assert isinstance(count, tuple)
    assert isinstance(names[0], str)
    assert isinstance(count[0], int)
    assert mm_data['name'] in names
    assert count[names.index(mm_data['name'])] >= 1


@pytest.mark.asyncio
async def test_insert_history(mm: MinionMeister, mm_data: dict):
    await mm.insert_history(mm_data['sid'], mm_data['uid'], mm_data['date'])
    names = await mm.show_participants(mm_data['sid'])
    assert mm_data['name'] in names
    names, dates = await mm.show_history(mm_data['sid'], mm_data['limit'])
    assert mm_data['name'] in names
    assert mm_data['date'] in dates
    names, count = await mm.show_count(mm_data['sid'])
    assert mm_data['name'] in names
    assert count[names.index(mm_data['name'])] >= 2


@pytest.mark.asyncio
async def test_admin_user(mm: MinionMeister, mm_data: dict):
    await mm.admin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert await mm.is_admin(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_show_admins(mm: MinionMeister, mm_data: dict):
    names = await mm.show_admins(mm_data['sid'])
    assert isinstance(names, list)
    assert isinstance(names[0], str)
    assert mm_data['name'] in names


@pytest.mark.asyncio
async def test_unadmin_user(mm: MinionMeister, mm_data: dict):
    await mm.unadmin_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert not await mm.is_admin(mm_data['sid'], mm_data['uid'])


@pytest.mark.asyncio
async def test_remove_user(mm: MinionMeister, mm_data: dict):
    await mm.remove_user(mm_data['sid'], mm_data['uid'], mm_data['name'])
    assert not await mm.is_user(mm_data['sid'], mm_data['uid'])
