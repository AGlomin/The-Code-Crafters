from telemetry.events import TelemetryEvent

def seed_win_session():
    return[TelemetryEvent.create("session_start" ,1,"s_win","user1",{}),
    TelemetryEvent.create("stage_start",1,"s_win","user1",{}),
    TelemetryEvent.create("stage_complete",1,"s_win","user1",{"turns_taken":4}),
    TelemetryEvent.create("session_end",1,"s_win","user1",{})]

def seed_fail_session():
    return[TelemetryEvent.create("session_start" ,1,"s_fail","user1",{}),
    TelemetryEvent.create("stage_start",1,"s_fail","user1",{}),
    TelemetryEvent.create("stage_fail",1,"s_fail","user1",{"turns_taken":4}),
    TelemetryEvent.create("session_end",1,"s_fail","user1",{})]