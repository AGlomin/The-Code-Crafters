from telemetry.events import TelemetryEvent
from telemetry.validator import validate_event, TelemetryValidationError
from telemetry.storage import write_event


def log_event(event_type: str, stage_id: int, payload: dict):
    event = TelemetryEvent.create(
        event_type=event_type,
        stage_id=stage_id,
        payload=payload
    )

    try:
        validate_event(event)
        write_event(event)
    except TelemetryValidationError as e:
        print(f"[Telemetry Error] {e}")

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