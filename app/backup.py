#!/usr/bin/env python3
"""
Filename: backup.py
Authors:  Yoshi Fu
Date:     July 24th 2022

Summary:
- Backup the records of the trampeltier Discord server.
- [TODO]
"""

import asyncio
import os

from dotenv import load_dotenv

import minion_meister

load_dotenv()
DB_FILE = os.getenv('DATABASE_FILE')


MM = minion_meister.MinionMeister(DB_FILE)


async def add_participants(server_id: int):
    await MM.add_user(server_id, 284044128449462272, 'Jord')
    await MM.add_user(server_id, 174470439848902657, 'Reno')
    await MM.add_user(server_id, 171666048196673536, 'Wouter')
    await MM.add_user(server_id, 400140550503923713, 'Luke')
    await MM.add_user(server_id, 172703726123876353, 'Joppe')
    await MM.add_user(server_id, 476081297777754112, 'Mark')
    await MM.add_user(server_id, 285380929126531072, 'Yoshi')
    await MM.add_user(server_id, 196556170897522688, 'Luka')
    await MM.add_user(server_id, 510416926946754580, 'Evert')
    await MM.add_user(server_id, 175728174712356864, 'Stefan')


async def add_admins(server_id: int):
    await MM.admin_user(server_id, 172703726123876353, 'Joppe')
    await MM.admin_user(server_id, 284044128449462272, 'Jord')


async def insert_records(server_id: int):
    await MM.insert_history(server_id, 172703726123876353, '2022-05-28')
    await MM.insert_history(server_id, 476081297777754112, '2022-06-04')
    await MM.insert_history(server_id, 285380929126531072, '2022-06-11')
    await MM.insert_history(server_id, 196556170897522688, '2022-06-18')
    await MM.insert_history(server_id, 510416926946754580, '2022-06-25')
    await MM.insert_history(server_id, 175728174712356864, '2022-07-02')
    await MM.insert_history(server_id, 174470439848902657, '2022-07-09')
    await MM.insert_history(server_id, 510416926946754580, '2022-07-16')
    await MM.insert_history(server_id, 171666048196673536, '2022-07-23')


async def main():
    server_id = 431135841671315467
    await add_participants(server_id)
    await add_admins(server_id)
    await insert_records(server_id)


if __name__ == "__main__":
    asyncio.run(main())
