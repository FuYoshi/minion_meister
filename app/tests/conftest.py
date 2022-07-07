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

import os
import sqlite3

import minion_meister
import pytest
from dotenv import load_dotenv

load_dotenv()
DB_FILE = os.getenv('DATABASE_FILE')


@pytest.fixture(scope='function')
def db_conn():
    conn = sqlite3.connect(DB_FILE)

    yield conn

    conn.close()


@pytest.fixture(scope='function')
def mm():
    MM = minion_meister.MinionMeister(DB_FILE)
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
