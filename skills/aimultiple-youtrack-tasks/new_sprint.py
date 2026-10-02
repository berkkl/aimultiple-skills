#!/usr/bin/env python3
"""Create this ISO week's sprint on the RES board and make it the default.

YouTrack has no recurring sprints and the MCP cannot manage sprints, so the
board owner runs this every Monday (session-pm checkin does it for Berkk).

  python3 new_sprint.py            # current ISO week
  python3 new_sprint.py --week 2026-W42
  python3 new_sprint.py --dry      # print the plan, change nothing

Creating the sprint with previousSprint moves the unresolved cards of the
previous sprint into the new one. New cards then land in the new sprint
because it is the board's default sprint.

Token: env YOUTRACK_TOKEN, else the youtrack MCP header in ~/.claude.json.
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

BASE = "https://aimresearcher.youtrack.cloud"
BOARD_ID = "195-7"  # "AIM Researcher" board, project RES
TZ = timezone(timedelta(hours=3))  # Europe/Istanbul, no DST


def token() -> str:
    if os.environ.get("YOUTRACK_TOKEN"):
        return os.environ["YOUTRACK_TOKEN"]
    with open(os.path.expanduser("~/.claude.json")) as f:
        cfg = json.load(f)
    servers = [cfg.get("mcpServers", {})] + [
        p.get("mcpServers", {}) for p in cfg.get("projects", {}).values()
    ]
    for s in servers:
        yt = s.get("youtrack")
        if yt and "headers" in yt:
            return yt["headers"]["Authorization"].split(" ", 1)[1]
    sys.exit("No YouTrack token: set YOUTRACK_TOKEN or add the youtrack MCP.")


def call(method: str, path: str, body: dict | None = None):
    req = urllib.request.Request(
        BASE + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {token()}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def week_bounds(label: str) -> tuple[int, int]:
    year, week = label.split("-W")
    monday = date.fromisocalendar(int(year), int(week), 1)
    start = datetime(monday.year, monday.month, monday.day, tzinfo=TZ)
    finish = start + timedelta(days=7) - timedelta(seconds=1)
    return int(start.timestamp() * 1000), int(finish.timestamp() * 1000)


def main() -> None:
    ap = argparse.ArgumentParser()
    y, w, _ = date.today().isocalendar()
    ap.add_argument("--week", default=f"{y}-W{w:02d}")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    fields = "sprints(id,name,start,finish,isDefault)"
    sprints = call("GET", f"/api/agiles/{BOARD_ID}?fields={fields}")["sprints"]
    existing = next((s for s in sprints if s["name"] == args.week), None)
    start, finish = week_bounds(args.week)

    if existing:
        print(f"{args.week} exists (default={existing['isDefault']}).")
        if not existing["isDefault"] and not args.dry:
            call("POST", f"/api/agiles/{BOARD_ID}/sprints/{existing['id']}", {"isDefault": True})
    else:
        dated = [s for s in sprints if s.get("finish")]
        prev = max(dated, key=lambda s: s["finish"]) if dated else None
        if prev and start <= prev["start"]:
            print(f"Latest sprint {prev['name']} is not older than {args.week}. Nothing to do.")
            return
        body ={"name": args.week, "start": start, "finish": finish, "isDefault": True}
        if prev:
            body["previousSprint"] = {"id": prev["id"]}
        print(f"Create {args.week}, carry over unresolved cards from {prev['name'] if prev else 'none'}.")
        if not args.dry:
            call("POST", f"/api/agiles/{BOARD_ID}/sprints?fields=id", body)

    if args.dry:
        return
    check = call(
        "GET",
        f"/api/agiles/{BOARD_ID}?fields=sprintsSettings(defaultSprint(name)),"
        "sprints(name,issues(idReadable))",
    )
    default = (check["sprintsSettings"].get("defaultSprint") or {}).get("name")
    cards = next((s.get("issues", []) for s in check["sprints"] if s["name"] == args.week), [])
    print(f"Default sprint: {default}. Cards in {args.week}: {len(cards)}.")
    if default != args.week:
        sys.exit("Default sprint did not switch. Set it in Board settings > Sprints.")


if __name__ == "__main__":
    main()
