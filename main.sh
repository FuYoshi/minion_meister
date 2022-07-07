#!/bin/sh
# Filename: run.sh
# Authors:  Yoshi Fu
# Project:  Minion Meister Discord Bot
# Date:     July 24th 2022

# Summary:
# - Create database.
# - Start Discord bot.

echo installing requirements...
pip3 install -r requirements.txt
echo finished installing requirements.

echo setting up database...
python3 database/create_database.py
echo finished setting up database

echo starting Discord bot...
python3 app/bot.py -w
