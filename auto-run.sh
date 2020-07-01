#!/bin/bash

date
cd /home/jondwoo_gmail_com/sermonupdate
git pull
python3 run.py
firebase deploy
