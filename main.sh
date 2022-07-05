#!/bin/sh
# Filename: run.sh
# Authors:  Yoshi Fu
# Project:  Minion Meister Discord Bot
# Date:     July 24th 2022

# Summary:
# - Create database.
# - Load backup from file.
# - Start Discord bot.

echo setting up database...
python3 create_database.py
echo finished setting up database

echo starting Discord bot...
python3 bot.py
