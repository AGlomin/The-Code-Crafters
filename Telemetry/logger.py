from Telemetry.event import TelemetryEvent
from Telemetry.validator import validate_event, detect_anomalies, TelemetryValidationError
from Telemetry.storage import write_event

def log_event(event_type: str, stage_id: int, payload: dict):

    event = TelemetryEvent.create(
        event_type=event_type,
        stage_id=stage_id,
        payload=payload
    )

    try:
        validate_event(event)
    except TelemetryValidationError as e:
        print(f"[Telemetry Validation Error] {e}")
        return
      
    event = detect_anomalies(event)


    write_event(event)



