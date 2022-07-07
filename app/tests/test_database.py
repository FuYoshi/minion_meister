#!/usr/bin/env python3
"""
Filename: test_database.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Contains unit tests for the database.
- [TODO]
"""


def test_connection(db_conn):
    """ Test if the database connection fixture works. """
    try:
        _ = db_conn.cursor()
        assert True
    except AttributeError:
        assert False


def test_users_table(db_conn):
    """ Test if the users table is of type (int, int, str). """
    cur = db_conn.cursor()
    cur.execute(
        "SELECT * "
        "FROM users"
    )
    db_conn.commit()
    for sid, uid, name in cur:
        assert isinstance(sid, int)
        assert isinstance(uid, int)
        assert isinstance(name, str)


def test_history_table(db_conn):
    """ Test if the history table is of type (int, int, int, str). """
    cur = db_conn.cursor()
    cur.execute(
        "SELECT * "
        "FROM history"
    )
    db_conn.commit()

    for hid, sid, uid, date in cur:
        assert isinstance(hid, int)
        assert isinstance(sid, int)
        assert isinstance(uid, int)
        assert isinstance(date, str)


def test_counts_table(db_conn):
    """ Test if the counts table is of type (int, int, int). """
    cur = db_conn.cursor()
    cur.execute(
        "SELECT * "
        "FROM counts"
    )
    db_conn.commit()

    for sid, uid, count in cur:
        assert isinstance(sid, int)
        assert isinstance(uid, int)
        assert isinstance(count, int)


def test_admins_table(db_conn):
    """ Test if the admins table is of type (int, int). """
    cur = db_conn.cursor()
    cur.execute(
        "SELECT * "
        "FROM admins"
    )
    db_conn.commit()

    for sid, uid in cur:
        assert isinstance(sid, int)
        assert isinstance(uid, int)
