from .event_types import EVENT_TYPES


class TelemetryValidationError(Exception):
    pass


PAYLOAD_SCHEMA = {
    "character_attack": ["damage"],
    "enemy_attack": ["damage"],
    "character_heal": ["heal_amount"],
    "stage_complete": ["turns_taken"],
}


SESSION_STATE = {}


def validate_event(event):

    if event.event_type not in EVENT_TYPES:
        raise TelemetryValidationError(f"Invalid event_type: {event.event_type}")

    if event.level_id < 0:
        raise TelemetryValidationError("Invalid level_id")

    if event.stage_id < 0:
        raise TelemetryValidationError("Invalid stage_id")

    if not event.session_id:
        raise TelemetryValidationError("Missing session_id")

    if not event.user_id:
        raise TelemetryValidationError("Missing user_id")

    if not isinstance(event.payload, dict):
        raise TelemetryValidationError("Payload must be dict")

    if event.event_type in PAYLOAD_SCHEMA:
        required = PAYLOAD_SCHEMA[event.event_type]
        for field in required:
            if field not in event.payload:
                raise TelemetryValidationError(
                    f"Missing payload field '{field}' for {event.event_type}"
                )

    if "damage" in event.payload and event.payload["damage"] < 0:
        raise TelemetryValidationError("Negative damage")

    if "heal_amount" in event.payload and event.payload["heal_amount"] < 0:
        raise TelemetryValidationError("Negative heal")

    if "turns_taken" in event.payload and event.payload["turns_taken"] < 0:
        raise TelemetryValidationError("Negative turns")

    return True


def detect_anomalies(event):

    if event.session_id not in SESSION_STATE:
        SESSION_STATE[event.session_id] = {"stage_started": False}

    state = SESSION_STATE[event.session_id]

    if event.event_type == "stage_start":
        state["stage_started"] = True

    if event.event_type == "stage_complete" and not state["stage_started"]:
        event.data_quality_flags.append("stage_complete_without_start")

    if event.event_type == "stage_complete":
        state["stage_started"] = False

    if event.event_type == "stage_retry":
        retries = event.payload.get("retry_count", 0)
        if retries > 10:
            event.data_quality_flags.append("excessive_retries")

    if event.event_type == "stage_complete":
        if event.payload.get("turns_taken", 1) == 0:
            event.data_quality_flags.append("instant_completion")

    return event