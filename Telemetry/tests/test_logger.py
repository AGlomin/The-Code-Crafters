from unittest.mock import patch
from Telemetry.telemetry.logger import log_event
from Telemetry.telemetry.validator import TelemetryValidationError

def test_log_event_pipeline_success():
    with patch("Telemetry.telemetry.logger.validate_event") as mock_validate, \
         patch("Telemetry.telemetry.logger.detect_anomalies", side_effect=lambda x: x) as mock_detect, \
         patch("Telemetry.telemetry.logger.write_event") as mock_write:

        log_event("character_move",0,1,"session_abc","user_123",{"x": 10})

        mock_write.assert_called_once()  #pipelineworked

        # is the event object correct whch is going to writtenevent
        written_event= mock_write.call_args[0][0]
        assert written_event.event_type=="character_move"
        assert written_event.user_id=="user_123"

def test_log_event_stops_on_validation_error():
    with patch("Telemetry.telemetry.logger.validate_event", side_effect=TelemetryValidationError("Invalid")), \
         patch("Telemetry.telemetry.logger.write_event") as mock_write, \
         patch("Telemetry.telemetry.logger.detect_anomalies") as mock_detect:

        log_event("bad_event",0,1,"session1","user1", {})

        mock_write.assert_not_called()
        mock_detect.assert_not_called()