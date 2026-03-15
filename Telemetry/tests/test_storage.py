import csv
from Telemetry.telemetry.events import TelemetryEvent
import Telemetry.telemetry.storage as storage


def test_write_event_creates_and_writes_csv(tmp_path, monkeypatch):
    #using monkeypatch to avoid writing to the real csv
    #temporary csv path
    test_file = tmp_path/"telemetry.csv"
    
    test_file.touch() #create temp file

    # temporarily changing file path
    monkeypatch.setattr(storage, "FILE_PATH", str(test_file))

    event = TelemetryEvent.create(
        event_type="character_attack",
        level_id=0,
        stage_id=1,
        session_id="session1",
        user_id="anon_user",
        payload={
            "attacker_id": "player_1",
            "target_id": "enemy_1",
            "damage": 5,
            "attack_range": 1}
    )
    storage.write_event(event)
  
    assert test_file.exists()
  
    with open(test_file,newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]
    assert "event_type" in row
    assert "level_id" in row
    assert "stage_id" in row
    assert "session_id" in row
    assert "user_id" in row
    
    assert row["event_type"] == "character_attack"
    assert row["level_id"] == "0"
    assert row["stage_id"] == "1"  
    assert row["user_id"] == "anon_user"
    assert row["session_id"] == "session1"

    import json
    assert json.loads(row["payload"].replace("'", '"')) == event.payload
    assert json.loads(row["data_quality_flags"].replace("'", '"')) == event.data_quality_flags
