def stage_funnel(events):
    started=len([e for e in events if e.event_type=="stage_start"])
    completed= len([e for e in events if e.event_type=="stage_complete"])
    failed= len([e for e in events if e.event_type=="stage_fail"])
    
    return{
        "started": started,
        "completed":completed,
        "failed":failed,
        "completion_rate":completed/started if started >0 else 0
    }