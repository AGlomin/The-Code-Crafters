try:
    from events import TelemetryEvent
except:
    try:
        from telemetry.events import TelemetryEvent
    except:
        from Telemetry.telemetry.events import TelemetryEvent
try:
    from validator import validate_event, detect_anomalies, TelemetryValidationError
except:
    try:
        from telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
    except:
        from Telemetry.telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
try:
    from storage import write_event
except:
    try:
        from telemetry.storage import write_event
    except:
        from Telemetry.telemetry.storage import write_event


def log_event(event_type, level_id, stage_id, session_id, user_id, payload):

    try:
        #create structured TelemetryEvent object
        event = TelemetryEvent.create(
            event_type=event_type,
            level_id=level_id,
            stage_id=stage_id,
            session_id=session_id,
            user_id=user_id,
            payload=payload,
        )
        #validate event schema and required fields
        validate_event(event)
        #anomaly detection
        event = detect_anomalies(event)
        #add event to telemetry storage (CSV file)
        write_event(event)
    #handle domain-specific validation errors separately
    except TelemetryValidationError as e:
        print(f"[Telemetry Validation Error] {e}")
    #catch any unexpected system errors
    except Exception as e:
        print(f"[Telemetry Error] {e}")

