import csv
import json
from collections import defaultdict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Try both possible repo layouts (case sensitive on some systems)
CANDIDATES = [
    os.path.join(PROJECT_ROOT, "telemetry", "telemetry.csv"),
    os.path.join(PROJECT_ROOT, "Telemetry", "telemetry.csv"),
]

TELEMETRY_PATH = next((p for p in CANDIDATES if os.path.exists(p)), CANDIDATES[0])


def load_events():
    events = []
    try:
        with open(TELEMETRY_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # robust int parsing (handles "0 but a string")
                try:
                    row["level_id"] = int(str(row.get("level_id", 0)).split()[0])
                except:
                    row["level_id"] = 0

                try:
                    row["stage_id"] = int(str(row.get("stage_id", 0)).split()[0])
                except:
                    row["stage_id"] = 0

                # decode json fields
                try:
                    row["payload"] = json.loads(row.get("payload", "{}"))
                except:
                    row["payload"] = {}

                try:
                    row["data_quality_flags"] = json.loads(row.get("data_quality_flags", "[]"))
                except:
                    row["data_quality_flags"] = []

                events.append(row)

    except FileNotFoundError:
        pass

    return events


def compute_funnel(events):
    funnel = defaultdict(int)

    for e in events:
        etype = e.get("event_type")

        if etype == "stage_start":
            funnel["Stage Starts"] += 1
        elif etype == "stage_complete":
            funnel["Stage Completes"] += 1
        elif etype == "stage_fail":
            funnel["Stage Fails"] += 1
        elif etype == "session_end":
            funnel["Sessions Ended"] += 1
        elif etype == "level_start":
            funnel["Level Starts"] += 1
        elif etype == "level_complete":
            funnel["Level Completes"] += 1

    stage_starts = funnel["Stage Starts"]
    stage_completes = funnel["Stage Completes"]

    if stage_starts > 0:
        funnel["Completion Rate %"] = round(100 * stage_completes / stage_starts, 1)
    else:
        funnel["Completion Rate %"] = 0.0

    return dict(funnel)


def stage_failures(events):
    failures = defaultdict(int)

    for e in events:
        if e.get("event_type") == "stage_fail":
            level = e.get("level_id")
            stage = e.get("stage_id")
            failures[(level, stage)] += 1

    return dict(failures)
