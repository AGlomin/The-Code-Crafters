from .events import TelemetryEvent
from .validator import validate_event, detect_anomalies, TelemetryValidationError
from .storage import write_event


def log_event(
    event_type,
    level_id,
    stage_id,
    session_id,
    user_id,
    payload,
    config_id="baseline",
):

    try:

        event = TelemetryEvent.create(
            event_type=event_type,
            level_id=level_id,
            stage_id=stage_id,
            session_id=session_id,
            user_id=user_id,
            config_id=config_id,
            payload=payload,
        )

        validate_event(event)

        event = detect_anomalies(event)

        write_event(event)

    except TelemetryValidationError as e:
        print(f"[Telemetry Validation Error] {e}")

    except Exception as e:
        print(f"[Telemetry Error] {e}")