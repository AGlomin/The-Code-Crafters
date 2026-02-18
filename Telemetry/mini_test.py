from Telemetry.telemetry.logger import log_event
import uuid

session_id = str(uuid.uuid4())
user_id = "anon_user"

log_event(
    "session_start",
    0,
    0,
    session_id,
    user_id,
    {"config_id": "balanced", "difficulty_label": "balanced"},
)

log_event(
    "stage_start",
    0,
    1,
    session_id,
    user_id,
    {"enemy_count": 1, "grid_size": "4x5"},
)

log_event(
    "character_attack",
    0,
    1,
    session_id,
    user_id,
    {
        "attacker_id": "player_1",
        "target_id": "enemy_1",
        "damage": 3,
        "attack_range": 1,
    },
)

log_event(
    "stage_complete",
    0,
    1,
    session_id,
    user_id,
    {"turns_taken": 5},
)

log_event(
    "turn_start",
    0,
    1,
    session_id,
    user_id,
    {"turn_number": 1, "active_side": "player"},
)

log_event(
    "turn_end",
    0,
    1,
    session_id,
    user_id,
    {"turn_number": 1, "active_side": "player"},
)

log_event(
    "character_move",
    0,
    1,
    session_id,
    user_id,
    {
        "character_id": "player_1",
        "to_row": 2,
        "to_col": 3,
        "turn_number": 1,
    },
)

log_event(
    "session_end",
    0,
    0,
    session_id,
    user_id,
    {"stages_completed": 1},
)
