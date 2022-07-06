#!/usr/bin/env python3
"""
Filename: database.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- Create database minion_meister.
- Create tables servers, users, history.
- [TODO]
"""

import asyncio
import os

import aiosqlite

from tools import argparser, get_database

DB_FILE = get_database()


async def create_users_table(con, cur) -> None:
    """ Create the users table. """
    await cur.execute(
        "CREATE TABLE IF NOT EXISTS users("
        "id INTEGER NOT NULL, "
        "server INTEGER NOT NULL, "
        "name VARCHAR(32), "
        "PRIMARY KEY (id, server)"
        ");"
    )
    await con.commit()


async def create_history_table(con, cur) -> None:
    """ Create the history table. """
    await cur.execute(
        "CREATE TABLE IF NOT EXISTS history("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "server INTEGER NOT NULL, "
        "user INTEGER NOT NULL, "
        "date TEXT(32) NOT NULL, "
        "FOREIGN KEY (user) REFERENCES users(id)"
        ");"
    )
    await con.commit()


async def create_counts_table(con, cur) -> None:
    """ Create the counts table. """
    await cur.execute(
        "CREATE TABLE IF NOT EXISTS counts("
        "server INTEGER NOT NULL, "
        "user INTEGER NOT NULL, "
        "count INTEGER NOT NULL, "
        "PRIMARY KEY (server, user), "
        "FOREIGN KEY (user) REFERENCES users(id)"
        ");"
    )
    await con.commit()


async def create_admins_table(con, cur) -> None:
    """ Create the admins table. """
    await cur.execute(
        "CREATE TABLE IF NOT EXISTS admins("
        "server INTEGER NOT NULL, "
        "user INTEGER NOT NULL, "
        "PRIMARY KEY (server, user), "
        "FOREIGN KEY (user) REFERENCES users(id)"
        ");"
    )
    await con.commit()


async def main():
    args = argparser()

    if args.delete:
        os.remove(DB_FILE)

    con = await aiosqlite.connect(DB_FILE)
    cur = await con.cursor()

    await create_users_table(con, cur)
    await create_history_table(con, cur)
    await create_counts_table(con, cur)
    await create_admins_table(con, cur)

    await cur.close()
    await con.close()


if __name__ == "__main__":
    asyncio.run(main())
