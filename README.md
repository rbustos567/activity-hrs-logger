# Activity-hrs-logger

A lightweight Python CLI tool to log daily activity hours into JSON Lines (`.json`) files and compute cumulative totals. Uses only the Python standard library with zero external dependencies.

## Features

- **Append-only JSON storage**: Stores one `{ "YYYY-MM-DD": hours }` object per line.
- **Duplicate dates supported**: Log multiple sessions on the same day without overwriting previous entries.
- **Automatic rounding**: Rounds logged hours to one decimal place.
- **Zero dependencies**: Runs on standard Python 3.10+.

## Data Format

Each activity is stored in its own file, with one JSON object per line:

```json
{"2026-11-18": 1.5}
{"2026-11-18": 0.8}
{"2026-11-19": 2.0}
```

---

## Installation
1. Clone the repository and make the script executable
```bash
git clone https://github.com/rbustos567/activity-hrs-logger.git
cd activity-hrs-logger
chmod +x log_activity_hrs.py
```
---
## Usage

### Log hours for today
```bash
python3 log_activity_hrs.py --add 1.5 --file ~/activity/reading.json
```
### Log hours for a specific date
```bash
python3 log_activity_hrs.py --add 0.75 --file ~/activity/running.json
```
### View total hours for an activity
```bash
python3 log_activity_hrs.py --view-total-time ~/activity/reading.json
```
### Output:
```bash
Total hrs: 1.5
```
