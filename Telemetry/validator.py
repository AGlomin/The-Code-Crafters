def validate_event(event):
    errors = []
  
    if not event.event_type:
        errors.append("missing event_type")
    if event.stage_id is None:
        errors.append("missing stage_id")
    if not event.user_id:
        errors.append("missing user_id")
    if not event.session_id:
        errors.append("missing session_id")
    if not event.timestamp:
        errors.append("missing timestamp")
    if event.payload is None:
        errors.append("missing payload")

   
    #continued
    #character move etc will be added in forward times (sprint2)

    return errors


