from dataclasses import dataclass, field
from typing import Dict, Any, List
import time
import uuid


SCHEMA_VERSION = "1.0"


@dataclass
class TelemetryEvent:
    event_type: str
    level_id: int
    stage_id: int
    session_id: str
    user_id: str
    config_id: str

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    payload: Dict[str, Any] = field(default_factory=dict)

    data_quality_flags: List[str] = field(default_factory=list)

    schema_version: str = SCHEMA_VERSION

    @staticmethod
    def create(
        event_type: str,
        level_id: int,
        stage_id: int,
        session_id: str,
        user_id: str,
        payload: Dict[str, Any],
        config_id: str = "baseline",
    ):

        if not isinstance(event_type, str):
            raise TypeError("event_type must be string")

        if not isinstance(level_id, int):
            raise TypeError("level_id must be int")

        if not isinstance(stage_id, int):
            raise TypeError("stage_id must be int")

        if not isinstance(session_id, str):
            raise TypeError("session_id must be string")

        if not isinstance(user_id, str):
            raise TypeError("user_id must be string")

        if not isinstance(config_id, str):
            raise TypeError("config_id must be string")

        if not isinstance(payload, dict):
            raise TypeError("payload must be dict")

        return TelemetryEvent(
            event_type=event_type,
            level_id=level_id,
            stage_id=stage_id,
            session_id=session_id,
            user_id=user_id,
            config_id=config_id,
            payload=payload,
        )