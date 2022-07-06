#!/usr/bin/env python3
"""
Filename: conftest.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Contains test fixtures for the different test cases.
- [TODO]
"""

import sqlite3

import pytest
from minion_meister import MinionMeister
from tools import get_database


@pytest.fixture(scope='function')
def db_conn():
    conn = sqlite3.connect(get_database())

    yield conn

    conn.close()


@pytest.fixture(scope='function')
def mm():
    MM = MinionMeister(get_database())
    return MM


@pytest.fixture(scope='function')
def mm_data():
    dic = {
        'sid': 111111,
        'uid': 000000,
        'name': 'jesus',
        'date': '0000-00-00',
        'limit': 5
    }
    return dic
