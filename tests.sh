#!/bin/sh
# Filename: tests.sh
# Authors:  Yoshi Fu
# Project:  Minion Meister Discord Bot
# Date:     July 24th 2022

# Summary:

echo setting up database...
python3 database/create_database.py
echo finished setting up database

echo starting tests...
pytest -v -s --asyncio-mode=auto
