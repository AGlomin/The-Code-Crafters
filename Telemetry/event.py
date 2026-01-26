from dataclasses import dataclass, field
from typing import Dict, Any
import time
import uuid

@dataclass
class TelemetryEvent:
    event_type: str
    stage_id: int
    session_id: str
    user_id: str
    timestamp: float
    payload: Dict[str, Any] = field(default_factory = dict)
    @staticmethod
    def create(event_type: str, stage_ig: int, payload: Dict[str, Any]):
        return TelemetryEvent(
            event_type=event_type,
            stage_id=stage_id,
            session_id=str(uuid.uuid4()),
            user_id="anon_user",
            payload=payload
        )
