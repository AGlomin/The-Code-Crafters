from dataclasses import dataclass, field
from typing import Dict, Any, List
import time
import uuid


@dataclass
class TelemetryEvent:
    # REQUIRED (no defaults)
    event_type: str
    stage_id: int
    session_id: str
    user_id: str

    # OPTIONAL / DEFAULTED (must come AFTER required fields)
    timestamp: float = field(default_factory=time.time)
    payload: Dict[str, Any] = field(default_factory=dict)
    data_quality_flags: List[str] = field(default_factory=list)

    @staticmethod
    def create(event_type: str, stage_id: int, payload: Dict[str, Any]):
        return TelemetryEvent(
            event_type=event_type,
            stage_id=stage_id,
            session_id=str(uuid.uuid4()),
            user_id="anon_user",
            payload=payload
        )
