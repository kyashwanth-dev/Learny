# Apache Kafka Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Apache Kafka?](#what-is-apache-kafka)
- [Key Concepts](#key-concepts)
- [Architecture](#architecture)
- [Installing Kafka](#installing-kafka)
- [Kafka CLI Tools](#kafka-cli-tools)
- [Producers](#producers)
- [Consumers](#consumers)
- [Topics and Partitions](#topics-and-partitions)
- [Consumer Groups](#consumer-groups)
- [Kafka Connect](#kafka-connect)
- [Kafka Streams](#kafka-streams)
- [Schema Registry](#schema-registry)
- [Security](#security)
- [Monitoring and Operations](#monitoring-and-operations)
- [Performance Tuning](#performance-tuning)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## Introduction

Apache Kafka is a distributed event streaming platform capable of handling trillions of events a day. Originally developed by LinkedIn and open-sourced in 2011, it has become the de facto standard for building real-time data pipelines and streaming applications.

## What is Apache Kafka?

Apache Kafka provides:

- **High Throughput**: Handle millions of messages per second
- **Scalability**: Horizontally scalable across multiple nodes
- **Durability**: Persistent storage with replication
- **Fault Tolerance**: Built-in resilience to node failures
- **Real-Time Processing**: Low-latency message delivery
- **Stream Processing**: Built-in stream processing capabilities

### Benefits
- ✅ Decouples data producers and consumers
- ✅ Provides message persistence and replay capability
- ✅ Scales horizontally to handle high loads
- ✅ Supports multiple programming languages
- ✅ Battle-tested at massive scale
- ✅ Active open-source community

### Use Cases
- **Messaging**: Replace traditional message brokers
- **Log Aggregation**: Collect logs from multiple services
- **Stream Processing**: Real-time analytics and ETL
- **Event Sourcing**: Store application state changes
- **Commit Log**: Database replication and change data capture
- **Metrics Collection**: Monitor application and system metrics

## Key Concepts

### Broker
A Kafka server that stores and serves data. A Kafka cluster consists of multiple brokers.

### Topic
A category or feed name to which records are published. Topics are multi-subscriber.

### Partition
Topics are divided into partitions for parallelism. Each partition is an ordered, immutable sequence of records.

### Producer
Applications that publish (write) data to Kafka topics.

### Consumer
Applications that subscribe to (read) data from Kafka topics.

### Consumer Group
A group of consumers that work together to consume a topic. Each partition is consumed by exactly one consumer in the group.

### Offset
A unique identifier for each record within a partition. Consumers track their position using offsets.

### Replica
A copy of a partition for fault tolerance. One replica is the leader, others are followers.

### ZooKeeper / KRaft
Coordination service used by Kafka (ZooKeeper is being replaced by KRaft in newer versions).

## Architecture

### Core Components

#### Kafka Cluster
```
┌─────────────────────────────────────────────────┐
│              Kafka Cluster                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Broker 1│  │ Broker 2│  │ Broker 3│        │
│  │         │  │         │  │         │        │
│  │ Topic A │  │ Topic A │  │ Topic B │        │
│  │ Part. 0 │  │ Part. 1 │  │ Part. 0 │        │
│  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────┘
         ▲                        │
         │                        ▼
    Producers                 Consumers
```

#### Data Flow
1. **Producer** sends messages to topics
2. **Broker** stores messages in partitions
3. **Consumer** reads messages from partitions
4. **Consumer Group** coordinates message consumption

### Topic Partitions

#### Partition Structure
```
Topic: orders
├── Partition 0: [msg0, msg3, msg6, msg9]  → Consumer A
├── Partition 1: [msg1, msg4, msg7, msg10] → Consumer B
└── Partition 2: [msg2, msg5, msg8, msg11] → Consumer C
```

#### Replication
```
Partition 0:
├── Leader (Broker 1)    ← Reads/Writes
├── Follower (Broker 2)  ← Replicates
└── Follower (Broker 3)  ← Replicates
```

## Installing Kafka

### Prerequisites
- Java 8 or higher
- Minimum 2 GB RAM
- 10 GB disk space

### Download and Install

#### Linux/macOS
```bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz

# Extract
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0

# Set environment variable
export KAFKA_HOME=$(pwd)
export PATH=$PATH:$KAFKA_HOME/bin
```

#### Windows
```powershell
# Download from https://kafka.apache.org/downloads
# Extract to C:\kafka

# Add to PATH
setx KAFKA_HOME "C:\kafka"
setx PATH "%PATH%;%KAFKA_HOME%\bin\windows"
```

### Start Kafka with ZooKeeper

#### Start ZooKeeper
```bash
# Start ZooKeeper server
bin/zookeeper-server-start.sh config/zookeeper.properties

# Windows
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

#### Start Kafka Broker
```bash
# Start Kafka server
bin/kafka-server-start.sh config/server.properties

# Windows
bin\windows\kafka-server-start.bat config\server.properties
```

### Start Kafka with KRaft (No ZooKeeper)

```bash
# Generate cluster ID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Format storage directory
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# Start Kafka server
bin/kafka-server-start.sh config/kraft/server.properties
```

### Docker Installation

#### Docker Compose
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
```

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f kafka

# Stop services
docker-compose down
```

## Kafka CLI Tools

### Topic Management

#### Create Topic
```bash
# Create topic with default settings
kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092

# Create with partitions and replication
kafka-topics.sh --create \
  --topic orders \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server localhost:9092

# Create with configuration
kafka-topics.sh --create \
  --topic logs \
  --partitions 5 \
  --replication-factor 1 \
  --config retention.ms=86400000 \
  --config segment.bytes=1073741824 \
  --bootstrap-server localhost:9092
```

#### List Topics
```bash
# List all topics
kafka-topics.sh --list \
  --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe \
  --topic my-topic \
  --bootstrap-server localhost:9092

# Describe all topics
kafka-topics.sh --describe \
  --bootstrap-server localhost:9092
```

#### Modify Topic
```bash
# Increase partitions (cannot decrease)
kafka-topics.sh --alter \
  --topic my-topic \
  --partitions 5 \
  --bootstrap-server localhost:9092

# Change configuration
kafka-configs.sh --alter \
  --entity-type topics \
  --entity-name my-topic \
  --add-config retention.ms=172800000 \
  --bootstrap-server localhost:9092
```

#### Delete Topic
```bash
# Delete topic
kafka-topics.sh --delete \
  --topic my-topic \
  --bootstrap-server localhost:9092
```

### Console Producer
```bash
# Simple producer
kafka-console-producer.sh \
  --topic my-topic \
  --bootstrap-server localhost:9092

# Producer with key
kafka-console-producer.sh \
  --topic orders \
  --property "parse.key=true" \
  --property "key.separator=:" \
  --bootstrap-server localhost:9092

# Example messages:
# key1:value1
# key2:value2

# Producer with properties
kafka-console-producer.sh \
  --topic my-topic \
  --producer-property acks=all \
  --producer-property compression.type=gzip \
  --bootstrap-server localhost:9092
```

### Console Consumer
```bash
# Simple consumer (from latest)
kafka-console-consumer.sh \
  --topic my-topic \
  --bootstrap-server localhost:9092

# Consumer from beginning
kafka-console-consumer.sh \
  --topic my-topic \
  --from-beginning \
  --bootstrap-server localhost:9092

# Consumer with key
kafka-console-consumer.sh \
  --topic orders \
  --property print.key=true \
  --property key.separator=":" \
  --from-beginning \
  --bootstrap-server localhost:9092

# Consumer group
kafka-console-consumer.sh \
  --topic my-topic \
  --group my-consumer-group \
  --bootstrap-server localhost:9092
```

### Consumer Group Management
```bash
# List consumer groups
kafka-consumer-groups.sh --list \
  --bootstrap-server localhost:9092

# Describe consumer group
kafka-consumer-groups.sh --describe \
  --group my-consumer-group \
  --bootstrap-server localhost:9092

# Reset offsets to earliest
kafka-consumer-groups.sh --reset-offsets \
  --group my-consumer-group \
  --topic my-topic \
  --to-earliest \
  --execute \
  --bootstrap-server localhost:9092

# Reset offsets to specific offset
kafka-consumer-groups.sh --reset-offsets \
  --group my-consumer-group \
  --topic my-topic:0 \
  --to-offset 100 \
  --execute \
  --bootstrap-server localhost:9092

# Delete consumer group
kafka-consumer-groups.sh --delete \
  --group my-consumer-group \
  --bootstrap-server localhost:9092
```

## Producers

### Producer Concepts

#### Acknowledgements (acks)
- `acks=0`: No acknowledgment (fastest, least safe)
- `acks=1`: Leader acknowledgment (balanced)
- `acks=all`: All in-sync replicas (slowest, safest)

#### Partitioning Strategies
- **Round-robin**: Default when no key is provided
- **Key-based**: Hash of key determines partition
- **Custom**: Implement custom partitioner

### Java Producer Example

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;

public class SimpleProducer {
    public static void main(String[] args) {
        // Configure producer
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.RETRIES_CONFIG, 3);
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "snappy");
        
        // Create producer
        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        
        try {
            // Send synchronously
            ProducerRecord<String, String> record = 
                new ProducerRecord<>("my-topic", "key1", "value1");
            RecordMetadata metadata = producer.send(record).get();
            System.out.printf("Sent to partition %d with offset %d%n", 
                metadata.partition(), metadata.offset());
            
            // Send asynchronously with callback
            producer.send(new ProducerRecord<>("my-topic", "key2", "value2"),
                (metadata, exception) -> {
                    if (exception != null) {
                        exception.printStackTrace();
                    } else {
                        System.out.printf("Sent to partition %d with offset %d%n",
                            metadata.partition(), metadata.offset());
                    }
                });
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            producer.close();
        }
    }
}
```

### Python Producer Example

```python
from kafka import KafkaProducer
import json

# Create producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3,
    compression_type='gzip'
)

# Send message
future = producer.send('my-topic', {'key': 'value'})

# Wait for message to be delivered
try:
    record_metadata = future.get(timeout=10)
    print(f"Sent to partition {record_metadata.partition} "
          f"with offset {record_metadata.offset}")
except Exception as e:
    print(f"Failed to send message: {e}")

# Flush and close
producer.flush()
producer.close()
```

### Node.js Producer Example

```javascript
const { Kafka } = require('kafkajs');

// Create Kafka client
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

// Create producer
const producer = kafka.producer();

async function sendMessage() {
  await producer.connect();
  
  try {
    // Send message
    const result = await producer.send({
      topic: 'my-topic',
      messages: [
        { 
          key: 'key1', 
          value: 'value1',
          partition: 0  // Optional: specific partition
        }
      ],
      acks: -1,  // Wait for all in-sync replicas
      compression: 'gzip'
    });
    
    console.log('Message sent:', result);
  } catch (error) {
    console.error('Error sending message:', error);
  } finally {
    await producer.disconnect();
  }
}

sendMessage();
```

### Producer Configuration Best Practices

```java
// Production-ready configuration
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

// Reliability
props.put("acks", "all");                    // Wait for all replicas
props.put("retries", 3);                     // Retry failed sends
props.put("enable.idempotence", "true");     // Prevent duplicates

// Performance
props.put("compression.type", "snappy");     // Compress messages
props.put("batch.size", 32768);              // Batch size in bytes
props.put("linger.ms", 10);                  // Wait for batching

// Timeout
props.put("request.timeout.ms", 30000);      // Request timeout
props.put("delivery.timeout.ms", 120000);    // Overall delivery timeout
```

## Consumers

### Consumer Concepts

#### Consumer Group Rebalancing
When consumers join or leave a group, partitions are redistributed.

#### Offset Management
- **Auto-commit**: Offsets committed automatically
- **Manual-commit**: Application controls when to commit
- **At-least-once**: Message may be processed multiple times
- **At-most-once**: Message may be lost
- **Exactly-once**: Message processed exactly once (with transactions)

### Java Consumer Example

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.time.Duration;
import java.util.*;

public class SimpleConsumer {
    public static void main(String[] args) {
        // Configure consumer
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "my-consumer-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        
        // Create consumer
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        
        // Subscribe to topics
        consumer.subscribe(Arrays.asList("my-topic"));
        
        try {
            while (true) {
                // Poll for records
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s%n",
                        record.topic(), record.partition(), record.offset(), 
                        record.key(), record.value());
                }
                
                // Manual commit
                consumer.commitSync();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            consumer.close();
        }
    }
}
```

### Python Consumer Example

```python
from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['localhost:9092'],
    group_id='my-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

try:
    for message in consumer:
        print(f"Topic: {message.topic}, "
              f"Partition: {message.partition}, "
              f"Offset: {message.offset}, "
              f"Key: {message.key}, "
              f"Value: {message.value}")
        
        # Manual commit
        consumer.commit()
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

### Node.js Consumer Example

```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'my-consumer-group' });

async function consumeMessages() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'my-topic', fromBeginning: true });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        topic,
        partition,
        offset: message.offset,
        key: message.key?.toString(),
        value: message.value.toString()
      });
    }
  });
}

consumeMessages().catch(console.error);
```

### Consumer Configuration Best Practices

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-consumer-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

// Offset management
props.put("enable.auto.commit", "false");         // Manual commit
props.put("auto.offset.reset", "earliest");       // Start from beginning if no offset

// Performance
props.put("fetch.min.bytes", 1024);               // Min bytes to fetch
props.put("fetch.max.wait.ms", 500);              // Max wait time
props.put("max.poll.records", 500);               // Records per poll

// Session management
props.put("session.timeout.ms", 10000);           // Consumer session timeout
props.put("heartbeat.interval.ms", 3000);         // Heartbeat interval
```

## Topics and Partitions

### Topic Configuration

#### Important Topic Settings
```bash
# Retention time (7 days in milliseconds)
retention.ms=604800000

# Retention size (1 GB)
retention.bytes=1073741824

# Segment size (1 GB)
segment.bytes=1073741824

# Compression type
compression.type=producer

# Min in-sync replicas
min.insync.replicas=2

# Cleanup policy (delete or compact)
cleanup.policy=delete
```

### Partitioning Strategy

#### Key-Based Partitioning
```java
// Messages with same key go to same partition
ProducerRecord<String, String> record = 
    new ProducerRecord<>("orders", "customer-123", orderData);
```

#### Custom Partitioner
```java
public class CustomPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                        Object value, byte[] valueBytes, Cluster cluster) {
        // Custom partitioning logic
        int numPartitions = cluster.partitionCountForTopic(topic);
        return Math.abs(key.hashCode()) % numPartitions;
    }
}
```

### Log Compaction

```bash
# Enable log compaction
kafka-configs.sh --alter \
  --entity-type topics \
  --entity-name user-state \
  --add-config cleanup.policy=compact \
  --bootstrap-server localhost:9092

# Configure compaction
kafka-configs.sh --alter \
  --entity-type topics \
  --entity-name user-state \
  --add-config min.cleanable.dirty.ratio=0.5 \
  --add-config segment.ms=86400000 \
  --bootstrap-server localhost:9092
```

## Consumer Groups

### Consumer Group Coordination

#### Partition Assignment Strategies
- **Range**: Assigns consecutive partitions to consumers
- **Round-Robin**: Distributes partitions evenly
- **Sticky**: Minimizes partition movement during rebalance
- **Cooperative Sticky**: Incremental rebalancing

### Consumer Group Example

```java
// Consumer 1
Properties props = new Properties();
props.put("group.id", "order-processors");
props.put("partition.assignment.strategy", 
    "org.apache.kafka.clients.consumer.RangeAssignor");
KafkaConsumer<String, String> consumer1 = new KafkaConsumer<>(props);

// Consumer 2 (same group)
KafkaConsumer<String, String> consumer2 = new KafkaConsumer<>(props);

// Partitions automatically distributed between consumer1 and consumer2
```

### Monitoring Consumer Lag

```bash
# Check consumer lag
kafka-consumer-groups.sh --describe \
  --group my-consumer-group \
  --bootstrap-server localhost:9092

# Output shows:
# GROUP, TOPIC, PARTITION, CURRENT-OFFSET, LOG-END-OFFSET, LAG
```

## Kafka Connect

### What is Kafka Connect?
A framework for connecting Kafka with external systems (databases, file systems, cloud services).

### Kafka Connect Modes

#### Standalone Mode
```bash
# Run standalone connector
connect-standalone.sh \
  config/connect-standalone.properties \
  config/connect-file-source.properties
```

#### Distributed Mode
```bash
# Run distributed connector
connect-distributed.sh config/connect-distributed.properties
```

### Source Connector Example

#### File Source Connector
```json
{
  "name": "file-source",
  "config": {
    "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "tasks.max": "1",
    "file": "/tmp/input.txt",
    "topic": "file-topic"
  }
}
```

#### JDBC Source Connector
```json
{
  "name": "jdbc-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "connection.user": "user",
    "connection.password": "password",
    "table.whitelist": "users,orders",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "db-"
  }
}
```

### Sink Connector Example

#### JDBC Sink Connector
```json
{
  "name": "jdbc-sink",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://localhost:5432/warehouse",
    "connection.user": "user",
    "connection.password": "password",
    "topics": "orders",
    "auto.create": "true",
    "auto.evolve": "true"
  }
}
```

### Managing Connectors

```bash
# List connectors (REST API)
curl http://localhost:8083/connectors

# Create connector
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @connector-config.json

# Check connector status
curl http://localhost:8083/connectors/my-connector/status

# Pause connector
curl -X PUT http://localhost:8083/connectors/my-connector/pause

# Resume connector
curl -X PUT http://localhost:8083/connectors/my-connector/resume

# Delete connector
curl -X DELETE http://localhost:8083/connectors/my-connector
```

## Kafka Streams

### What is Kafka Streams?
A client library for building stream processing applications and microservices.

### Basic Stream Processing

```java
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import java.util.Properties;

public class WordCountApp {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "wordcount-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        
        StreamsBuilder builder = new StreamsBuilder();
        
        // Read from input topic
        KStream<String, String> textLines = builder.stream("text-input");
        
        // Process: split, group, count
        KTable<String, Long> wordCounts = textLines
            .flatMapValues(line -> Arrays.asList(line.toLowerCase().split("\\W+")))
            .groupBy((key, word) -> word)
            .count();
        
        // Write to output topic
        wordCounts.toStream().to("word-counts", 
            Produced.with(Serdes.String(), Serdes.Long()));
        
        // Start the streams application
        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();
        
        // Graceful shutdown
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
```

### Stream Operations

#### Stateless Operations
```java
// Filter
KStream<String, String> filtered = stream.filter((key, value) -> value.length() > 5);

// Map
KStream<String, String> mapped = stream.mapValues(value -> value.toUpperCase());

// FlatMap
KStream<String, String> flatMapped = stream.flatMapValues(
    value -> Arrays.asList(value.split(",")));

// Branch
KStream<String, String>[] branches = stream.branch(
    (key, value) -> value.startsWith("A"),
    (key, value) -> value.startsWith("B"),
    (key, value) -> true  // default
);
```

#### Stateful Operations
```java
// Aggregation
KTable<String, Long> aggregated = stream
    .groupByKey()
    .aggregate(
        () -> 0L,
        (key, value, aggregate) -> aggregate + value.length()
    );

// Windowing
TimeWindowedKStream<String, String> windowed = stream
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)));

// Join
KStream<String, String> joined = stream1.join(stream2,
    (value1, value2) -> value1 + "-" + value2,
    JoinWindows.of(Duration.ofMinutes(5)));
```

### Interactive Queries

```java
// Query state store
ReadOnlyKeyValueStore<String, Long> store = streams.store(
    StoreQueryParameters.fromNameAndType("word-counts", 
    QueryableStoreTypes.keyValueStore()));

Long count = store.get("hello");
```

## Schema Registry

### What is Schema Registry?
A centralized repository for managing and validating schemas for Kafka messages.

### Avro Schema Example

```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
```

### Producer with Avro

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "http://localhost:8081");

KafkaProducer<String, GenericRecord> producer = new KafkaProducer<>(props);

// Create Avro record
Schema schema = new Schema.Parser().parse(new File("user-schema.avsc"));
GenericRecord user = new GenericData.Record(schema);
user.put("id", 1);
user.put("name", "John Doe");
user.put("email", "john@example.com");

// Send
ProducerRecord<String, GenericRecord> record = 
    new ProducerRecord<>("users", "1", user);
producer.send(record);
```

### Schema Evolution

```bash
# Register schema
curl -X POST http://localhost:8081/subjects/users-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{\"type\":\"record\",\"name\":\"User\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}]}"}'

# Get latest schema
curl http://localhost:8081/subjects/users-value/versions/latest

# Check compatibility
curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "..."}'
```

## Security

### Authentication

#### SASL/PLAIN
```properties
# Server configuration (server.properties)
listeners=SASL_PLAINTEXT://localhost:9092
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```

#### SSL/TLS
```properties
# Server configuration
listeners=SSL://localhost:9093
ssl.keystore.location=/path/to/keystore.jks
ssl.keystore.password=password
ssl.key.password=password
ssl.truststore.location=/path/to/truststore.jks
ssl.truststore.password=password
```

### Authorization (ACLs)

```bash
# Create ACL for user
kafka-acls.sh --add \
  --allow-principal User:alice \
  --operation Read \
  --operation Write \
  --topic orders \
  --bootstrap-server localhost:9092

# List ACLs
kafka-acls.sh --list \
  --bootstrap-server localhost:9092

# Remove ACL
kafka-acls.sh --remove \
  --allow-principal User:alice \
  --operation Read \
  --topic orders \
  --bootstrap-server localhost:9092
```

### Client Configuration for SSL

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9093");
props.put("security.protocol", "SSL");
props.put("ssl.truststore.location", "/path/to/truststore.jks");
props.put("ssl.truststore.password", "password");
props.put("ssl.keystore.location", "/path/to/keystore.jks");
props.put("ssl.keystore.password", "password");
props.put("ssl.key.password", "password");
```

## Monitoring and Operations

### JMX Metrics

```bash
# Enable JMX
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9999 \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false"

bin/kafka-server-start.sh config/server.properties
```

### Key Metrics to Monitor

#### Broker Metrics
- `UnderReplicatedPartitions`: Partitions without enough replicas
- `OfflinePartitionsCount`: Partitions without a leader
- `ActiveControllerCount`: Should be 1 in cluster
- `RequestHandlerAvgIdlePercent`: Handler thread utilization

#### Producer Metrics
- `record-send-rate`: Records sent per second
- `record-error-rate`: Failed record sends
- `request-latency-avg`: Average request latency
- `compression-rate-avg`: Compression effectiveness

#### Consumer Metrics
- `records-consumed-rate`: Records consumed per second
- `fetch-latency-avg`: Average fetch latency
- `records-lag-max`: Maximum lag across partitions

### Monitoring with Prometheus

```yaml
# kafka-exporter deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-exporter
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: kafka-exporter
        image: danielqsj/kafka-exporter:latest
        args:
        - --kafka.server=kafka:9092
        ports:
        - containerPort: 9308
```

### Log Management

```properties
# log4j.properties
log4j.rootLogger=INFO, stdout, kafkaAppender

# File appender
log4j.appender.kafkaAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.kafkaAppender.File=/var/log/kafka/server.log
log4j.appender.kafkaAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.kafkaAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.kafkaAppender.layout.ConversionPattern=[%d] %p %m (%c)%n
```

## Performance Tuning

### Broker Tuning

```properties
# Network threads
num.network.threads=8

# I/O threads
num.io.threads=16

# Socket buffer sizes
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Log settings
num.partitions=3
default.replication.factor=2
log.retention.hours=168
log.segment.bytes=1073741824

# Performance
compression.type=snappy
num.replica.fetchers=4
```

### Producer Tuning

```java
// Throughput optimization
props.put("batch.size", 65536);           // Larger batches
props.put("linger.ms", 100);              // Wait for batching
props.put("compression.type", "snappy");  // Compression
props.put("buffer.memory", 67108864);     // 64 MB buffer

// Latency optimization
props.put("batch.size", 16384);           // Smaller batches
props.put("linger.ms", 0);                // No batching delay
props.put("acks", "1");                   // Leader-only ack
```

### Consumer Tuning

```java
// Throughput optimization
props.put("fetch.min.bytes", 1048576);    // 1 MB min fetch
props.put("fetch.max.wait.ms", 500);      // Wait for data
props.put("max.poll.records", 2000);      // More records per poll

// Latency optimization
props.put("fetch.min.bytes", 1);          // Don't wait
props.put("fetch.max.wait.ms", 100);      // Short wait
props.put("max.poll.records", 100);       // Fewer records
```

### OS-Level Tuning

```bash
# Increase file descriptors
ulimit -n 100000

# Disable swap
sudo swapoff -a

# Set vm.swappiness
echo 1 | sudo tee /proc/sys/vm/swappiness

# Increase network buffer
sudo sysctl -w net.core.rmem_max=2097152
sudo sysctl -w net.core.wmem_max=2097152
```

## Best Practices

### 1. Topic Design
```bash
# Use meaningful topic names
orders.created
orders.updated
user.events

# Appropriate partition count
# Partitions = max(consumers, throughput / producer_throughput)
# Start with: desired_throughput_mb_per_sec / 10

# Replication factor: 3 for production
kafka-topics.sh --create \
  --topic critical-data \
  --partitions 6 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092
```

### 2. Message Design
```java
// Include metadata
{
  "version": "1.0",
  "timestamp": 1634567890,
  "source": "order-service",
  "id": "order-123",
  "data": {
    "customerId": "cust-456",
    "amount": 99.99
  }
}

// Use consistent key for ordering
record = new ProducerRecord<>("orders", orderId, orderData);
```

### 3. Error Handling
```java
// Producer error handling
producer.send(record, (metadata, exception) -> {
    if (exception != null) {
        // Log error
        logger.error("Failed to send message", exception);
        
        // Retry logic or dead letter queue
        sendToDeadLetterQueue(record);
    }
});

// Consumer error handling
try {
    processMessage(record);
    consumer.commitSync();
} catch (Exception e) {
    logger.error("Failed to process message", e);
    // Don't commit - will reprocess
    // Or send to DLQ and commit
}
```

### 4. Idempotence
```java
// Enable idempotent producer
props.put("enable.idempotence", "true");

// Consumer idempotence
// Store processed message IDs
if (processedMessageIds.contains(record.offset())) {
    continue;  // Skip duplicate
}
processMessage(record);
processedMessageIds.add(record.offset());
```

### 5. Monitoring
```bash
# Set up alerts for:
# - Under-replicated partitions > 0
# - Offline partitions > 0
# - Consumer lag > threshold
# - Broker disk usage > 80%
# - High error rate
```

## Real-World Examples

### Event-Driven Microservices

```java
// Order Service - Producer
public class OrderService {
    private KafkaProducer<String, OrderEvent> producer;
    
    public void createOrder(Order order) {
        // Save to database
        orderRepository.save(order);
        
        // Publish event
        OrderEvent event = new OrderEvent(order.getId(), "CREATED", order);
        ProducerRecord<String, OrderEvent> record = 
            new ProducerRecord<>("orders.events", order.getId(), event);
        producer.send(record);
    }
}

// Inventory Service - Consumer
public class InventoryService {
    @KafkaListener(topics = "orders.events", groupId = "inventory-service")
    public void handleOrderEvent(OrderEvent event) {
        if (event.getType().equals("CREATED")) {
            // Reserve inventory
            inventoryRepository.reserveItems(event.getOrder().getItems());
            
            // Publish inventory event
            publishInventoryReserved(event.getOrder().getId());
        }
    }
}
```

### Log Aggregation

```java
// Application logging to Kafka
import org.apache.log4j.AppenderSkeleton;
import org.apache.log4j.spi.LoggingEvent;

public class KafkaLog4jAppender extends AppenderSkeleton {
    private KafkaProducer<String, String> producer;
    private String topic;
    
    @Override
    protected void append(LoggingEvent event) {
        String message = layout.format(event);
        ProducerRecord<String, String> record = 
            new ProducerRecord<>(topic, event.getLoggerName(), message);
        producer.send(record);
    }
}

// Log consumer and processor
public class LogProcessor {
    public void processLogs() {
        KafkaConsumer<String, String> consumer = createConsumer();
        consumer.subscribe(Arrays.asList("application-logs"));
        
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
            for (ConsumerRecord<String, String> record : records) {
                // Parse and store logs
                LogEntry entry = parseLog(record.value());
                elasticsearchClient.index(entry);
            }
        }
    }
}
```

### Change Data Capture (CDC)

```json
// Debezium connector for MySQL
{
  "name": "mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "password",
    "database.server.id": "1",
    "database.server.name": "mysql-db",
    "table.include.list": "inventory.customers,inventory.orders",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes"
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Under-Replicated Partitions
```bash
# Check under-replicated partitions
kafka-topics.sh --describe \
  --under-replicated-partitions \
  --bootstrap-server localhost:9092

# Common causes:
# - Broker is down
# - Network issues
# - Disk I/O problems
# - Insufficient resources

# Solutions:
# - Restart broker
# - Check network connectivity
# - Monitor disk and CPU usage
```

#### 2. Consumer Lag
```bash
# Check consumer lag
kafka-consumer-groups.sh --describe \
  --group my-group \
  --bootstrap-server localhost:9092

# Solutions:
# - Add more consumers
# - Increase consumer poll records
# - Optimize consumer processing
# - Check for consumer rebalancing
```

#### 3. Connection Refused
```bash
# Check broker is running
ps aux | grep kafka

# Check listeners configuration
grep listeners config/server.properties

# Check firewall
sudo iptables -L

# Test connection
telnet localhost 9092
```

#### 4. Out of Memory
```bash
# Increase heap size
export KAFKA_HEAP_OPTS="-Xmx2G -Xms2G"

# Monitor memory usage
jmap -heap <kafka-pid>

# Check for memory leaks
jstat -gc <kafka-pid> 1000
```

#### 5. Disk Full
```bash
# Check disk usage
df -h

# Clean old logs
kafka-configs.sh --alter \
  --entity-type topics \
  --entity-name my-topic \
  --add-config retention.ms=86400000 \
  --bootstrap-server localhost:9092

# Delete old logs manually
rm -rf /tmp/kafka-logs/my-topic-*
```

### Debugging Commands

```bash
# Check broker logs
tail -f /var/log/kafka/server.log

# Check ZooKeeper connection
bin/zookeeper-shell.sh localhost:2181
ls /brokers/ids

# Check topic configuration
kafka-topics.sh --describe \
  --topic my-topic \
  --bootstrap-server localhost:9092

# Test producer
kafka-console-producer.sh \
  --topic test \
  --bootstrap-server localhost:9092

# Test consumer
kafka-console-consumer.sh \
  --topic test \
  --from-beginning \
  --bootstrap-server localhost:9092

# Check consumer group state
kafka-consumer-groups.sh --describe \
  --group my-group \
  --state \
  --bootstrap-server localhost:9092
```

### Performance Issues

```bash
# Enable request logging
log4j.logger.kafka.request.logger=DEBUG, requestAppender

# Profile with JMX
jconsole localhost:9999

# Check network performance
iperf3 -c broker-host

# Monitor with tools
# - LinkedIn Kafka Monitor
# - Confluent Control Center
# - Burrow (consumer lag monitor)
# - Kafka Manager
```

## Resources

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Documentation](https://docs.confluent.io/)
- [Kafka Improvement Proposals (KIPs)](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals)

### Books
- "Kafka: The Definitive Guide" by Neha Narkhede
- "Kafka Streams in Action" by Bill Bejeck
- "Designing Event-Driven Systems" by Ben Stopford

### Tools and Utilities
- [Kafka Tool](https://www.kafkatool.com/) - GUI for managing Kafka
- [Conduktor](https://www.conduktor.io/) - Modern Kafka desktop client
- [AKHQ](https://akhq.io/) - Web UI for Apache Kafka
- [Kafdrop](https://github.com/obsidiandynamics/kafdrop) - Web UI for viewing topics

### Learning Resources
- [Confluent Developer](https://developer.confluent.io/)
- [Kafka Tutorials](https://kafka-tutorials.confluent.io/)
- [Apache Kafka YouTube Channel](https://www.youtube.com/@ApacheKafkaOfficial)

### Community
- [Kafka Users Mailing List](https://kafka.apache.org/contact)
- [Confluent Community](https://forum.confluent.io/)
- [Stack Overflow - Apache Kafka](https://stackoverflow.com/questions/tagged/apache-kafka)

---

**Next Steps**: Learn how to provision and manage infrastructure with [Terraform](../Terraform/README.md)!
