import csv
import os
import json

FILE_PATH = "telemetry/telemetry.csv"

FIELDS = [
    "timestamp",
    "event_type",
    "stage_id",
    "session_id",
    "user_id",
    "payload",
    "data_quality_flags",
]


def write_event(event):

    os.makedirs("telemetry", exist_ok=True)
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
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
    stage_id=1,
    payload={
        "attacker_id": "player_1",
        "target_id": "enemy_2",
        "damage": 3
    }
)

"""