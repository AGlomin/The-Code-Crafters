import csv
import os
import json

FILE_PATH = "telemetry/telemetry.csv"

def write_event(event):

    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:

        fieldnames = [
            "event_id",
            "timestamp",
            "event_type",
            "level_id",
            "stage_id",
            "session_id",
            "user_id",
            "config_id",
            "payload",
            "data_quality_flags"
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists or os.stat(FILE_PATH).st_size == 0:
            writer.writeheader()

        writer.writerow({
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "level_id": event.level_id,
            "stage_id": event.stage_id,
            "session_id": event.session_id,
            "user_id": event.user_id,
            "config_id": event.config_id,
            "payload": event.payload,
            "data_quality_flags": event.data_quality_flags
        })