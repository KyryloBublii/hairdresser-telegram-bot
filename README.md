---
title: Hairdresser Telegram Bot
year: 2026
tags: [python, telegram, telegram-bot, python-telegram-bot, appointment-scheduling, booking, async]
status: complete
cover: photos/main.jpg
---

## What is it

A Telegram bot that lets clients book hairdresser appointments entirely through Telegram's inline keyboard interface. Users pick a service, a date from the next 7 days, and an available time slot — all without leaving the chat.

## Problem it solves

Replaces manual scheduling (phone calls, DMs, paper logs) with a self-service booking system available 24/7. The hairdresser no longer needs to respond to individual booking requests — the bot handles service selection, date/time picking, slot-conflict checking, and cancellations autonomously.

## How it works

- **Hardware:** None — pure software, runs as a Python process on any server or local machine.
- **Software:** Python 3, `python-telegram-bot 21.6` (async), `python-dotenv` for environment config, JSON flat-file storage (`appointments.json`) for persistence.
- **Key challenge:** The booking flow is a 4-step state machine built with `ConversationHandler` (service → date → time → confirm). Taken slots are marked with `✖` in the time picker inline keyboard in real time. A second conflict check runs at the final confirmation step to handle the race condition where two users could simultaneously select the same free slot — the first confirm wins, the second gets a "slot just taken" error and is sent back to `/book`.

## Results

Bot was tested with real bookings: two haircut appointments were successfully created (April 8 and April 10, 2026) via the full conversation flow. All three commands are implemented and functional:

| Command | Description |
|---|---|
| `/book` | Opens the 4-step booking conversation |
| `/my_appointments` | Lists upcoming bookings for the calling user |
| `/cancel_appointment` | Shows a one-tap inline keyboard to cancel any booking |

Services offered: Haircut (45 min), Coloring (2 h), Styling (30 min), Highlights (2.5 h), Trim & Blowout (1 h). Working hours: 09:00–18:00.

## Photos

No photos folder present in the repository.

---

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
BOT_TOKEN=your_telegram_bot_token
```

Run:

```bash
python main.py
```
