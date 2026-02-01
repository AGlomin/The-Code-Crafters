# Ran directly from source
try:
    from events import TelemetryEvent
    from validator import validate_event, detect_anomalies, TelemetryValidationError
    from storage import write_event
except:
    # Ran from mini_test
    try:
        from telemetry.events import TelemetryEvent
        from telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
        from telemetry.storage import write_event
    # Ran from game
    except:
        from Telemetry.telemetry.events import TelemetryEvent
        from Telemetry.telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
        from Telemetry.telemetry.storage import write_event

def log_event(event_type: str, stage_id: int, payload: dict):
    try:
        event = TelemetryEvent.create(
            event_type=event_type,
            stage_id=stage_id,
            payload=payload
        )

        validate_event(event)
        event = detect_anomalies(event)
        write_event(event)

    except TelemetryValidationError as e:
        print(f"[Telemetry Validation Error] {e}")

    except Exception as e:
        # Telemetry must NEVER crash the game
        print(f"[Telemetry Error] {e}")
