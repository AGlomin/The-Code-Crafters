from dataclasses import dataclass, field
from typing import Dict, Any, List
import time
import uuid


@dataclass
class TelemetryEvent:
    #event classification and context identifiers
    event_type: str
    level_id: int
    stage_id: int
    session_id: str
    user_id: str

    #automatically generates a unique event identifier
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    #timestamp automatically set at event creation
    timestamp: float = field(default_factory=time.time)
    
    #additional structured event-specific data
    payload: Dict[str, Any] = field(default_factory=dict)

    #flags used for data validation
    data_quality_flags: List[str] = field(default_factory=list)

    @staticmethod
    def create(
        event_type: str,
        level_id: int,
        stage_id: int,
        session_id: str,
        user_id: str,
        payload: Dict[str, Any],
    ):
        #type validation to ensure telemetry integrity
        if not isinstance(event_type, str):
            raise TypeError("event_type must be string")

        if not isinstance(stage_id, int):
            raise TypeError("stage_id must be int")
        
        if not isinstance(level_id, int):
            raise TypeError("level_id must be int")

        if not isinstance(session_id, str):
            raise TypeError("session_id must be string")

        if not isinstance(user_id, str):
            raise TypeError("user_id must be string")

        if not isinstance(payload, dict):
            raise TypeError("payload must be dict")

        #return validated TelemetryEvent instances
        return TelemetryEvent(
            event_type=event_type,
            level_id=level_id,
            stage_id=stage_id,
            session_id=session_id,
            user_id=user_id,
            payload=payload,
        )
 
