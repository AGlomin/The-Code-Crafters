import pytest
from Telemetry.telemetry.events import TelemetryEvent
from Telemetry.telemetry.validator import validate_event, TelemetryValidationError,detect_anomalies

def test_valid_event():   
    event = TelemetryEvent.create(
        event_type="character_attack",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={
        "attacker_id": "player_1",
        "target_id": "enemy_1",
        "damage": 5,
        "attack_range": 1
        }
    )
    assert validate_event(event) is True

def test_invalid_event_type():
    event= TelemetryEvent.create(
        event_type="invalid_event",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={}
    )
    with pytest.raises(TelemetryValidationError):
        validate_event(event)


def test_negative_stage_id():
    event=TelemetryEvent.create(
        event_type="character_attack",
        level_id=0,
        stage_id=-1,
        session_id="session1",
        user_id="user1",
        payload={
            "attacker_id": "player_1",
            "target_id": "enemy_1",
            "damage": 5,
            "attack_range": 1}
    )
    with pytest.raises(TelemetryValidationError):
        validate_event(event)

def test_negative_damage():
    event=TelemetryEvent.create(
        event_type="character_attack",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={
            "attacker_id": "player_1",
            "target_id": "enemy_1",
            "damage": -3,
            "attack_range": 1}
    )
    with pytest.raises(TelemetryValidationError):
        validate_event(event)

def test_instant_completion_flag():
    event=TelemetryEvent.create(
        event_type="stage_complete",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={"turns_taken": 0}
    )
    result = detect_anomalies(event)
    assert "instant_completion" in result.data_quality_flags

def test_excessive_retries_flag():
    event=TelemetryEvent.create(
        event_type="stage_retry",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={"retry_count": 11}
    )
    result = detect_anomalies(event)
    assert "excessive_retries" in result.data_quality_flags
def test_no_anomalies():
    event=TelemetryEvent.create(
        event_type="character_attack",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="user1",
        payload={
            "attacker_id": "player_1",
            "target_id": "enemy_1",
            "damage": 5,
            "attack_range": 1}
    )
    result= detect_anomalies(event)
    assert result.data_quality_flags == []

    
