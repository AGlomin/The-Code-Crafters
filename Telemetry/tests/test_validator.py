""" import pytest
from telemetry.events import TelemetryEvent
from telemetry.validator import validate_event, TelemetryValidationError

def test_valid_event_passes():
    
    event = TelemetryEvent.create(
        event_type="character_attack",
        stage_id=1,
        payload={"attacker_id": "player_1", "target_id": "enemy_1", "damage": 5}
    )
    event.user_id = "test_user"
    event.data_quality_flags = []

    assert validate_event(event) == True
    """
#commit 