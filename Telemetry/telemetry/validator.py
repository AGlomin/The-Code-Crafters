try:
    from event_types import EVENT_TYPES
except:
    from telemetry.event_types import EVENT_TYPES


class TelemetryValidationError(Exception):
    pass


def validate_event(event):

    if event.event_type not in EVENT_TYPES:
        raise TelemetryValidationError(f"Invalid event_type: {event.event_type}")

    if event.stage_id is None or event.stage_id < 0:
        raise TelemetryValidationError("Invalid stage_id")

    if not event.session_id:
        raise TelemetryValidationError("Missing session_id")

    if not event.user_id:
        raise TelemetryValidationError("Missing user_id")

    if not isinstance(event.payload, dict):
        raise TelemetryValidationError("Payload must be dict")

    # numeric sanity checks
    if "damage" in event.payload and event.payload["damage"] < 0:
        raise TelemetryValidationError("Negative damage")

    if "heal_amount" in event.payload and event.payload["heal_amount"] < 0:
        raise TelemetryValidationError("Negative heal")

    if "turns_taken" in event.payload and event.payload["turns_taken"] < 0:
        raise TelemetryValidationError("Negative turns")

    return True


def detect_anomalies(event):

    if event.event_type == "stage_complete":
        if event.payload.get("turns_taken", 1) == 0:
            event.data_quality_flags.append("instant_completion")

    if event.event_type == "stage_retry":
        if event.payload.get("retry_count", 0) > 10:
            event.data_quality_flags.append("excessive_retries")

    if event.event_type == "stage_complete" and event.stage_id == 0:
        event.data_quality_flags.append("invalid_stage_complete")

    return event
