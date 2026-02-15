from analytics import compute_funnel
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
    assert "Completion Rate %" not in funnel
    

