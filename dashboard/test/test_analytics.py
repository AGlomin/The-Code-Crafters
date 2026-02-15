import pytest
from dashboard.analytics import compute_funnel, stage_failures
#funnel tests
def test_compute_win_and_fail():
    events=[
        {"event_type":"stage_start"},
        {"event_type":"stage_complete"},
        {"event_type":"stage_start"},
        {"event_type":"stage_fail"},
        {"event_type":"session_end"},
    ]
    funnel=compute_funnel(events)

    assert funnel["Stage Starts"]==2
    assert funnel["Stage Completes"]==1
    assert funnel["Stage Fails"]==1
    assert funnel["Sessions Ended"]==1
    assert funnel["Completion Rate %"]==50.0

def test_compute_all_win():
    events=[
        {"event_type":"stage_start"},
        {"event_type":"stage_complete"},
    ]
    funnel=compute_funnel(events)
    assert funnel["Stage Starts"]==1
    assert funnel["Stage Completes"]==1
    assert funnel["Completion Rate %"]==100.0
#if there is no start
def test_compute_no_start():
    events=[
        {"event_type":"stage_complete"},
        {"event_type":"stage_fail"},
    ]
    funnel=compute_funnel(events)

    assert funnel["Stage Starts"]==0
    assert funnel["Stage Fails"]==1
    assert funnel["Completion Rate %"]== 0
#--------------------------------------------
##Stage failures tests
def test_stage_failures_mult_stages():
    events=[
        {"event_type":"stage_fail","stage_id":1},
        {"event_type":"stage_fail","stage_id":1},
        {"event_type":"stage_fail","stage_id":2},
        {"event_type":"stage_start","stage_id":2},
        {"event_type":"stage_complete","stage_id":2}]
    failures=stage_failures(events)
    assert failures[1]==2
    assert failures[2]==1
    assert len(failures)==2
def test_stage_no_failures():
    events=[
        {"event_type":"stage_start","stage_id":1},
        {"event_type":"stage_complete","stage_id":1}]
    failures=stage_failures(events)
    assert failures == {}






