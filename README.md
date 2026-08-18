# Mudae Reset Reminder Bot

Pings a role every hour at :21 PH time, when Mudae pulls reset.

## Features

- Auto-reminder at every :21 (Philippines time)
- `!subscribe` — get the reminder role
- `!unsubscribe` — remove the reminder role
- `!remindon` / `!remindoff` — toggle reminders for the whole server
- `!remindstatus` — check current time and reminder status

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your bot token, channel ID, and role ID
3. `python bot.py`

