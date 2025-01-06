import pytest
from unittest.mock import MagicMock
from DataProcessor.publisher import Publisher

def test_publisher_initialization():
    publisher = Publisher(kafka_server="localhost:9092", topic="test_topic")
    assert publisher.kafka_server == "localhost:9092"
    assert publisher.topic == "test_topic"
    assert publisher.producer is not None

from unittest.mock import Mock, patch
@patch('confluent_kafka.Producer')
def test_send_event_to_kafka_success(mock_producer):
    mock_instance = mock_producer.return_value
    mock_instance.produce = MagicMock()
    publisher = Publisher(kafka_server='localhost:9092', topic='test_topic')
    publisher.send_event_to_kafka({'key': 'value'})
    mock_instance.produce.assert_called_once()

@patch('confluent_kafka.Producer')
def test_send_event_to_kafka_failure(mock_producer):
    mock_instance = mock_producer.return_value
    mock_instance.produce = MagicMock(side_effect=Exception('Kafka error'))
    publisher = Publisher(kafka_server='localhost:9092', topic='test_topic')
    with pytest.raises(Exception, match="Kafka error"):
        publisher.send_event_to_kafka({'key': 'value'})
