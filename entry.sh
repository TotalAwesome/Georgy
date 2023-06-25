#!/bin/bash

if ! pgrep -f start_bot
then 
    /opt/itkambot/venv/bin/python /opt/itkambot/manage.py start_bot >> /tmp/georgy_bot.log 2>&1 &
fi
