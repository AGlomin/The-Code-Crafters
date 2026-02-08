import pytest
from telemetry.events import TelemetryEvent
from telemetry.funnel import stage_funnel
from seed_data import seed_win_session, seed_fail_session

def test_win_sessions_funnel():
    events= seed_win_session()
    funnel=stage_funnel(events)

    assert funnel["started"]==1
    assert funnel["completed"]==1
    assert funnel["failed"]==0
    assert funnel["completion_rate"]==1.0

def test_fail_sessions_funnel():
    events= seed_fail_session()
    funnel=stage_funnel(events)

    assert funnel["started"]==1
    assert funnel["completed"]==0
    assert funnel["failed"]==1
    assert funnel["completion_rate"]==0.0
