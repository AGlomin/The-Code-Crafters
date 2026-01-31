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
        if not isinstance(event_type, str):
            raise TypeError("event_type must be a string")
        if not isinstance(stage_id, int):
            raise TypeError("stage_id must be an integer")
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
    
        return TelemetryEvent(
            event_type=event_type,
            stage_id=stage_id,
            session_id=str(uuid.uuid4()),
            user_id="anon_user",
            payload=payload
        )
#commit 