# new?/old? version of the file commented out below

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

''' looks like a new version of the file, but spams the console with : [Telemetry Error] dict contains fields not in fieldnames: 'payload', 'config_id'


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
    "config_id" #NEWLY ADDED
    "payload",
    "data_quality_flags",
]


def write_event(event):
    #ensure telemetry directory exists
    os.makedirs(os.path.dirname(FILE_PATH) or ".", exist_ok=True)
    #check whether file already exists
    file_exists = os.path.isfile(FILE_PATH)
    #check if file exists but empty
    file_empty = os.path.getsize(FILE_PATH) == 0

    #open file in append mode to preserve previous telemetry
    with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:
        #create DictWriter with schema
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        #if file is new or empty, write header row first
        if (not file_exists) or file_empty:
            writer.writeheader()
            
        #write event data to CSV
        #complex fields (payload and data_quality_flags) are JSON-encoded
        writer.writerow({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "level_id": event.level_id,
            "stage_id": event.stage_id,
            "session_id": event.session_id,
            "user_id": event.user_id,
            "config_id": event.config_id, #NEWLY ADDED
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
'''
