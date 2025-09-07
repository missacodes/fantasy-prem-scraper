# FPL Player Rankings Dashboard

Ranks Fantasy Premier League (FPL) players by **Total Points** with filters for **Club**, **Position**, and **Price (£m)**. Built with Streamlit and AG Grid.

---

## Why this exists
I wanted a compact tool that answers a simple question during transfers: *who has produced the most points within a price range and role, for specific clubs?*

## Features
- Rank by **Total Points** (default sort, descending).
- Filters:
  - **Club** (checkbox list in the grid sidebar and column header).
  - **Position** (Goalkeeper, Defender, Midfielder, Forward).
  - **Price (£m)** slider with 0.1 increments.
- Auto‑refresh: optional timed refresh and a manual **Refresh now** button.
- Vertical scrolling (no pagination).

## How it works
- **Endpoint**: `https://fantasy.premierleague.com/api/bootstrap-static/`
- **Processing**: the app maps team IDs to club names and element types to positions, then exposes:
  - `Name` — first and second name concatenated
  - `Club` — mapped from team ID
  - `Position` — GK/DEF/MID/FWD
  - `Price (£m)` — `now_cost / 10` (one decimal place)
  - `Total Points` — cumulative FPL points
  - `Minutes` — total minutes played
- **Caching**: responses are cached for 300 seconds to avoid unnecessary calls.
- **Auto‑refresh**: interval is user‑configurable in the sidebar (1–15 minutes).

## Local setup
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# (optional) generate a CSV once
python3 main.py

python3 -m streamlit run dashboard.py
```

## Deploy (Streamlit Community Cloud)
- **Repository**: `<your-username>/fpl-scraper-dashboard`
- **Branch**: `main`
- **Main file path**: `dashboard.py`

## Known limits
- Data only updates when FPL updates the endpoint; there is no guaranteed schedule.
- During live matches FPL may throttle or change values; expect brief inconsistencies.
- Layout can vary slightly by browser width; the table is intentionally narrow for readability.



---

_Last updated: 2025-09-07_
