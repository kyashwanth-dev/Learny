# Basic Kafka producer example using kafka-python

from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {"event": "test", "value": 42}
producer.send('test_topic', value=data)
producer.flush()
print("Message sent!")
