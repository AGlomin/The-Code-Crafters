import pytest
import uuid

from Telemetry.telemetry.anomaly import TelemetryAnomaly

def test_anomaly_defaults():
    anomaly=TelemetryAnomaly(
        event_id="1",
        anomaly_type="delay",
        detected_by="system"
    )
    assert anomaly.resolution_status=="unresolved"
    assert anomaly.anomaly_id is not None

    uuid.UUID(anomaly.anomaly_id)

    assert anomaly.event_id== "1"
    assert anomaly.anomaly_type=="delay"
    assert anomaly.detected_by== "system"

def test_anomaly_uuid_unique():
    anomaly1 = TelemetryAnomaly(
        event_id="1",
        anomaly_type="delay",
        detected_by="system"
    )
    anomaly2 = TelemetryAnomaly(
        event_id="2",
        anomaly_type="latency",
        detected_by="system"
    )
    assert anomaly1.anomaly_id != anomaly2.anomaly_id

def test_custom_resolution_status():
    anomaly = TelemetryAnomaly(
        event_id="1",
        anomaly_type="delay",
        detected_by="system",
        resolution_status="resolved"
    )
    assert anomaly.resolution_status=="resolved"