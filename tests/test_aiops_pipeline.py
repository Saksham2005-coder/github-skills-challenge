import io
import runpy
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.anomaly_detector import AnomalyDetector
from src.aiops_pipeline import run_pipeline
from src.event_consumer import EventConsumer
from src.event_producer import EventProducer
from src.event_topic import EventTopic


def test_normal_record_is_not_anomaly():
    detector = AnomalyDetector()

    record = {
        "timestamp": "2026-09-20T10:00:00",
        "service": "payment-service",
        "response_time_ms": 120,
        "cpu_percent": 42,
        "memory_percent": 51,
        "log_level": "INFO",
        "message": "Payment request processed successfully"
    }

    assert detector.detect(record) is None


def test_anomalous_record_is_detected():
    detector = AnomalyDetector()

    record = {
        "timestamp": "2026-09-20T10:05:00",
        "service": "payment-service",
        "response_time_ms": 610,
        "cpu_percent": 75,
        "memory_percent": 70,
        "log_level": "ERROR",
        "message": "Payment service timeout"
    }

    event = detector.detect(record)

    assert event is not None
    assert event["type"] == "ANOMALY"


def test_producer_publishes_event():
    topic = EventTopic("anomaly-events")
    producer = EventProducer(topic)

    event = {
        "type": "ANOMALY",
        "service": "payment-service"
    }

    assert producer.publish(event)
    assert len(topic.get_messages()) == 1


def test_consumer_receives_event():
    topic = EventTopic("anomaly-events")
    producer = EventProducer(topic)
    consumer = EventConsumer(topic)

    event = {
        "type": "ANOMALY",
        "service": "payment-service"
    }

    producer.publish(event)

    messages = consumer.consume()

    assert len(messages) == 1


def test_warning_log_is_flagged_as_anomaly():
    detector = AnomalyDetector()

    record = {
        "timestamp": "2026-09-20T10:10:00",
        "service": "payment-service",
        "response_time_ms": 180,
        "cpu_percent": 55,
        "memory_percent": 58,
        "log_level": "WARNING",
        "message": "Potential slowdown detected"
    }

    event = detector.detect(record)

    assert event is not None
    assert "Error log detected" in event["reasons"]


def test_run_pipeline_consumes_generated_anomaly_events():
    result = run_pipeline("data/service_data.json")

    assert result["records_processed"] == 10
    assert len(result["anomalies_detected"]) == 2
    assert len(result["events_consumed"]) == 2
    assert result["events_consumed"][0]["type"] == "ANOMALY"


def test_producer_rejects_empty_event():
    topic = EventTopic("empty-events")
    producer = EventProducer(topic)

    assert producer.publish({}) is False
    assert topic.get_messages() == []


def test_event_topic_clear_removes_messages():
    topic = EventTopic("events")
    topic.publish({"type": "ANOMALY", "service": "payment-service"})

    topic.clear()

    assert topic.get_messages() == []


def test_pipeline_main_executes_and_prints_summary():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        runpy.run_module("src.aiops_pipeline", run_name="__main__")

    output = buffer.getvalue()
    assert "AIOps Pipeline Result" in output
    assert "Records processed:" in output
    assert "Anomalies detected:" in output
    assert "Events consumed:" in output