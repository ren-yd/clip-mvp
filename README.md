# CLIP MVP

A minimal, privacy-first cognitive load monitor.

## What It Does
- Runs in the background on your computer
- Watches typing speed, backspace rate, pauses, and mouse activity
- Computes a 0-10 "Cognitive Load Index" every 10-60 seconds
- Shows a real-time colored dashboard
- Stores history locally in SQLite

## What It NEVER Does
- Records what you type (only timing and backspace count)
- Takes screenshots
- Sends data to the cloud
- Requires internet

## Install

1. Install Python 3.9+
2. Install dependencies:
```bash
pip install -r requirements.txt
>>>>>>> 4247b9a (feat: MVP working - detects cognitive load from typing behavior)
