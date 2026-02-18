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
    "payload",
    "data_quality_flags",
]


def write_event(event):

    os.makedirs(os.path.dirname(FILE_PATH) or ".", exist_ok=True)
    file_exists = os.path.isfile(FILE_PATH)
    file_empty = os.path.getsize(FILE_PATH) == 0

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if (not file_exists) or file_empty:
            writer.writeheader()

        writer.writerow({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "level_id": event.level_id,
            "stage_id": event.stage_id,
            "session_id": event.session_id,
            "user_id": event.user_id,
            "payload": json.dumps(event.payload),
            "data_quality_flags": json.dumps(event.data_quality_flags),
        })


#how to use in mainplay:
"""
log_event(
    event_type="character_attack",
    level_id,
    stage_id,
    payload={
        "attacker_id": "player_1",
        "target_id": "enemy_2",
        "damage": 3
    }
)

"""
