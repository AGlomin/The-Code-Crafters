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

    #if event.event_type == "move" or event.event_type == "character_move":
    #    if "character_id" not in event.payload or "from_tile" not in event.payload or "to_tile" not in event.payload:
    #        errors.append("move event missing fields")
    #continued

    return errors
