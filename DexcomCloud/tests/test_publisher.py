import pytest
from unittest.mock import MagicMock
from DataProcessor.publisher import Publisher

def test_publisher_initialization():
    publisher = Publisher(kafka_server="kafka:9092", topic="test_topic")
    assert publisher.kafka_server == "localhost:9092"
    assert publisher.topic == "test_topic"
    assert publisher.producer is not None

def test_send_event_to_kafka_success(mocker):
    publisher = Publisher(kafka_server="kafka:9092", topic="test_topic")
    mocker.patch.object(publisher.producer, 'produce', return_value=None)
    mocker.patch.object(publisher.producer, 'flush', return_value=None)

    publisher.send_event_to_kafka({"key": "value"})
    publisher.producer.produce.assert_called_once_with("test_topic", value='{"key": "value"}')
    publisher.producer.flush.assert_called_once()

def test_send_event_to_kafka_failure(mocker):
    publisher = Publisher(kafka_server="kafka:9092", topic="test_topic")
    mocker.patch.object(publisher.producer, 'produce', side_effect=Exception("Kafka Error"))

    with pytest.raises(Exception, match="Kafka Error"):
        publisher.send_event_to_kafka({"key": "value"})
