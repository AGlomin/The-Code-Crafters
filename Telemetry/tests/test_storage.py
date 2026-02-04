import csv
from telemetry.events import TelemetryEvent
import telemetry.storage as storage


def test_write_event_creates_and_writes_csv(tmp_path, monkeypatch):
    #using monkeypatch to avoid writing to the real csv
    #temporary csv path
    test_file = tmp_path / "telemetry.csv"

    # temporarily changing file path
    monkeypatch.setattr(storage, "FILE_PATH", str(test_file))

    event = TelemetryEvent.create(
        event_type="character_attack",
        stage_id=1,
        payload={"damage": 5}
    )
    storage.write_event(event)
  
    assert test_file.exists()
  
    with open(test_file,newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]

    
    assert row["event_type"] == "character_attack"
    assert row["stage_id"] == "1"  
    assert row["user_id"] == "anon_user"
