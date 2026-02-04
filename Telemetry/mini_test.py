from telemetry.logger import log_event
import uuid

log_event(
    event_type="session_start",
    stage_id=0,
    payload={"session_id":session_id,
             "difficulty": "balanced"}
)

log_event(
    event_type="stage_start",
    stage_id=1,
    session_id=str(uuid.uuid4()),
    payload={"session_id":session_id}
)

log_event(
    event_type="character_attack",
    stage_id=1,
    session_id=str(uuid.uuid4())
    payload={"session_id":session_id,
        "attacker_id": "player_1",
        "target_id": "enemy_1",
        "damage": 3
    }
)

log_event(
    event_type="stage_complete",
    stage_id=1,
    session_id=str(uuid.uuid4())
    payload={"session_id":session_id,
             "turns_taken": 5}
)

log_event(
    event_type="turn start",
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
             "to_col":3
         }
)

log_event(
    event_type="session_end",
    stage_id=0,
    payload={
        "session_id":session_id,
        "stages_completed":1
    }
)
