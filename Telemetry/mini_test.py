from Telemetry.telemetry.logger import log_event
import uuid

session_id=str(uuid.uuid4())

log_event(
    event_type="session_start",
    stage_id=0,
    payload={"session_id":session_id,
             "config_id": "balanced",
             "difficulty_label": "balanced"}
)

log_event(
    event_type="stage_start",
    stage_id=1,
    payload={"session_id":session_id,
            "enemy_count": 1,
            "grid_size": "4x5"}
)

log_event(
    event_type="character_attack",
    stage_id=1,
    payload={"session_id":session_id,
            "attacker_id": "player_1",
            "target_id": "enemy_1",
            "damage": 3,
            "attack_range": 1}
)

log_event(
    event_type="stage_complete",
    stage_id=1,
    payload={"session_id":session_id,
             "turns_taken": 5}
)

log_event(
    event_type="turn_start",
    stage_id=1,
    payload={"session_id": session_id,
            "turn_number":1,
            "active_side":"player"
            }
)

log_event(
    event_type="turn_end",
    stage_id=1,
    payload={
        "session_id":session_id,
        "turn_number":1,
        "active_side":"player"}
)

log_event(event_type="character_move",
         stage_id=1,
         payload={
             "session_id":session_id,
             "character_id":"player_1",
             "to_row":2,
             "to_col":3,
             "turn_number": 1}
)

log_event(
    event_type="session_end",
    stage_id=0,
    payload={
        "session_id":session_id,
        "stages_completed":1
    }
)
