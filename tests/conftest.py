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
from tools import get_database


@pytest.fixture(scope='function')
def db_conn():
    conn = sqlite3.connect(get_database())

    yield conn

    conn.close()
