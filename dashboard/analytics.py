import csv
from collections import defaultdict

TELEMETRY_FILE = "Telemetry/telemetry.csv"

def load_events():
    #will load from csv
    events = []
    try:
        with open(TELEMETRY_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                events.append(row)
    except FileNotFoundError: #NEED TO ADD CLASS
        pass 
    return events

def computer_funnel(events):
    funnel = defaultdict(int)
    for e in events:
        if etype == "stage_start":
            funnel["Stage Starts"] += 1
        elif etype == "stage_complete":
            funnel["Stage Completes"] += 1
        elif etype == "stage_fail":
            funnel["Stage Fails"] += 1
        elif etype == "quit":
            funnel["Quits"] +=1
    return funnel

def stage_failures(events):
    #counts failures perstage
    fails = defaultdict(int)

    for e in events:
        if e.get("event_type") == "stage_fail":
            fails[e.get("stage_id")] += 1
    return fails