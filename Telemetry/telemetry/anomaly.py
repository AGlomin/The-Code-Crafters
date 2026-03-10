from dataclasses import dataclass, field
import uuid


@dataclass
class TelemetryAnomaly:
    event_id: str
    anomaly_type: str
    detected_by: str

    anomaly_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resolution_status: str = "unresolved"