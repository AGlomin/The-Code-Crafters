import pytest
import time
import uuid
from Telemetry.telemetry.events import TelemetryEvent

def test_event_init_fields():
    event= TelemetryEvent.create("character_attack",1,"s1","anon_user",{"damage":5})
    assert event.event_type=="character_attack"
    assert event.stage_id==1
    assert event.user_id=="anon_user"
    assert event.payload=={"damage":5}

def test_event_id_unique():
    event1 = TelemetryEvent.create("event", 1, "s1", "u1", {})
    event2 = TelemetryEvent.create("event", 1, "s1", "u1", {})
    assert event1.event_id != event2.event_id

def test_timestamp_autoset():
    before=time.time()
    event=TelemetryEvent.create("event",1,"s1", "u1",{})
    after=time.time()
    assert before<=event.timestamp<=after

def test_default_payload():
    #testing whether defaults are empty
    event=TelemetryEvent.create("event",1,"s1", "u1",{})
    assert event.payload=={}

def test_default_data_quality_flags():
    #testing whether defaults are empty
    event=TelemetryEvent.create("event",1, "s1", "u1",{})
    assert event.data_quality_flags==[]

#testing that mutable defaults are independent between instances
def test_mutable_defaults_independent():
    event1=TelemetryEvent.create("event1",1,"s1", "u1",{})
    event2=TelemetryEvent.create("event2",2,"s2","u2",{})
    event1.payload["new_key"]="value"
    event1.data_quality_flags.append("flag1")
    assert "new_key" not in event2.payload
    assert "flag1" not in event2.data_quality_flags

def test_event_type_wrong_type():
    with pytest.raises(TypeError):
        TelemetryEvent.create(123, 1,"s1", "u1", {})

def test_stage_id_wrong_type():
    with pytest.raises(TypeError):
        TelemetryEvent.create("event", "wrong_stage","s1", "u1",{})

def test_payload_wrong_type():
    with pytest.raises(TypeError):
        TelemetryEvent.create("event", 1,"s1","u1","not_a_dict")
