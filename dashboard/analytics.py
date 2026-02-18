import csv
import json
from collections import defaultdict

TELEMETRY_FILE = "telemetry/telemetry.csv"


def load_events():
    events = []

    try:
        with open(TELEMETRY_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # normalize types
                row["level_id"] = int(row["level_id"])
                row["stage_id"] = int(row["stage_id"])

                # decode json fields (if using fixed storage)
                try:
                    row["payload"] = json.loads(row["payload"])
                except:
                    row["payload"] = {}

                try:
                    row["data_quality_flags"] = json.loads(row["data_quality_flags"])
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

     # levels
        elif etype == "level_start":
            funnel["Level Starts"] += 1

        elif etype == "level_complete":
            funnel["Level Completes"] += 1

    # derived metric
    stage_starts = funnel["Stage Starts"]
    stage_completes = funnel["Stage Completes"]

    if stage_starts > 0:
        funnel["Completion Rate %"] = round(100 * stage_completes / stage_starts, 1)
    else:
        funnel["Completion Rate %"] = 0

    return dict(funnel)
        
def stage_failures(events):
    failures = defaultdict(int)

    for e in events:
        if e.get("event_type") == "stage_fail":
            level = e.get("level_id")
            stage = e.get("stage_id")
            failures[level, stage] += 1

    return dict(failures)
