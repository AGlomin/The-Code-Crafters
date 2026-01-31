from telemetry.logger import log_event

log_event(
    event_type="session_start",
    stage_id=0,
    payload={"difficulty": "balanced"}
)

log_event(
    event_type="stage_start",
    stage_id=1,
    payload={}
)

log_event(
    event_type="character_attack",
    stage_id=1,
    payload={
        "attacker_id": "player_1",
        "target_id": "enemy_1",
        "damage": 3
    }
)

log_event(
    event_type="stage_complete",
    stage_id=1,
    payload={"turns_taken": 5}
)
