#!/usr/bin/env python3
"""
Filename: tools.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Function to read from database.
- Function to push to database.
- [TODO]
"""

import argparse
import os
from datetime import datetime

from aiosqlite import connect
from dotenv import load_dotenv


def argparser():
    """ Check for commandline arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', action='store_true',
                        help="Delete current database")
    parser.add_argument('-w', '--webserver', action='store_true',
                        help="Start webserver")
    args = parser.parse_args()
    return args


async def read_from_db(db_filename: str, sql: str, values=None) -> list:
    """ Perform a SQL Query that reads from the database.

        SQL injection is prevented by using bound parameter execution.
        SQL statements are only valid in the SQL part of the query and
        therefore not in the values part.

        Params:
            database_filename: str, required
                filename of the database for aiosqlite to connect to.
            sql: str, required
                sql part of query with optional named colon parameters.
            values: dict or tuple, optional
                dictionary that maps named colon parameter to value.
    """
    if values is None:
        values = dict()

    con = await connect(db_filename)
    cur = await con.cursor()

    await cur.execute(sql, values)
    await con.commit()

    res = await cur.fetchall()
    res = [line for line in res]

    await cur.close()
    await con.close()

    return res


async def push_to_db(db_filename: str, sql: str, values=None) -> None:
    """ Perform a SQL Query that alters the database.

        SQL injection is prevented by using bound parameter execution.
        SQL statements are only valid in the SQL part of the query and
        therefore not in the values part.

        Params:
            database_filename: str, required
                filename of the database for aiosqlite to connect to.
            sql: str, required
                sql part of query with optional named colon parameters.
            values: dict or tuple, optional
                dictionary that maps named colon parameter to value.
    """
    if values is None:
        values = dict()

    con = await connect(db_filename)
    cur = await con.cursor()

    await cur.execute(sql, values)
    await con.commit()

    await cur.close()
    await con.close()


def is_date(date: str) -> bool:
    """ Check if the date is the right format (yyyy-mm-dd).

        Parameters:
            :date: str, required
                string containing a date.

        Returns:
            bool
    """
    try:
        return bool(datetime.strptime(date, '%Y-%m-%d'))
    except ValueError:
        return False


def get_database():
    """ Load the database file environment variable and return it. """
    load_dotenv()
    DB_FILE = os.getenv('DATABASE_FILE')
    return DB_FILE
