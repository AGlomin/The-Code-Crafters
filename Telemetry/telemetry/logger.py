try:
    from events import TelemetryEvent
    from validator import validate_event, detect_anomalies, TelemetryValidationError
    from storage import write_event
except:
    from telemetry.events import TelemetryEvent
    from telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
    from telemetry.storage import write_event


def log_event(event_type, stage_id, session_id, user_id, payload):

    try:
        event = TelemetryEvent.create(
            event_type=event_type,
            stage_id=stage_id,
            session_id=session_id,
            user_id=user_id,
            payload=payload,
        )

        validate_event(event)
        event = detect_anomalies(event)
        write_event(event)

    except TelemetryValidationError as e:
        print(f"[Telemetry Validation Error] {e}")

    except Exception as e:
        print(f"[Telemetry Error] {e}")
