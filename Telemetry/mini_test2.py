import uuid
import time

from telemetry.logger import log_event
#from Telemetry.telemetry.logger import log_event


def run_test():

    print("Starting telemetry test...")

    session_id = str(uuid.uuid4())
    user_id = "test_player"
    config_id = "balanced"

    level_id = 1
    stage_id = 0

    # session start
    log_event(
        event_type="session_start",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={}
    )

    # level start
    log_event(
        event_type="level_start",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={}
    )

    # stage start
    log_event(
        event_type="stage_start",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={}
    )

    # player attack
    log_event(
        event_type="character_attack",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={
            "damage": 5
        }
    )

    # enemy attack
    log_event(
        event_type="enemy_attack",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={
            "damage": 3
        }
    )

    # player takes damage
    log_event(
        event_type="player_damage",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={
            "damage": 3
        }
    )

    # stage complete
    log_event(
        event_type="stage_complete",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={
            "turns_taken": 5
        }
    )

    # anomaly test (instant completion)
    log_event(
        event_type="stage_complete",
        level_id=level_id,
        stage_id=1,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={
            "turns_taken": 0
        }
    )

    # session end
    log_event(
        event_type="session_end",
        level_id=level_id,
        stage_id=stage_id,
        session_id=session_id,
        user_id=user_id,
        config_id=config_id,
        payload={}
    )

    print("Telemetry test finished.")
    print("Check telemetry/telemetry.csv for logged events.")


if __name__ == "__main__":
    run_test()