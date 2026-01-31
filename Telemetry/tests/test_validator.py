import pytest
from telemetry.events import TelemetryEvent
from telemetry.validator import validate_event,TelemetryValidationError,detect_anomalies

def test_valid_event():   
    event = TelemetryEvent.create(
        event_type="character_attack",
        stage_id=1,
        payload={"attacker_id": "player_1",
        "target_id": "enemy_1",
        "damage": 5
        }
    )
    assert validate_event(event) is True

def test_invalid_event_type():
    event= TelemetryEvent.create(
        event_type="invalid_event",
        stage_id=1,
        payload={}
    )
    with pytest.raises(TelemetryValidationError):
        validate_event(event)


def test_negative_stage_id():
    event=TelemetryEvent.create(
        event_type="character_attack",
        stage_id=-1,
        payload={}
    )
    with pytest.raises(TelemetryValidationError):
        validate_event(event)
