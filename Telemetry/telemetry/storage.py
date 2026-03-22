import csv
import os
import json

FILE_PATH = "telemetry/telemetry.csv"

FIELDS = [
    "timestamp",
    "event_type",
    "level_id",
    "stage_id",
    "session_id",
    "user_id",
    "config_id",
    "payload",
    "data_quality_flags",
]


def write_event(event):
    # ensure telemetry directory exists
    os.makedirs(os.path.dirname(FILE_PATH) or ".", exist_ok=True)

    # check whether file already exists
    file_exists = os.path.isfile(FILE_PATH)
    file_empty = (not file_exists) or os.path.getsize(FILE_PATH) == 0

    # open file in append mode to preserve previous telemetry
    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        # if file is new or empty, write header row first
        if file_empty:
            writer.writeheader()

        # write event data to CSV
        writer.writerow({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "level_id": event.level_id,
            "stage_id": event.stage_id,
            "session_id": event.session_id,
            "user_id": event.user_id,
            "config_id": event.config_id,
            "payload": json.dumps(event.payload),
            "data_quality_flags": json.dumps(event.data_quality_flags),
        })